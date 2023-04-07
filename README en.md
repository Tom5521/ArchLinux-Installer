
# Arch-Installer
My Arch Linux installer

No entiendes nada?Tranquilo amigo [aqui](https://github.com/Tom5521/Arch-Linux-Installer/blob/master/README.md) tienes la documentacion en español
## Usage

### Configuration

The JSON file is a data structure used to configure the installation parameters of the provided Python script. Below are the available configuration options:

`custom_pacman_config`: A boolean value indicating whether to use a custom pacman configuration. The default value is "true". 
`keyboard`: Configures the keyboard layout for the installation. The default value is an empty string.

#### Wifi

- `wifi`: An object specifying the wireless network configuration. It consists of the following four properties: 
1. `state`: A boolean value indicating whether to enable the wireless connection. The default value is "false". 
2. `name`: The name of the wireless network to connect to. The default value is an empty string. 
3. `adapter`: The wireless network adapter to use for the connection. The default value is an empty string. 
4. `password`: The password for the wireless network. The default value is an empty string.

#### Partitions

`partitions`: An object specifying the partitions to be used for the installation. It consists of the following properties:

1.  `boot`: An object specifying the boot partition. It consists of the following properties:

*   `partition`: The partition device. The default value is "/dev/".
*   `format`: A boolean value indicating whether to format the partition. The default value is "false".
*   `filesystem`: The file system to be used for the partition. The default value is "fat32".

2.  `root`: An object specifying the root partition. It has the same properties as the boot partition.
3.  `home`: An object specifying the home folder partition. It has the same properties as the boot partition.
4.  `swap`: An object specifying the swap partition. It has the same properties as the boot partition, except it does not have the "filesystem" property.

#### Extra Configs

`grub_install_disk`: The storage device where the GRUB bootloader will be installed. The default value is "/dev/". 
`pacstrap_skip`: A boolean value indicating whether to skip the installation of Arch Linux basic packages. The default value is "false". 
`additional_packages`: A string specifying the additional packages to install. The default value is an empty string. 
`uefi`: A boolean value indicating whether the system uses UEFI instead of BIOS. The default value is "false". 
`arch-chroot`: A boolean value indicating whether to run the script in the Arch Linux chroot environment. The default value is "false". 
`post_install_commands`: A string specifying the commands to be executed after the package installation. The default value is an empty string. 
`post_install_chroot_commands`: A string specifying the commands to be executed after the package installation in the Arch Linux chroot environment. The default value is an empty string. 
`reboot`: Allows specifying whether to restart the system after installation. If this field is omitted, the default configuration will be used.