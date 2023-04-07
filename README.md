# Arch-Installer
Mi instalador de Arch-Linux

Do you not understand anything? Don't worry, [here](https://github.com/Tom5521/Arch-Linux-Installer/blob/master/README%20en.md) is the English version
## Uso

### Configurar
El archivo JSON es una estructura de datos que se utiliza para configurar los parámetros de instalación del script de Python proporcionado. A continuación, se describe cada una de las opciones de configuración disponibles:

```custom_pacman_config```: Un valor booleano que indica si se desea utilizar una configuración personalizada de pacman. El valor predeterminado es "true".

```keyboard```: Configura el diseño del teclado para la instalación. El valor predeterminado es "en".
#### Wifi
```wifi```: Un objeto que especifica la configuración de la red inalámbrica. Se compone de las siguientes cuatro propiedades:
1. ```state```: Un valor booleano que indica si se desea habilitar la conexión inalámbrica. El valor predeterminado es "false".
2. ```name```: El nombre de la red inalámbrica a la que se desea conectar. El valor predeterminado es una cadena vacía.
3. ```adaptator```: El adaptador de red inalámbrica que se utilizará para la conexión. El valor predeterminado es una cadena vacía.
4. ```password```: La contraseña de la red inalámbrica. El valor predeterminado es una cadena vacía.
#### Particiones
```partitions```: Un objeto que especifica las particiones que se utilizarán para la instalación. Se compone de las siguientes propiedades:
- ```boot```: Un objeto que especifica la partición de arranque. Se compone de las siguientes propiedades:
1. ```partition```: El dispositivo de la partición. El valor predeterminado es "/dev/".
2. ```format```: Un valor booleano que indica si se desea formatear la partición. El valor predeterminado es "false".
3. ```filesystem```: El sistema de archivos que se utilizará para la partición. El valor predeterminado es "fat32".
- ```root```: Un objeto que especifica la partición raíz. Se compone de las mismas propiedades que la partición de arranque.
- ```home```: Un objeto que especifica la partición de la carpeta de inicio. Se compone de las mismas propiedades que la partición de arranque.
- ```swap```: Un objeto que especifica la partición de intercambio. Se compone de las mismas propiedades que la partición de arranque, excepto que no tiene la propiedad "filesystem".

#### Configuraciones Extra

```grub_install_disk```: El dispositivo de almacenamiento en el que se instalará el gestor de arranque GRUB. El valor predeterminado es "/dev/".

```pacstrap_skip```: Un valor booleano que indica si se desea saltar la instalación de los paquetes básicos de Arch Linux. El valor predeterminado es "false".
```additional_packages```: Una cadena que especifica los paquetes adicionales que se desean instalar. El valor predeterminado es una cadena vacía.

```uefi```: Un valor booleano que indica si el sistema utiliza UEFI en lugar del BIOS. El valor predeterminado es "false".

```arch-chroot```: Un valor booleano que indica si se debe ejecutar el script en el entorno chroot de Arch Linux. El valor predeterminado es "false".

```post_install_commands```: Una cadena que especifica los comandos que se ejecutarán después de la instalación de los paquetes. El valor predeterminado es una cadena vacía.

```post_install_chroot_commands```: Una cadena que especifica los comandos que se ejecutarán después de la instalación de los paquetes en el entorno chroot de Arch Linux. El valor predeterminado es una cadena vacia

```reboot```: permite especificar si se debe reiniciar el sistema después de la instalación. Si se omite este campo, se utilizará la configuración por defecto.