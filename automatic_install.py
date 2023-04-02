from os import system as sys
import os
import urllib
from time import sleep as sl
import json

with open("config.json") as f:
    dat = json.load(f)


def internet_on():
    try:
        urllib.request.urlopen("https://archlinux.org/", timeout=1)
        return True
    except urllib.request.URLError as e:
        return False


def clear():
    sys("clear")


keyboard = dat["keyboard"]
wifi = {
    "state": dat["wifi"]["state"],
    "name": dat["wifi"]["name"],
    "adaptator": dat["wifi"]["adaptator"],
}
additional_packages = dat["additional_packages"]
chroot = dat["chroot"]
reboot = dat["reboot"]
custom_config = dat["custom_pacman_config"]
uefi = dat["uefi"]


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


sys(f"loadkeys {keyboard}")
global wifii
if wifi["state"] == "y":
    sys("rfkill unblock all")
    sys(f"ip link set {wifi['adaptator']} up")
    sys(f"iwctl station {wifi['adaptator']} connect {wifi['name']}")
    wifii = "networkmanger "
if custom_config == "y":
    sys("cp pacman.conf /etc")

if partitions.boot["format"] == "y":
    if partitions.boot["format"] == "fat32":
        sys("mkfs.fat -F 32 " + partitions.boot["partition"])
    else:
        sys(
            "mkfs." + partitions.boot["filesystem"] + " " + partitions.boot["partition"]
        )
if partitions.root["format"] == "y":
    sys("mkfs." + partitions.root["filesystem"] + " " + partitions.root["partition"])

if partitions.home["format"] == "y" and partitions.home["partition"] != "/dev/":
    sys("mkfs." + partitions.home["filesystem"] + " " + partitions.home["partition"])

if partitions.swap["format"] == "y" and partitions.swap["partition"] != "/dev/":
    sys("mkswap " + partitions.swap["partition"])


sys("mount " + partitions.root["partition"] + " /mnt")
if uefi == "y":
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

sys(
    f"pacstrap /mnt base base-devel grub git efibootmgr dialog wpa_supplicant nano linux linux-headers linux-firmware {wifii} {additional_packages}"
)
sys("genfstab -U /mnt >> /mnt/etc/fstab")
if uefi == "y":
    sys("grub-install --target=x86_64-efi --efi-directory=/mnt/efi --recheck")
else:
    sys("grub-install --target=i386-pc --recheck " + partitions.boot["partition"])
sys("exit|grub-mkconfig -o /boot/grub/grub.cfg|chroot /mnt")
