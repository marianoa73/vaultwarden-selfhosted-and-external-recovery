# Por qué este proyecto, y qué usar en su lugar

[English version](why.en.md)

## La necesidad

Administrar sitios web, redes sociales, publicaciones, hosting, servidores en la nube, servicios de IA y cuentas de brokers multiplica las credenciales. Si se las deja solas terminan repetidas, guardadas en los navegadores, pegadas en notas o perdidas. Este proyecto nació para **asegurar y controlar todas las claves de esos proyectos en un solo lugar**, con segundo factor, una copia cifrada fuera de sitio y un camino de regreso probado si algo falla.

## El modelo: tres niveles de secretos

| Nivel | Qué es | Dónde vive |
|---|---|---|
| Secretos raíz | contraseña maestra, códigos de recuperación del segundo factor, frase del backup, recuperación de la cuenta de correo propietaria | **escritos en papel**, guardados offline en lugares separados; la contraseña maestra además se memoriza |
| Credenciales de uso diario | los muchos ingresos que se usan todos los días | **en el gestor de contraseñas**: generadas, únicas, autocompletadas, nunca retipeadas |
| Secretos de máquina | claves de API, tokens, claves de despliegue | en el gestor (notas seguras), con el menor alcance posible, topes de gasto y fecha de rotación |

La regla: **papel para las pocas claves que abren todo; el gestor para las muchas que se usan a diario**. Si el gestor falla, el papel lo recupera; si se pierde el papel, el gestor sigue funcionando.

## Alternativas

Este repositorio describe un camino probado, no el único. Sirve cualquier modelo parecido; revisá en cada producto sus funciones, precio y condiciones de privacidad actuales.

| Necesidad | Ejemplos |
|---|---|
| Bóveda propia | Vaultwarden (este proyecto; un servidor no oficial compatible con los clientes de Bitwarden), la edición autoalojada oficial de Bitwarden, KeePassXC con un archivo sincronizado |
| Bóveda en servicio externo | Bitwarden, 1Password, Proton Pass, Dashlane |
| App autenticadora (TOTP) | Google Authenticator, Microsoft Authenticator, Aegis (Android, código abierto), 2FAS, Ente Auth |
| Llaves físicas de seguridad (FIDO2) | YubiKey, Google Titan; registrar al menos dos |
| Passkeys | integradas en la mayoría de las plataformas; usarlas donde el sitio las ofrezca |

Vaultwarden no es de Bitwarden Inc.; usá los clientes oficiales y mantené actualizada la imagen del servidor.

## Recomendaciones

- **Los navegadores no deberían recordar contraseñas.** Desactivá el guardado y autocompletado de contraseñas del navegador y dejá que lo haga el gestor. Si un navegador guarda alguna, protegé esa cuenta con segundo factor, bloqueá el equipo y cifrá su disco.
- **Usá segundo factor en todo lo que lo ofrezca**, mejor llaves físicas o una app autenticadora que SMS.
- **Guardá los secretos raíz en papel**, en dos lugares que no dependan uno del otro, y comprobá que podés leerlos.
- **Nunca pongas secretos en chats, tickets, notas, capturas, repositorios ni en la memoria de un asistente de IA.**
- **Separá las cuentas propietarias de las de operación**, y dale a cada automatización el menor token que necesite.
- La lista completa está en [seguridad](security.md); el camino de regreso está en [recuperación](recovery.md).
