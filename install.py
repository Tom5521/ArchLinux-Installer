from os import system as sys
import os
import urllib
from time import sleep as sl

print("My custom Arch Installer\nRun this with sudo")
import urllib.request


def clear():
    sys("clear")
    pass


def internet_on():
    try:
        urllib.request.urlopen("https://archlinux.org/", timeout=1)
        return True
    except urllib.request.URLError as e:
        return False


global web
web = ""


def get_connection_type():
    route = os.popen("ip route").read()
    if "wlan" in route:
        web = "networkmanager "
        return "wifi", web
    elif "eth" in route:
        return "wired"
    else:
        return "unknown"


keyboard = str(input("Put the keyboard\n:"))
sys(f"loadkeys {keyboard}")
clear()
if internet_on() == False:
    if get_connection_type() == "wifi":
        print("Connect to wifi")
        print("rfkill unblock")
        sys("rfkill unblock all")
        print("put wlan0 up")
        sys("ip link set wlan0 up")
        wifi = str(input("Name of your wifi:"))
        sys(f"iwctl station wlan0 connec {wifi}")
    else:
        pass
print("Config the partitions")
sys("fdisk -l")
disk = str("/dev/" + input("Why DISK want use?\n:/dev/"))
sys(f"cfdisk {disk}")
clear()
sys("fdisk -l")
print(
    "Why partitions you want use to install?(leave it blank if you don't want it to be used)"
)
root_partition = str("/dev/" + input("root partition?\n:/dev/"))
boot_partition = str("/dev/" + input("boot partition?\n:/dev/"))
home_partition = str("/dev/" + input("home partition?\n:/dev/"))
swap_partition = str("/dev/" + input("swap partition?\n:/dev/"))
clear()
check = str(input("Format partitions?[Yes/No]\n:"))
if check.upper() == "YES" or "Y":
    double_check = str(input("YOU REALLY WANT TO FORMAT THE PARTITIONS?[YES/NO]\n:"))
    if double_check == "YES":
        sys(f"mkfs.ext4 -F {root_partition}")
        sys(f"mkfs.fat -F 32 {boot_partition}")
        if home_partition != "/dev/":
            check = str(input("Format home partition?[Yes/No]\n:"))
            if check.upper() == "YES" or "Y":
                double_check = str(
                    input("YOU REALLY WANT TO FORMAT THE HOME PARTITION?[YES/NO]\n:")
                )
                if double_check == "YES":
                    sys(f"mkfs.ext4 -F {home_partition}")
        if swap_partition != "/dev/":
            sys(f"mkswap {swap_partition}")
if check == "NO" or "N":
    pass
sys(f"mount {root_partition} /mnt")
check_boot = os.listdir("/mnt")
if "boot" not in check_boot:
    os.mkdir("/mnt/boot")
sys(f"mount {boot_partition} /mnt/boot")
if home_partition != "/dev/":
    sys(f"mount {home_partition} /mnt/home")
if swap_partition != "/dev/":
    sys(f"swaplabel {swap_partition}")
print("put the faster pacman config")
sys("cp -f pacman.conf /etc")
clear()
custom = str(input("Custom packages to install?\n:"))
sys(
    f"pacstrap /mnt base base-devel grub git efibootmgr dialog wpa_supplicant nano linux linux-headers linux-firmware {web} {custom}"
)
clear()
os.chdir("/mnt")
sys(
    f"grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=arch_grub --recheck"
)
sys("grub-mkconfig -o /mnt/boot/grub/grub.cfg")
clear()
sys("genfstab -U /mnt >> /mnt/etc/fstab")
sleep_seconds = 10

while True:
    clear()
    print(
        f"Instalation Completed!\nNow you can disconnect the USB!\nRebooting in {sleep_seconds} seconds...",
        end="\r",
    )
    sleep_seconds -= 1
    sl(1)
    if sleep_seconds == 0:
        sys("reboot now")
