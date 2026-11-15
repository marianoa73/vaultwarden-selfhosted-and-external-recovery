# Opciones de alojamiento, destino de las copias y cifrado

[English version](options.en.md)

El diseño de referencia usa un servidor chico en casa, un VPS remoto y herramientas de código abierto, pero nada de eso es obligatorio. Esta página lista las alternativas de **dónde corre cada cosa**, **adónde van las copias cifradas** y **cómo proteger las claves**, y la regla que nunca cambia: **todo se cifra antes de salir de la máquina y la frase de paso se guarda aparte de las copias.**

## Dónde pueden correr el servidor y el standby

| Opción | Sirve para | Ojo con |
|---|---|---|
| Equipo físico chico en casa (mini PC, placa de bajo consumo) | el principal: poco consumo, siempre encendido, bajo tu control | necesita UPS y un segundo lugar para las copias |
| **Máquina virtual en tu propio hardware** (Proxmox, KVM/libvirt, Hyper-V, VirtualBox, hipervisor del NAS) | el principal o el standby; snapshots fáciles y reconstrucción rápida | una VM en el mismo equipo que el principal no sobrevive a la pérdida de ese equipo: poné el standby en otra máquina |
| **VPS** (cualquier servidor chico en la nube) | el receptor remoto y un standby apagado, fuera de tu casa | es hardware ajeno: ahí solo viven archivos cifrados, sin frase de paso y sin ruta a tu red de casa |
| Solo contenedor, en cualquier Linux o en Windows con WSL2 | una primera prueba o una instalación en notebook | el equipo tiene que estar encendido a la hora del backup; mejor un equipo de escritorio o uno siempre encendido |
| Segundo equipo físico en otro lugar (familiar, oficina) | un standby que controlás vos | requiere el mismo endurecimiento que el principal |

El principal y el standby no deben compartir la misma falla: otra máquina, otro lugar y, si se puede, otra red.

## Adónde pueden ir las copias cifradas

| Destino | Cómo | Notas |
|---|---|---|
| Servidor remoto por SSH (por defecto) | `vw-send.sh` con una clave restringida y un comando forzado | el receptor puede guardar pero nunca abrir los archivos |
| **Drive en la nube** (Google Drive, OneDrive, Dropbox) | `vw-copy.sh` mediante `rclone`, `VW_RCLONE_REMOTE` | cómodo y barato; el archivo ya está cifrado, así que el proveedor no puede leerlo |
| Almacenamiento de objetos (compatible con S3, Backblaze B2, otros) | igual, mediante `rclone` | activá versionado o bloqueo de objetos, para recuperar una copia borrada o pisada |
| Disco externo, USB o carpeta de un NAS | `vw-copy.sh`, `VW_COPY_DIR` | dejá un disco fuera de línea y lejos de casa; desconectalo después de copiar |
| Servidor SFTP o WebDAV | igual, mediante `rclone` | cualquier servidor en el que confíes para guardar archivos, no para leerlos |

Apuntá a la regla 3-2-1: **tres copias, en dos tipos de medio, una de ellas fuera del lugar.** Usá una cuenta o carpeta dedicada con los permisos mínimos y verificación en dos pasos, y nunca reutilices la cuenta de la bóveda.

## Cifrado del más alto nivel

- **Cifrar antes de enviar.** El archivo es un GnuPG con AES-256 y el derivado de clave más exigente (`--s2k-mode 3`, cantidad máxima de iteraciones). El cifrado propio del proveedor es una capa extra, nunca la única.
- **Verificar descifrando.** Cada archivo nuevo se abre y se revisa su base de datos antes de reemplazar nada. Un archivo que nunca abriste no es un backup.
- **Una frase de paso larga y aleatoria**, de al menos 128 bits (48 bytes aleatorios sobran), generada por el script y nunca elegida a mano. Es un secreto distinto de la contraseña maestra.
- **Variante con clave pública (más fuerte para el servidor).** Si la máquina que hace los backups solo tiene una clave pública, un servidor comprometido no puede leer los archivos viejos, y la clave privada queda fuera de línea. Pide un cambio chico en los scripts (cifrar en `vw-backup.sh`, descifrar en `vw-restore.sh`):

```bash
# en el principal: solo se importa la clave PÚBLICA
gpg --batch --yes --encrypt --recipient recovery-key --cipher-algo AES256 -o vault.tar.gpg vault.tar
# en la máquina de recuperación: la clave PRIVADA, guardada fuera de línea, lo abre
gpg --decrypt vault.tar.gpg > vault.tar
```

- **Nunca subir nada legible.** `vw-copy.sh` rechaza un archivo que no esté cifrado con GnuPG.
- Guardá la configuración de la herramienta de la nube (el token de acceso) con permisos 600 y alcance mínimo: puede escribir backups y nada más.

## Dónde vive la frase de paso

Las copias son tan seguras como la frase de paso, así que vive **aparte de ellas**:

- En **papel, en dos lugares separados** (caja fuerte de casa, casa de un familiar, caja del banco). Nada más es la copia principal.
- **Nunca en la misma cuenta de nube, disco o servidor** que los archivos, y **nunca dentro de la propia bóveda**: si perdés la bóveda perdés también la llave de sus backups.
- Opcionalmente partida entre personas de confianza (por ejemplo 2 de 3), para que nadie pueda abrir los backups solo y se pueda perder una parte.
- Un token de hardware o un gestor de contraseñas sin conexión puede ser una segunda copia, nunca la única.
- Anotá **para qué sirve y dónde están los archivos**, no la frase ni su ubicación en un documento compartido.
- Si la frase pudo ser vista, generá una nueva, hacé un backup nuevo y retirá las copias viejas.

## Niveles de recuperación ante desastres

| Nivel | Qué mantenés | Tiempo de recuperación | Punto de recuperación |
|---|---|---|---|
| Solo archivos (frío) | copias cifradas en dos lugares | horas: instalar el servidor en cualquier equipo y restaurar | la última noche |
| Standby en una VM en otra máquina | la misma imagen, apagada | de minutos a una hora: arrancar y restaurar | la última noche |
| Standby en un VPS | la misma imagen, apagada | de minutos a una hora, desde cualquier lugar | la última noche |
| Standby tibio (recibe la copia y se revisa a diario) | la misma imagen, restaurada con un horario | minutos | la última noche |

Elegí el nivel más bajo con el que tu familia pueda vivir, y ensayalo. El contacto de emergencia ([emergency-access.md](emergency-access.md)) es la última red de seguridad, no el plan.

## Configurar un segundo destino

Sumá una o las dos líneas al archivo de entorno privado y corré un backup a mano:

```bash
# /etc/vw-recovery.env  (modo 600)
VW_COPY_DIR=/ruta/al/disco/montado          # disco externo, carpeta de NAS u otra máquina
VW_RCLONE_REMOTE=midrive:backups-boveda     # un remoto de rclone y su carpeta, creado con: rclone config
```

```bash
sudo systemctl start vw-backup.service && journalctl -u vw-backup.service -n 20
rclone lsf midrive:backups-boveda            # tenés que ver el .tar.gpg y su .sha256
```

Después restaurá desde **esa** copia en un equipo de repuesto al menos una vez, como indica la guía de [recuperación](recovery.md).

## Lista de control

1. Servidor y standby en máquinas distintas, de preferencia en lugares distintos.
2. Al menos tres copias, dos tipos de medio, una fuera del lugar.
3. Toda copia cifrada antes de salir de la máquina y verificada descifrando.
4. Frase de paso larga, aleatoria y distinta de la contraseña maestra.
5. Frase de paso en papel en dos lugares, nunca junto a los archivos y nunca en la bóveda.
6. Cuenta de almacenamiento dedicada, alcance mínimo y verificación en dos pasos.
7. Versionado o bloqueo de objetos donde el proveedor lo ofrezca.
8. Un ensayo de restauración desde cada destino al menos cada trimestre.
9. La antigüedad del último backup en un mensaje de estado diario.
