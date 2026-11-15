#!/usr/bin/env bash
# Restores an encrypted backup into the data directory of the STANDBY (or a rebuilt) server and starts it.
# The passphrase is typed on a real terminal (ssh -t) and is never stored. The previous data is kept (last 3 copies).
#   vw-restore.sh --list | --status | --start | --stop | --wipe-db | [backup-file]
. "$(dirname "$0")/vw-common.sh"
: "${VW_BACKUP_IN:?set VW_BACKUP_IN (where the encrypted backups are)}"
COMPOSE_DIR="${VW_COMPOSE_DIR:-}"
dc() { [ -n "$COMPOSE_DIR" ] && [ -z "${VW_NO_DOCKER:-}" ] && (cd "$COMPOSE_DIR" && docker compose "$@"); return 0; }

case "${1:-}" in
  --list)   ls -1t "$VW_BACKUP_IN"/vault-*.tar.gpg | xargs -n1 basename; exit 0 ;;
  --status) [ -f "$VW_DATA_DIR/db.sqlite3" ] && { read -r a b c < <(db_summary "$VW_DATA_DIR/db.sqlite3"); echo "data present: integrity=$a users=$b items=$c"; } || echo "no restored data"; exit 0 ;;
  --start)  [ -f "$VW_DATA_DIR/db.sqlite3" ] || die "no restored data: restore first"; dc up -d; echo "standby started with the data it already has"; exit 0 ;;
  --stop)   dc down; echo "standby stopped (data stays on disk)"; exit 0 ;;
  --wipe-db)
    [ -t 0 ] || die "a real terminal is required"
    read -rp "Type WIPE to remove the restored database and its previous copies: " R
    [ "$R" = "WIPE" ] || { echo "cancelled"; exit 0; }
    dc down; rm -rf "$VW_DATA_DIR" "$VW_DATA_DIR".prev-*; install -d -m 700 "$VW_DATA_DIR"
    echo "restored data removed; encrypted backups are untouched"; exit 0 ;;
esac

FILE="${1:-$(ls -1t "$VW_BACKUP_IN"/vault-*.tar.gpg | head -n1)}"
[ -f "$FILE" ] || FILE="$VW_BACKUP_IN/$FILE"; [ -f "$FILE" ] || die "backup not found"
SUM="${FILE%.tar.gpg}.sha256"
[ -f "$SUM" ] && (cd "$(dirname "$FILE")" && sha256sum -c --quiet "$(basename "$SUM")") || die "checksum missing or wrong: the file is damaged or was altered"

if [ -n "${VW_ALLOW_PASSPHRASE_FILE:-}" ] && [ -r "${VW_PASSPHRASE_FILE:-}" ]; then   # tests only
  PASS_ARGS=(--passphrase-file "$VW_PASSPHRASE_FILE")
else
  [ -t 0 ] || die "a real terminal is required to type the passphrase (use ssh -t)"
  IFS= read -r -s -p "Backup passphrase (not shown): " P; echo
  PASS_ARGS=(--passphrase-fd 3)
fi
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
if [ "${PASS_ARGS[0]}" = "--passphrase-fd" ]; then
  gpg --batch --quiet --decrypt "${PASS_ARGS[@]}" "$FILE" 3<<<"$P" | tar -C "$T" -xf - || die "wrong passphrase or damaged file"
else
  gpg --batch --quiet --decrypt "${PASS_ARGS[@]}" "$FILE" | tar -C "$T" -xf - || die "wrong passphrase or damaged file"
fi
unset P
read -r OK USERS ITEMS < <(db_summary "$T/db.sqlite3"); [ "$OK" = "ok" ] || die "restored database failed its integrity check"
echo "backup: $(basename "$FILE")  integrity=$OK  users=$USERS  items=$ITEMS"
if [ -z "${VW_ALLOW_PASSPHRASE_FILE:-}" ]; then read -rp "Type YES to replace the data of this server: " R; [ "$R" = "YES" ] || { echo "cancelled"; exit 0; }; fi

dc down
if [ -d "$VW_DATA_DIR" ]; then mv "$VW_DATA_DIR" "$VW_DATA_DIR.prev-$(date -u +%Y%m%d-%H%M%S)"; fi
{ ls -1dt "$VW_DATA_DIR".prev-* 2>/dev/null || true; } | tail -n +4 | xargs -r rm -rf
install -d -m 700 "$VW_DATA_DIR"; cp -a "$T"/. "$VW_DATA_DIR"/; echo "$(basename "$FILE")" > "$VW_DATA_DIR/.restored-from"
dc up -d
echo "restored and started: $USERS user(s), $ITEMS item(s). Sign in with the master password and second factor."
