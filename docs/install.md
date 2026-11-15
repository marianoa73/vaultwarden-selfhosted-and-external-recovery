# Instalación del servidor local

[English version](install.en.md)

## Requisitos

Una máquina Linux chica con Docker y Compose, una VPN en malla a la que se una esa máquina y tus dispositivos, y un usuario para los backups. Nada de esto necesita una dirección pública. Todos los nombres de abajo son marcadores.

## 1. Crear el servidor

Copiá `examples/compose.primary.yml`, poné tu dominio privado y el hash de la imagen que verificaste, y levantalo:

```bash
mkdir -p /ruta/a/vaultwarden/data && cd /ruta/a/vaultwarden
cp /ruta/al/repo/examples/compose.primary.yml compose.yml
docker compose up -d
```

## 2. Publicarlo sólo en la red privada

Publicá el puerto de loopback con la función HTTPS de tu VPN en malla o con un proxy inverso que escuche sólo en la interfaz privada. Comprobá desde un dispositivo que **no** esté en la red privada que la dirección no responde.

## 3. Crear las cuentas y cerrar el registro

El registro está cerrado por defecto: abrilo sólo el minuto necesario, creá tu cuenta (y la del contacto de emergencia, ver [acceso de emergencia](emergency-access.md)) y volvé a cerrarlo:

```bash
sed -i 's/SIGNUPS_ALLOWED: "false"/SIGNUPS_ALLOWED: "true"/' compose.yml && docker compose up -d   # abrir
# ... crear las cuentas ...
sed -i 's/SIGNUPS_ALLOWED: "true"/SIGNUPS_ALLOWED: "false"/' compose.yml && docker compose up -d   # cerrar
```

## 4. Endurecer la cuenta

1. Elegí una contraseña maestra larga que puedas memorizar.
2. En la bóveda web, subí la derivación de clave a Argon2id con parámetros más fuertes.
3. Activá la app autenticadora y registrá dos llaves físicas; imprimí el código de recuperación.
4. Instalá los clientes oficiales en tus dispositivos y apuntalos a tu dirección privada.
5. Desactivá el guardado de contraseñas en todos los navegadores.

## 5. Verificar

Creá un elemento de prueba, bloqueá y desbloqueá desde un segundo dispositivo y confirmá que la página de administración está apagada. Después seguí con el [backup](backup.md).
