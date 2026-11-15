#!/usr/bin/env bash
# Copies an ALREADY ENCRYPTED backup to extra destinations, besides the SSH receiver:
#   VW_COPY_DIR       a mounted directory (external disk, NAS share, second machine)
#   VW_RCLONE_REMOTE  an rclone remote and folder (cloud drive, object storage, SFTP, WebDAV...), e.g. mydrive:vault-backups
# It refuses any file that is not GnuPG-encrypted, so nothing readable can ever leave the machine. The passphrase is never
# sent: it lives apart, on paper. Each destination keeps the last VW_KEEP copies.
. "$(dirname "$0")/vw-common.sh"
FILE="${1:?usage: vw-copy.sh <file.tar.gpg>}"
[[ "$(basename "$FILE")" =~ ^vault-[0-9]{8}-[0-9]{6}\.tar\.gpg$ ]] || die "unexpected file name"
PK=$(gpg --batch --pinentry-mode cancel --list-packets "$FILE" 2>/dev/null || true)
grep -qE ":(symkey|pubkey) enc packet:" <<<"$PK" || die "refusing to copy a file that is not GnuPG-encrypted"
SUM="${FILE%.tar.gpg}.sha256"; NAME="$(basename "$FILE")"; DONE=0

if [ -n "${VW_COPY_DIR:-}" ]; then
  mkdir -p "$VW_COPY_DIR"; chmod 700 "$VW_COPY_DIR"
  cp "$FILE" "$VW_COPY_DIR/"; [ -f "$SUM" ] && cp "$SUM" "$VW_COPY_DIR/"
  ( cd "$VW_COPY_DIR" && sha256sum -c --quiet "${NAME%.tar.gpg}.sha256" ) || die "copy in $VW_COPY_DIR does not match its checksum"
  ls -1t "$VW_COPY_DIR"/vault-*.tar.gpg | tail -n +$((VW_KEEP + 1)) | while read -r old; do rm -f "$old" "${old%.tar.gpg}.sha256"; done
  echo "copy ok: directory"; DONE=1
fi

if [ -n "${VW_RCLONE_REMOTE:-}" ]; then
  command -v rclone >/dev/null || die "rclone is not installed"
  rclone copy "$FILE" "$VW_RCLONE_REMOTE" --checksum; [ -f "$SUM" ] && rclone copy "$SUM" "$VW_RCLONE_REMOTE" --checksum
  rclone check "$(dirname "$FILE")" "$VW_RCLONE_REMOTE" --one-way --include "$NAME" >/dev/null 2>&1 || die "remote copy does not match"
  rclone lsf "$VW_RCLONE_REMOTE" --include 'vault-*.tar.gpg' | sort -r | tail -n +$((VW_KEEP + 1)) | while read -r old; do
    rclone deletefile "$VW_RCLONE_REMOTE/$old"; rclone deletefile "$VW_RCLONE_REMOTE/${old%.tar.gpg}.sha256" 2>/dev/null || true
  done
  echo "copy ok: rclone remote"; DONE=1
fi
[ "$DONE" = 1 ] || die "set VW_COPY_DIR and/or VW_RCLONE_REMOTE"
