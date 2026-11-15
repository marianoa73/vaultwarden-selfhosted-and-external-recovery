#!/usr/bin/env bash
# Runs on the REMOTE host as the forced command of a dedicated SSH key. Receives one encrypted backup on stdin.
# It never sees the passphrase and cannot decrypt anything. Keeps the last $KEEP copies with their checksums.
set -euo pipefail
umask 077
DIR="${VW_REMOTE_DIR:?set VW_REMOTE_DIR}"; KEEP="${VW_KEEP:-14}"
LABEL="${SSH_ORIGINAL_COMMAND:-}"
[[ "$LABEL" =~ ^[0-9]{8}-[0-9]{6}$ ]] || { echo "invalid label" >&2; exit 2; }
TMP="$DIR/.receiving-$LABEL"; trap 'rm -f "$TMP"' EXIT
cat > "$TMP"
[ "$(stat -c %s "$TMP")" -gt "${VW_MIN_BYTES:-5000}" ] || { echo "file too small" >&2; exit 3; }
PK=$(head -c 65536 "$TMP" | gpg --batch --list-packets 2>/dev/null || true)
[[ "$PK" == *"symkey enc packet"* ]] || { echo "not a passphrase-encrypted GnuPG file" >&2; exit 4; }
DEST="$DIR/vault-$LABEL.tar.gpg"; mv "$TMP" "$DEST"; trap - EXIT
( cd "$DIR" && sha256sum "$(basename "$DEST")" > "vault-$LABEL.sha256" )
ls -1t "$DIR"/vault-*.tar.gpg | tail -n +$((KEEP + 1)) | while read -r old; do rm -f "$old" "${old%.tar.gpg}.sha256"; done
echo "received $(basename "$DEST")"
