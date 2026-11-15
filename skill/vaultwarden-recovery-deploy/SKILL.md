---
name: vaultwarden-recovery-deploy
description: Deploy this repository's design for a user, on Linux or Windows (through WSL2): a self-hosted Vaultwarden password vault, an encrypted nightly backup to a remote server, a switched-off standby and view-only emergency access. Use when someone asks to set up, install or recover their own password vault with off-site backup. Never handles the user's secrets.
---

# Deploy Vaultwarden with an encrypted off-site copy (agent guide)

You are setting this up **for a person, on their machines**. Read the whole file before touching anything. The design and
reasons are in `docs/` (start with `docs/why.en.md`, `docs/security.en.md`); the scripts are in `src/`, the templates in `examples/`.

## Rules that never bend

1. **You never see, ask for, print, store or send a secret**: master password, second-factor codes, backup passphrase,
   recovery codes, private keys, tokens. The person types or generates each one on their own terminal. Do not use
   `echo`, `cat` or logs on any file that may contain one. If one appears in your context by mistake, tell the person and
   suggest rotating it.
2. **Ask before each step that changes something** (install, open sign-ups, create a key, edit the remote host, enable a timer).
   Show the exact command and what it does first.
3. **Nothing is exposed to the internet**: the server listens on loopback only, reached through a private network.
4. **Never invent values**: hostnames, addresses, domains and paths come from the person. Keep them in the private
   environment file, never in this repository.
5. **Stop and report** if a check fails. Do not work around a failed verification.

## Step 0: learn the situation

Ask, one short question at a time:
- Operating system of the machine that will host the vault: **Linux**, **Windows**, or macOS.
- Where should the encrypted copies go besides the remote server: a **cloud drive, external disk or NAS** (see `docs/options.en.md`)? The person creates the account and the `rclone` login; you only set `VW_COPY_DIR` / `VW_RCLONE_REMOTE`. The passphrase never goes to the same place as the archives.
- Is there a **second, remote Linux server** (a small VPS) for the encrypted copies? Who administers it?
- Is a **private mesh VPN** (Tailscale, Headscale, WireGuard) already in use, or should it be set up first?
- Does the person already have a **second factor** (authenticator app, hardware keys) and **paper** for the root secrets?
- Is there someone they trust as an **emergency contact**?

Detect the system yourself: `uname -a` on Linux/WSL, `systeminfo` or `wsl -l -v` on Windows. Confirm `docker --version`,
`docker compose version`, `python3 --version`, `gpg --version`, `ssh -V`.

## Step 1: platform preparation

**Linux**: Docker Engine and the Compose plugin from the distribution or Docker's repository; `gnupg`, `python3`, `openssh-client`;
systemd for the timer.

**Windows**: the scripts are bash, so run everything **inside WSL2 with an Ubuntu distribution**.
1. Check `wsl -l -v` shows the distro on version 2. If not, the person runs `wsl --install -d Ubuntu` in an administrator
   terminal and restarts.
2. Docker: either Docker Desktop with WSL integration enabled for that distro, or Docker Engine installed inside the distro.
3. For the nightly timer, enable systemd in the distro (`/etc/wsl.conf` with `[boot]` and `systemd=true`, then `wsl --shutdown`),
   **or** use Windows Task Scheduler to run `wsl -d Ubuntu -- bash -lc "/path/to/vw-backup.sh"` every night.
4. Keep the repository and data **inside the Linux filesystem** (not under `/mnt/c`): permissions (mode 600) and speed depend on it.
5. The vault is reachable only from the person's private network. The remote receiver must be a **Linux** host.
6. Warn that the laptop must be on at backup time; a desktop or small always-on machine is better.

**macOS**: possible with Docker Desktop, but untested here; say so and proceed only if the person accepts.

## Step 2: the server (`docs/install.en.md`)

1. Copy `examples/compose.primary.yml`; ask for the private domain and have the person pick and verify an image digest
   (`docker pull`, `docker inspect`). Write it in the compose file.
2. Start it, and check `curl -fsS http://127.0.0.1:8222/alive` answers.
3. Publish it **only** on the private network (the mesh VPN's HTTPS feature or a private-interface proxy). Ask the person to
   confirm from a device **outside** that network that the address does **not** answer.
4. Sign-ups are closed by default. Open them **only while the person creates their account** (and the contact's), then close them again and recheck.
5. The person, on their own device: chooses the master password, raises the key derivation to Argon2id, enables the
   authenticator app and registers two hardware keys, prints the recovery codes, and turns off password saving in browsers.

## Step 3: encrypted backup (`docs/backup.en.md`)

1. Create the private environment file from `examples/vw.env.example` (mode 600) with the person's paths.
2. **The person** runs `src/vw-init-passphrase.sh /path/to/backup-passphrase` in their own terminal and writes the passphrase on
   paper (two copies, two places). You do not run it, you do not read the file.
3. Run `bash tests/test_backup_restore.sh` to prove the chain works on this machine.
4. With the person's OK, create a dedicated SSH key, install it on the remote host with `examples/authorized_keys.example`
   (forced command, `restrict`), and set `VW_REMOTE`. Check that the key cannot open a shell.
5. Run one real backup by hand: expect `backup ok` with users and items, an `.sha256` file and the copy on the remote host.
6. Install the timer (`examples/vw-backup.service`, `examples/vw-backup.timer`, or Task Scheduler on Windows) and add the age of
   the last backup to the person's status message.

## Step 4: standby and rehearsal (`docs/recovery.en.md`)

1. On the remote host, place `examples/compose.standby.yml` with the **same pinned image**; leave it **stopped**.
2. Rehearse once with the person at the keyboard: `ssh -t <host> sudo .../vw-restore.sh`, the person types the passphrase and
   YES, signs in to the standby with master password and second factor, then runs `--stop` and `--wipe-db`.
3. Record how long it took. A restore that was never tried does not count as done.

## Step 5: emergency access (`docs/emergency-access.en.md`)

Walk the person through creating the contact's account, adding the contact with *View* access and a waiting time, confirming the
fingerprint, and configuring outgoing mail for notices. Test once with a short waiting time.

## Definition of done

- Vault reachable only through the private network; sign-ups closed; admin page off.
- Second factor with two hardware keys; recovery codes and backup passphrase **on paper in two places**, confirmed by the person.
- One real nightly backup arrived and its checksum matches; the test suite passes.
- A full restore rehearsal succeeded on the standby, which is switched off again.
- Emergency contact configured and tested.
- Browsers do not save passwords. No secret was shown to you.

Tell the person plainly what is done, what is not and what remains theirs (paper copies, hardware keys, the contact).
