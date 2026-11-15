<p align="center"><img src="docs/assets/banner.en.png?v=1" alt="Vaultwarden Self-Hosted and External Recovery" width="100%"></p>

<p align="center">
<a href="README.es.md"><img src="docs/assets/btn-es.svg" height="44" alt="Ver en Español"></a>
&nbsp;
<a href="https://marianoa73.github.io/vaultwarden-selfhosted-and-external-recovery/"><img src="docs/assets/btn-site-en.svg" height="44" alt="Interactive page (EN / ES)"></a>
</p>

> *One place for every key: a self-hosted vault, an encrypted off-site copy and a contingency that has been tried.*

**How to secure and control the credentials of websites, social networks, publications, hosting and AI services with a self-hosted password vault, a second factor, an encrypted copy on a remote server, a standby that switches on only in an emergency, and a view-only emergency contact.**

Author: Mariano Araujo · MIT License · [Versión en español](README.es.md)

## In one minute

1. **Problem:** many projects mean many keys; they get reused, saved in browsers or lost.
2. **Decision:** three tiers: root secrets on paper, daily credentials in a password manager, machine secrets in the manager with small scope.
3. **What it includes:** the design, an install guide, backup and restore scripts with tests, the contingency procedure, emergency access, a security checklist and diagrams.
4. **Agnostic by design:** no names, addresses, domains, ports or paths of any real setup, and no statement of where each secret is kept.
5. **Verify the backup chain without Vaultwarden, Docker or a network:**
   ```bash
   bash tests/test_backup_restore.sh
   python3 -m unittest discover -s tests -v
   ```

![Overview](docs/assets/01-overview.en.svg?v=1)

[High-resolution PNG](docs/assets/01-overview.en.png?v=1) · [Versión en español](README.es.md)

## Why this project

It was created to **secure and control all the keys** of the websites, social accounts, publications, hosting, servers and AI services that one person runs. Use this model or a similar one; the alternatives (other password managers, authenticator apps from Google or Microsoft, open-source authenticators, hardware keys) are compared in [docs/why.en.md](docs/why.en.md).

The rule that makes it work: **paper for the few keys that open everything, the manager for the many you use daily**, so nothing has to be retyped or managed one by one. Browsers should not remember passwords; if one does, its account needs a second factor.

## How it is built

![Encryption layers](docs/assets/02-encryption.en.svg?v=1)

Four independent layers: client-side vault encryption, a second factor, a separately encrypted and verified backup, and a restricted transport. Details in [docs/security.en.md](docs/security.en.md).

## Backup and off-site copy

![Nightly backup](docs/assets/03-backup.en.svg?v=1)

Every night: snapshot, encrypt, verify by decrypting, checksum, rotate, send. The remote host stores the files but never has the passphrase. See [docs/backup.en.md](docs/backup.en.md). The server and the standby can be a virtual machine, a VPS or a local machine, and the encrypted copy can also go to a cloud drive, an external disk or another safe place: see [docs/options.en.md](docs/options.en.md).

## Contingency

![Contingency activation](docs/assets/04-contingency.en.svg?v=1)

A person types the passphrase on a real terminal; the archive is checked and counted before anything is replaced. See [docs/recovery.en.md](docs/recovery.en.md).

## Keys and emergency access

![Keys needed](docs/assets/05-keys.en.svg?v=1)

![Emergency access](docs/assets/06-emergency.en.svg?v=1)

Which secrets are needed to recover and what happens without them, plus a second, view-only account that opens after a waiting time: [docs/emergency-access.en.md](docs/emergency-access.en.md).

## Security recommendations in brief

- Long memorised master password, Argon2id raised, authenticator app plus two hardware keys, recovery codes on paper.
- Sign-ups closed, admin page off, loopback only behind a private network, image pinned by digest.
- Keys-only SSH, one dedicated key with one forced command, remote host with no route to your home network.
- Encrypted, verified backups with their own passphrase; a restore rehearsal every quarter.
- Browsers do not save passwords; no secrets in chat, notes, repositories or assistants.

## Deploy with an AI assistant

The repository includes an agent guide, [skill/vaultwarden-recovery-deploy/SKILL.md](skill/vaultwarden-recovery-deploy/SKILL.md), that an AI assistant can read to deploy this design for you on **Linux or Windows (through WSL2)**. It asks before every change, runs the checks, and **never sees your secrets**: you type the master password and generate the backup passphrase yourself. [AGENTS.md](AGENTS.md) points other agents to it.

## Contributors

The author, with Claude, Codex and OpenRouter/OpenCode as AI assistants under human review. See [CONTRIBUTORS.md](CONTRIBUTORS.md).

## Documentation

| Guide | English | Español |
|---|---|---|
| Why and alternatives | [why.en.md](docs/why.en.md) | [why.md](docs/why.md) |
| Architecture and software | [architecture.en.md](docs/architecture.en.md) | [architecture.md](docs/architecture.md) |
| Installing the local server | [install.en.md](docs/install.en.md) | [install.md](docs/install.md) |
| Security model and checklist | [security.en.md](docs/security.en.md) | [security.md](docs/security.md) |
| Local and remote backup | [backup.en.md](docs/backup.en.md) | [backup.md](docs/backup.md) |
| Hosting, destinations and encryption options (VM, VPS, local, cloud drive) | [options.en.md](docs/options.en.md) | [options.md](docs/options.md) |
| Recovery and contingency | [recovery.en.md](docs/recovery.en.md) | [recovery.md](docs/recovery.md) |
| Emergency access | [emergency-access.en.md](docs/emergency-access.en.md) | [emergency-access.md](docs/emergency-access.md) |
| Limitations | [limitations.en.md](docs/limitations.en.md) | [limitations.md](docs/limitations.md) |

Related: [ai-split-raspberry-pi](https://github.com/marianoa73/ai-split-raspberry-pi) · [ai-video-edit-and-shorts](https://github.com/marianoa73/ai-video-edit-and-shorts).
