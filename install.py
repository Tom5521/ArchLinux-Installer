import json
import subprocess
import os
from sys import exit


def clear():
    sys("clear")


def command_read(command):
    result = subprocess.run(command.split(), stdout=subprocess.PIPE)
    output = result.stdout.decode("utf-8")
    return output


def red(datt):
    return "\033[31m" + datt + "\033[0m"


def yellow(self):
    return f"\033[33m{self}\033[0m"


def green(datt):
    return "\033[32m" + datt + "\033[0m"

def error():
    print(red("ERROR"))

def sys(command):
    try:
        subprocess.check_call(command, shell=True)
        return True
    except subprocess.CalledProcessError:
        subprocess.call(command, shell=True)
        error()
        return False


if "config.json" not in os.listdir():
    print(red("Configuration file does not exist"))
    print(yellow("Cloning config.json template"))
    sys(
        "curl -LJO https://raw.githubusercontent.com/Tom5521/ArchLinux-Installer/master/config.json"
    )
    exit()

with open("config.json") as f:
    dat = json.load(f)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~FLAGS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
keyboard = dat["keyboard"]
wifi = {
    "state": dat["wifi"]["state"],
    "name": dat["wifi"]["name"],
    "adaptator": dat["wifi"]["adaptator"],
    "wifi_passwd": dat["wifi"]["password"],
}
additional_packages = dat["additional_packages"]
arch_chroot = dat["arch-chroot"]
reboot = dat["reboot"]
custom_config = dat["custom_pacman_config"]
uefi = dat["uefi"]
p_i_c = dat["post_install_commands"]
p_i_ch_c = dat["post_install_chroot_commands"]
pacstrap_skip = dat["pacstrap_skip"]
global wifii
wifii = ""
grub_install_disk = dat["grub_install_disk"]

if custom_config == True and "pacman.conf" not in os.listdir():
    print(red("no custom pacman config"))
    print(yellow("Cloning pacman.conf..."))
    sys(
        "curl -LJO https://raw.githubusercontent.com/Tom5521/ArchLinux-Installer/master/pacman.conf"
    )


class partitions:
    boot = {
        "partition": dat["partitions"]["boot"]["partition"],
        "format": dat["partitions"]["boot"]["format"],
        "filesystem": dat["partitions"]["boot"]["filesystem"],
    }
    root = {
        "partition": dat["partitions"]["root"]["partition"],
        "format": dat["partitions"]["root"]["format"],
        "filesystem": dat["partitions"]["root"]["filesystem"],
    }
    home = {
        "partition": dat["partitions"]["home"]["partition"],
        "format": dat["partitions"]["home"]["format"],
        "filesystem": dat["partitions"]["home"]["filesystem"],
    }
    swap = {
        "partition": dat["partitions"]["swap"]["partition"],
        "format": dat["partitions"]["swap"]["format"],
    }


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if wifi["state"] == True and wifi["adaptator"] in command_read("ip link"):
    sys("rfkill unblock all")
    sys(f"ip link set {wifi['adaptator']} up")
    sys(
        f"iwctl station {wifi['adaptator']} connect {wifi['name']} --passphrase {wifi['wifi_passwd']}"
    )
    wifii = "networkmanger iwd "
if wifi["adaptator"] not in command_read("ip link") and wifi["state"] == True:
    print(red("WARNING:Adaptator not found"))
if custom_config == True and "---YES---THATS---MODIFIED---" not in command_read(
    "cat /etc/pacman.conf"
):
    sys("cp pacman.conf /etc")
else:
    print(green("Pacman.conf already pasted"))
# ~~~~~~~~~~~~~~~~~~~~~~~~~FORMAT~PARTITIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print(red("FORMATTING PARTITIONS"))
if partitions.boot["format"] == True:
    if partitions.boot["filesystem"] == "fat32":
        sys("mkfs.vfat -F 32 " + partitions.boot["partition"])
    else:
        sys(
            "mkfs."
            + partitions.boot["filesystem"]
            + " -F "
            + partitions.boot["partition"]
        )
if partitions.root["format"] == True:
    sys("mkfs." + partitions.root["filesystem"] + " -F " + partitions.root["partition"])

if partitions.home["format"] == True and partitions.home["partition"] != "/dev/":
    sys("mkfs." + partitions.home["filesystem"] + " -F " + partitions.home["partition"])

if partitions.swap["format"] == True and partitions.swap["partition"] != "/dev/":
    sys("mkswap " + partitions.swap["partition"])
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~MOUNT~PARTITIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print(yellow("Mounting partitions..."))
sys("mount " + partitions.root["partition"] + " /mnt")
if uefi == True:
    if "efi" not in os.listdir(path="/mnt"):
        sys("mkdir /mnt/efi")
    sys("mount " + partitions.boot["partition"] + " /mnt/efi")
elif "boot" not in os.listdir(path="/mnt"):
    sys("mkdir /mnt/boot")
sys("mount " + partitions.boot["partition"] + " /mnt/boot")
if partitions.home["partition"] != "/dev/":
    if "home" not in os.listdir(path="/mnt"):
        sys("mkdir /mnt/home")
    sys("mount " + partitions.home["partition"] + " /mnt/home")
if partitions.swap["partition"] != "/dev/":
    sys("swaplabel " + partitions.swap["partition"])
    sys("swapon")
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if pacstrap_skip == False:
    sys(
        f"pacstrap /mnt base base-devel grub git efibootmgr dialog wpa_supplicant nano linux linux-headers linux-firmware {wifii} {additional_packages}"
    )

else:
    print(yellow("Skipping pacstrap..."))
print(yellow("generating fstab"))
fstab = sys("genfstab -pU /mnt >> /mnt/etc/fstab")
if fstab == True:
    print(green("Fstab generated correctly"))
print(yellow("Installing grub..."))
if uefi == False:
    grub = sys(f"echo exit|echo grub-install {grub_install_disk}|arch-chroot /mnt")
else:
    print(yellow("UEFI/EFI mode is true"))
    grub = sys(
        f"echo exit|echo grub-install {grub_install_disk} --efi-directory /efi|arch-chroot /mnt"
    )

mkconfig = sys("echo exit|echo grub-mkconfig -o /boot/grub/grub.cfg|arch-chroot /mnt")
if grub and mkconfig == True:
    print(green("Grub installed correctly"))

if p_i_c != "":
    sys(p_i_c)
if keyboard in command_read("localectl list-keymaps"):
    print(yellow("Setting Keyboard"))
    keyboards = sys(
        f"echo exit|echo echo KEYMAP={keyboard} > /mnt/etc/vconsole.conf|arch-chroot /mnt"
    )
    if keyboards == True:
        print(green("Keyboard configured correctly"))
else:
    print(red("WARNING:keyboard specification not exist "))

if p_i_ch_c != "":
    sys(f"echo exit|echo {p_i_ch_c}|arch-chroot /mnt")

print(
    red(
        'please use the command "passwd --root /mnt" to set the root password before rebooting.'
    )
)
if arch_chroot == True:
    sys("arch-chroot /mnt")

if reboot == True:
    sys("reboot")
