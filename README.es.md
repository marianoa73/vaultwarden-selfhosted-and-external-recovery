<p align="center"><img src="docs/assets/banner.es.png?v=1" alt="Vaultwarden Self-Hosted y Recuperación Externa" width="100%"></p>

<p align="center">
<a href="README.md"><img src="docs/assets/btn-en.svg" height="44" alt="View in English"></a>
&nbsp;
<a href="https://marianoa73.github.io/vaultwarden-selfhosted-and-external-recovery/?lang=es"><img src="docs/assets/btn-site-es.svg" height="44" alt="Página interactiva (ES / EN)"></a>
</p>

> *Un solo lugar para todas las claves: bóveda propia, copia cifrada fuera de sitio y una contingencia probada.*

**Cómo asegurar y controlar las credenciales de sitios web, redes sociales, publicaciones, hosting y servicios de IA con una bóveda de contraseñas propia, segundo factor, una copia cifrada en un servidor remoto, un respaldo que se enciende sólo en una emergencia y un contacto de emergencia de sólo lectura.**

Autor: Mariano Araujo · Licencia MIT · [English version](README.md)

## En un minuto

1. **Problema:** muchos proyectos son muchas claves; se repiten, se guardan en los navegadores o se pierden.
2. **Decisión:** tres niveles: secretos raíz en papel, credenciales diarias en un gestor de contraseñas, secretos de máquina en el gestor con poco alcance.
3. **Qué incluye:** el diseño, una guía de instalación, scripts de backup y restauración con pruebas, el procedimiento de contingencia, el acceso de emergencia, una lista de seguridad y diagramas.
4. **Agnóstico por diseño:** sin nombres, direcciones, dominios, puertos ni rutas de ninguna instalación real, y sin decir dónde se guarda cada secreto.
5. **Verificar la cadena de backup sin Vaultwarden, Docker ni red:**
   ```bash
   bash tests/test_backup_restore.sh
   python3 -m unittest discover -s tests -v
   ```

![Vista general](docs/assets/01-overview.es.svg?v=1)

[PNG en alta resolución](docs/assets/01-overview.es.png?v=1) · [English version](README.md)

## Por qué este proyecto

Nació para **asegurar y controlar todas las claves** de los sitios web, cuentas sociales, publicaciones, hosting, servidores y servicios de IA que administra una persona. Usá este modelo u otro parecido; las alternativas (otros gestores de contraseñas, apps autenticadoras de Google o Microsoft, autenticadores de código abierto, llaves físicas) se comparan en [docs/why.md](docs/why.md).

La regla que lo hace funcionar: **papel para las pocas claves que abren todo, el gestor para las muchas que se usan a diario**, así no hay que retipear ni gestionar nada una por una. Los navegadores no deberían recordar contraseñas; si alguno lo hace, su cuenta necesita segundo factor.

## Cómo está construido

![Capas de cifrado](docs/assets/02-encryption.es.svg?v=1)

Cuatro capas independientes: cifrado de la bóveda en el cliente, un segundo factor, un backup cifrado y verificado por separado y un transporte restringido. Detalle en [docs/security.md](docs/security.md).

## Backup y copia fuera de sitio

![Backup nocturno](docs/assets/03-backup.es.svg?v=1)

Cada noche: foto, cifrado, verificación descifrando, hash, rotación y envío. El host remoto guarda los archivos pero nunca tiene la frase. Ver [docs/backup.md](docs/backup.md).

## Contingencia

![Activación de la contingencia](docs/assets/04-contingency.es.svg?v=1)

Una persona tipea la frase en una terminal real; el archivo se verifica y se cuenta antes de reemplazar nada. Ver [docs/recovery.md](docs/recovery.md).

## Claves y acceso de emergencia

![Claves necesarias](docs/assets/05-keys.es.svg?v=1)

![Acceso de emergencia](docs/assets/06-emergency.es.svg?v=1)

Qué secretos hacen falta para recuperar y qué pasa sin ellos, más una segunda cuenta de sólo lectura que se abre tras un tiempo de espera: [docs/emergency-access.md](docs/emergency-access.md).

## Recomendaciones de seguridad en breve

- Contraseña maestra larga y memorizada, Argon2id elevado, app autenticadora más dos llaves físicas, códigos de recuperación en papel.
- Registro cerrado, página de administración apagada, sólo loopback detrás de una red privada, imagen anclada por hash.
- SSH sólo con llaves, una clave dedicada con un comando forzado, host remoto sin ruta a tu red de casa.
- Backups cifrados y verificados con su propia frase; un ensayo de restauración cada trimestre.
- Los navegadores no guardan contraseñas; ningún secreto en chats, notas, repositorios ni asistentes.

## Desplegar con un asistente de IA

El repositorio incluye una guía para agentes, [skill/vaultwarden-recovery-deploy/SKILL.md](skill/vaultwarden-recovery-deploy/SKILL.md), que un asistente de IA puede leer para desplegar este diseño por vos en **Linux o Windows (con WSL2)**. Pregunta antes de cada cambio, corre las verificaciones y **nunca ve tus secretos**: la contraseña maestra la escribís vos y la frase del backup la generás vos. [AGENTS.md](AGENTS.md) lleva a otros agentes hasta ella.

## Colaboradores

El autor, con Claude, Codex y OpenRouter/OpenCode como asistentes de IA bajo revisión humana. Ver [CONTRIBUTORS.md](CONTRIBUTORS.md).

## Documentación

| Guía | English | Español |
|---|---|---|
| Por qué y alternativas | [why.en.md](docs/why.en.md) | [why.md](docs/why.md) |
| Arquitectura y software | [architecture.en.md](docs/architecture.en.md) | [architecture.md](docs/architecture.md) |
| Instalación del servidor local | [install.en.md](docs/install.en.md) | [install.md](docs/install.md) |
| Modelo de seguridad y lista de control | [security.en.md](docs/security.en.md) | [security.md](docs/security.md) |
| Backup local y remoto | [backup.en.md](docs/backup.en.md) | [backup.md](docs/backup.md) |
| Recuperación y contingencia | [recovery.en.md](docs/recovery.en.md) | [recovery.md](docs/recovery.md) |
| Acceso de emergencia | [emergency-access.en.md](docs/emergency-access.en.md) | [emergency-access.md](docs/emergency-access.md) |
| Limitaciones | [limitations.en.md](docs/limitations.en.md) | [limitations.md](docs/limitations.md) |

Relacionados: [ai-split-raspberry-pi](https://github.com/marianoa73/ai-split-raspberry-pi) · [ai-video-edit-and-shorts](https://github.com/marianoa73/ai-video-edit-and-shorts).
