# Installing the local server

[Versión en español](install.md)

## Prerequisites

A small Linux machine with Docker and Compose, a mesh VPN joined by that machine and by your devices, and a user for the backups. Nothing here needs a public address. All names below are placeholders.

## 1. Create the server

Copy `examples/compose.primary.yml`, set your private domain and the image digest you verified, and start it:

```bash
mkdir -p /path/to/vaultwarden/data && cd /path/to/vaultwarden
cp /path/to/repo/examples/compose.primary.yml compose.yml
docker compose up -d
```

## 2. Publish it on the private network only

Publish the loopback port through your mesh VPN's HTTPS feature or a reverse proxy that listens only on the private interface. Check from a device that is **not** on the private network that the address does not answer.

## 3. Create accounts, then close sign-ups

Sign-ups are closed by default: open them only for the minute needed, create your account (and the emergency contact's, see [emergency access](emergency-access.en.md)), then close them again:

```bash
sed -i 's/SIGNUPS_ALLOWED: "false"/SIGNUPS_ALLOWED: "true"/' compose.yml && docker compose up -d   # open
# ... create the accounts ...
sed -i 's/SIGNUPS_ALLOWED: "true"/SIGNUPS_ALLOWED: "false"/' compose.yml && docker compose up -d   # close
```

## 4. Harden the account

1. Choose a long master password you can memorise.
2. In the web vault, raise the key derivation to Argon2id with stronger parameters.
3. Enable the authenticator app and register two hardware keys; print the recovery code.
4. Install the official clients on your devices and point them at your private address.
5. Turn off password saving in every browser.

## 5. Verify

Create a test item, lock and unlock from a second device, and confirm that the admin page is off. Then continue with [backup](backup.en.md).
