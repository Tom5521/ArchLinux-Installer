from os import system as sys
import json
import subprocess

with open("config.json") as f:
    dat = json.load(f)


def clear():
    sys("clear")


def command_read(command):
    result = subprocess.run(command.split(), stdout=subprocess.PIPE)
    output = result.stdout.decode("utf-8")
    return output


def red(datt):
    return "\033[31m" + datt + "\033[0m"


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


class partitions:
    boot = {
        "partition": dat["partitions"]["boot"]["partition"],
        "format": dat["partitions"]["boot"]["format"],
        "filesystem": dat["partitions"]["boot"]["filesystem"],
    }
    root = {
        "partition": dat["partitions"]["root"]["partition"],
        "format": dat["partitions"]["boot"]["format"],
        "filesystem": dat["partitions"]["boot"]["filesystem"],
    }
    home = {
        "partition": dat["partitions"]["home"]["partition"],
        "format": dat["partitions"]["boot"]["format"],
        "filesystem": dat["partitions"]["boot"]["filesystem"],
    }
    swap = {
        "partition": dat["partitions"]["swap"]["partition"],
        "format": dat["partitions"]["boot"]["format"],
    }


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if wifi["state"] == True and wifi["adaptator"] in command_read("ip link"):
    sys("rfkill unblock all")
    sys(f"ip link set {wifi['adaptator']} up")
    sys(
        f"iwctl station {wifi['adaptator']} connect {wifi['name']} --passphrase {wifi['wifi_passwd']}"
    )
    wifii = "networkmanger iwd "
if wifi["adaptator"] not in command_read("ip link"):
    print(red("WARNING:Adaptator not found"))
if custom_config == True and "---YES---THATS---MODIFIED---" not in command_read(
    "cat /etc/pacman.conf"
):
    sys("cp pacman.conf /etc")
else:
    print(red("WARNING:pacman.conf already pasted"))
# ~~~~~~~~~~~~~~~~~~~~~~~~~FORMAT~PARTITIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if partitions.boot["format"] == True:
    if partitions.boot["filesystem"] == "fat32":
        sys("mkfs.fat -F 32 " + partitions.boot["partition"])
    else:
        sys(
            "mkfs." + partitions.boot["filesystem"] + " " + partitions.boot["partition"]
        )
if partitions.root["format"] == True:
    sys("mkfs." + partitions.root["filesystem"] + " " + partitions.root["partition"])

if partitions.home["format"] == True and partitions.home["partition"] != "/dev/":
    sys("mkfs." + partitions.home["filesystem"] + " " + partitions.home["partition"])

if partitions.swap["format"] == True and partitions.swap["partition"] != "/dev/":
    sys("mkswap " + partitions.swap["partition"])
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~MOUNT~PARTITIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sys("mount " + partitions.root["partition"] + " /mnt")
if uefi == True:
    sys("mkdir /mnt/efi")
    sys("mount " + partitions.boot["partition"] + " /mnt/efi")
else:
    sys("mkdir /mnt/boot")
    sys("mount " + partitions.boot["partition"] + " /mnt/boot")
if partitions.home["partition"] != "/dev/":
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
sys("genfstab -U /mnt >> /mnt/etc/fstab")
if uefi == True:
    sys(
        "exit|echo grub-install --target=x86_64-efi --efi-directory=/mnt/efi --recheck|arch-chroot /mnt"
    )
else:
    sys("grub-install --target=i386-pc --recheck " + partitions.boot["partition"])
sys("exit|echo grub-mkconfig -o /boot/grub/grub.cfg|arch-chroot /mnt")
sys(p_i_c)
if keyboard in command_read("localectl list-keymaps"):
    sys(f"echo KEYMAP={keyboard} > /mnt/etc/vconsole.conf")
else:
    print(red("WARNING:keyboard specification not exist"))
sys(f"exit|{p_i_ch_c}|arch-chroot /mnt")
if arch_chroot == True:
    sys("arch-chroot /mnt")
if reboot == True:
    sys("reboot")
