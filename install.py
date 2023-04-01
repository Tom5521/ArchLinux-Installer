from os import system as sys
import os
import urllib
from time import sleep as sl

print("My custom Arch Installer\nRun this with sudo")
import urllib.request


def clear():
    sys("clear")


def internet_on():
    try:
        urllib.request.urlopen("https://archlinux.org/", timeout=1)
        return True
    except urllib.request.URLError as e:
        return False


def get_connection_type():
    route = os.popen("ip route").read()
    if "wlan" in route:
        return "wifi"
    elif "eth" in route:
        return "wired"
    else:
        return "desconocida"


print("Put the keyboard")
keyboard = str(input(""))
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
disk = str(input("Why DISK want use?\n:"))
sys(f"cfdisk {disk}")
print(
    "Why partitions you want use to install?(leave it blank if you don't want it to be used)"
)
print("root partition?")
root_partition = str(input(":"))
print("boot partition?")
boot_partition = str(input(":"))
print("home partition?")
home_partition = str(input(":"))
print("swap partition?")
swap_partition = str(input(":"))
clear()
check = str(input("Format partitions?[Yes/No]\n:"))
if check.upper() == "YES" or "Y":
    double_check = str(input("YOU REALLY WANT TO FORMAT THE PARTITIONS?[YES/NO]\n:"))
    if double_check == "YES":
        sys(f"mkfs.ext4 -F {root_partition}")
        sys(f"mkfs.fat -F 32 {boot_partition}")
        if home_partition != "":
            check = str(input("Format home partition?[Yes/No]\n:"))
            if check.upper() == "YES" or "Y":
                double_check = str(
                    input("YOU REALLY WANT TO FORMAT THE HOME PARTITION?[YES/NO]\n:")
                )
                if double_check == "YES":
                    sys(f"mkfs.ext4 -F {home_partition}")
        if swap_partition != "":
            sys(f"mkswap {swap_partition}")
sys(f"mount {root_partition} /mnt")
sys(f"mount {boot_partition} /mnt/boot")
if home_partition != "":
    sys(f"mount {home_partition} /mnt/home")
if swap_partition != "":
    sys(f"swaplabel {swap_partition}")
if get_connection_type == "wifi":
    web = "networkmanager "
print("put the faster pacman config")
sys("cp -f pacman.conf /etc")
sys("pacman -Syy")
clear()
print("Custom packages to install?\n:")
custom = str(input())
sys(
    f"pacstrap /mnt base base-devel grub git efibootmgr dialog wpa_supplicant nano linux linux-headers linux-firmware {web} {custom}"
)
sys("genfstab -U /mnt >> /mnt/etc/fstab")
clear()
sys(f"grub-install --root-directory=/mnt {root_partition}")
clear()
sleep_seconds = 5
while True:
    clear()
    print(f"Instalation Completed!\nRebooting in {sleep_seconds} seconds...", end="\r")
    sleep_seconds -= 1
    sl(1)
    if sleep_seconds == 0:
        sys("reboot now")
