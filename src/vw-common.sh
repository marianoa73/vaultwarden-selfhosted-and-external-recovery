#!/usr/bin/env bash
# Shared settings and helpers. Every path comes from the environment: nothing is hard-coded.
# Copy examples/vw.env.example to /etc/vw-recovery.env (mode 600) and adapt it.
set -euo pipefail
umask 077
[ -r "${VW_ENV:-/etc/vw-recovery.env}" ] && . "${VW_ENV:-/etc/vw-recovery.env}"
: "${VW_DATA_DIR:?set VW_DATA_DIR (the Vaultwarden data directory)}"
VW_KEEP="${VW_KEEP:-14}"

die() { echo "error: $*" >&2; exit 1; }

# Prints "integrity users items" for a SQLite file, read-only.
db_summary() {
  python3 - "$1" <<'PY'
import sqlite3, sys
c = sqlite3.connect(f"file:{sys.argv[1]}?mode=ro", uri=True)
ok = c.execute("pragma integrity_check").fetchone()[0]
users = c.execute("select count(*) from users").fetchone()[0]
items = c.execute("select count(*) from ciphers").fetchone()[0]
print(ok, users, items)
PY
}
