import json
from os import system as sys
import subprocess


def red(datt):
    return "\033[31m" + datt + "\033[0m"


with open("config.json") as f:
    dat = json.load(f)

if dat["uefi"] == False:
    print("uefi is false")
else:
    print("uefi is true")


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

test = "hola me llamo carlos"
# sys("rfkill unblock all")
# sys(f"ip link set {wifi['adaptator']} up")
# sys(
#    f"iwctl station {wifi['adaptator']} connect {wifi['name']} --passphrase {wifi['wifi_passwd']}"
# )


def command_read(command):
    result = subprocess.run(command.split(), stdout=subprocess.PIPE)
    output = result.stdout.decode("utf-8")
    return output


if wifi["adaptator"] in command_read("ip link"):
    print("test1 yes")
if ".gitignore" in command_read("ls -a"):
    print("test2 yes")

if keyboard in command_read("localectl list-keymaps"):
    pass
    # sys(f"echo KEYMAP={keyboard} > /mnt/etc/vconsole.conf")
else:
    print(red("WARNING:keyboard specification not exist"))
