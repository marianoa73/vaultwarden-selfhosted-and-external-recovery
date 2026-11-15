#!/usr/bin/env bash
# Creates the backup passphrase file (mode 600) and shows the passphrase ONCE on the terminal, so its owner can
# write it on paper. It refuses to run without a real terminal: if an assistant ran it, the passphrase would end up in
# the assistant's session, or nobody would ever see it. Run it yourself.
set -euo pipefail
umask 077
FILE="${1:-${VW_PASSPHRASE_FILE:-}}"
[ -n "$FILE" ] || { echo "usage: vw-init-passphrase.sh /path/to/backup-passphrase  (or set VW_PASSPHRASE_FILE)" >&2; exit 2; }
[ -t 0 ] && [ -t 1 ] || { echo "error: run this yourself in a real terminal; it never prints the passphrase anywhere else" >&2; exit 1; }
[ ! -e "$FILE" ] || { echo "error: $FILE already exists; it will not be overwritten" >&2; exit 1; }
head -c 48 /dev/urandom | base64 -w0 > "$FILE"; chmod 600 "$FILE"
echo
echo "BACKUP PASSPHRASE (shown once). Write it on paper now, in two copies kept in separate places:"
echo
cat "$FILE"; echo; echo
read -r -p "Press Enter when you have written it down; the screen will be cleared..." _
printf '\033c'
echo "Saved to $FILE (mode 600). It is NOT the vault's master password."
