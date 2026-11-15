#!/usr/bin/env bash
# Writes a CONSISTENT snapshot of the Vaultwarden data as a tar stream on stdout.
# The database is copied with SQLite's backup API, so the server can keep running.
. "$(dirname "$0")/vw-common.sh"
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
python3 - "$VW_DATA_DIR/db.sqlite3" "$T/db.sqlite3" <<'PY'
import sqlite3, sys
src = sqlite3.connect(sys.argv[1]); dst = sqlite3.connect(sys.argv[2]); src.backup(dst); dst.close(); src.close()
PY
for f in rsa_key.pem config.json; do [ -e "$VW_DATA_DIR/$f" ] && cp -a "$VW_DATA_DIR/$f" "$T/"; done
for d in attachments sends; do [ -d "$VW_DATA_DIR/$d" ] && cp -a "$VW_DATA_DIR/$d" "$T/"; done
tar -C "$T" -cf - .
