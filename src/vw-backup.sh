#!/usr/bin/env bash
# Snapshot -> encrypt (GnuPG symmetric, AES-256) -> verify by decrypting -> checksum -> rotate -> optional send.
# The passphrase is read from a file readable only by the backup user. It is a SEPARATE secret from the vault's
# master password. Output: $VW_BACKUP_OUT/vault-<UTC timestamp>.tar.gpg and .sha256
. "$(dirname "$0")/vw-common.sh"
: "${VW_BACKUP_OUT:?set VW_BACKUP_OUT}"; : "${VW_PASSPHRASE_FILE:?set VW_PASSPHRASE_FILE}"
[ -s "$VW_PASSPHRASE_FILE" ] || die "passphrase file is missing or empty"
[ "$(stat -c %a "$VW_PASSPHRASE_FILE")" = "600" ] || die "passphrase file must be mode 600"
mkdir -p "$VW_BACKUP_OUT"; chmod 700 "$VW_BACKUP_OUT"
LABEL=$(date -u +%Y%m%d-%H%M%S)
OUT="$VW_BACKUP_OUT/vault-$LABEL.tar.gpg"; TMP="$OUT.partial"; trap 'rm -f "$TMP"' EXIT

"$(dirname "$0")/vw-snapshot.sh" \
  | gpg --batch --yes --quiet --symmetric --cipher-algo AES256 --s2k-mode 3 --s2k-count 65011712 \
        --passphrase-file "$VW_PASSPHRASE_FILE" -o "$TMP"

# Verification: the archive must decrypt with the passphrase and the database must pass its integrity check.
V=$(mktemp -d); trap 'rm -rf "$V"; rm -f "$TMP"' EXIT
gpg --batch --quiet --decrypt --passphrase-file "$VW_PASSPHRASE_FILE" "$TMP" | tar -C "$V" -xf -
read -r OK USERS ITEMS < <(db_summary "$V/db.sqlite3")
[ "$OK" = "ok" ] || die "integrity check failed on the new backup"

mv "$TMP" "$OUT"; trap - EXIT; rm -rf "$V"
( cd "$VW_BACKUP_OUT" && sha256sum "$(basename "$OUT")" > "vault-$LABEL.sha256" )
ls -1t "$VW_BACKUP_OUT"/vault-*.tar.gpg | tail -n +$((VW_KEEP + 1)) | while read -r old; do rm -f "$old" "${old%.tar.gpg}.sha256"; done
echo "backup ok: $(basename "$OUT") ($(du -h "$OUT" | cut -f1)), users=$USERS items=$ITEMS"
[ -n "${VW_REMOTE:-}" ] && "$(dirname "$0")/vw-send.sh" "$OUT"
if [ -n "${VW_COPY_DIR:-}${VW_RCLONE_REMOTE:-}" ]; then "$(dirname "$0")/vw-copy.sh" "$OUT" || echo "warning: the extra copy failed" >&2; fi
exit 0
