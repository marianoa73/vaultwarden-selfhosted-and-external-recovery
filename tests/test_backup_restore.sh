#!/usr/bin/env bash
# End-to-end test with a FAKE vault (a SQLite file with the two tables the scripts read). No Vaultwarden, no Docker,
# no network: it proves the encrypt -> verify -> rotate -> checksum -> restore chain and the tamper checks.
set -euo pipefail
R="$(cd "$(dirname "$0")/.." && pwd)"; T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
export VW_ENV=/nonexistent VW_DATA_DIR="$T/data" VW_BACKUP_OUT="$T/out" VW_BACKUP_IN="$T/out" VW_PASSPHRASE_FILE="$T/pass" VW_KEEP=3 VW_NO_DOCKER=1 VW_ALLOW_PASSPHRASE_FILE=1
mkdir -p "$VW_DATA_DIR/attachments"; echo "fake attachment" > "$VW_DATA_DIR/attachments/a.bin"; echo fakepem > "$VW_DATA_DIR/rsa_key.pem"
python3 - "$VW_DATA_DIR/db.sqlite3" <<'PY'
import sqlite3, sys
c = sqlite3.connect(sys.argv[1]); c.execute("create table users(id text)"); c.execute("create table ciphers(id text, updated_at text)")
c.execute("insert into users values('u1')"); [c.execute("insert into ciphers values(?, '2026-01-01')", (str(i),)) for i in range(5)]; c.commit()
PY
printf 'correct horse battery staple test only' > "$T/pass"; chmod 600 "$T/pass"
fail() { echo "FAIL: $*"; exit 1; }

# 1. the passphrase file must be private
chmod 644 "$T/pass"; "$R/src/vw-backup.sh" >/dev/null 2>&1 && fail "accepted a world-readable passphrase file"; chmod 600 "$T/pass"

# 2. backups, rotation to 3 copies, checksums
for i in 1 2 3 4 5; do sleep 1; "$R/src/vw-backup.sh" > "$T/log"; done
grep -q "users=1 items=5" "$T/log" || fail "summary missing"
[ "$(ls "$T/out"/vault-*.tar.gpg | wc -l)" = 3 ] || fail "rotation did not keep 3"
[ "$(ls "$T/out"/vault-*.sha256 | wc -l)" = 3 ] || fail "checksums not rotated"

# 3. the archive is encrypted: no readable content
! gpg --batch --quiet --decrypt --passphrase "wrong" "$(ls -1t "$T/out"/vault-*.tar.gpg | head -1)" >/dev/null 2>&1 || fail "decrypted with a wrong passphrase"
! grep -aq "fake attachment" "$(ls -1t "$T/out"/vault-*.tar.gpg | head -1)" || fail "plaintext leaked into the archive"

# 4. restore into a fresh data directory
rm -rf "$VW_DATA_DIR"; "$R/src/vw-restore.sh" > "$T/restore.log" || { cat "$T/restore.log"; fail "restore failed"; }
grep -q "1 user(s), 5 item(s)" "$T/restore.log" || fail "restore summary wrong"
[ "$(cat "$VW_DATA_DIR/attachments/a.bin")" = "fake attachment" ] || fail "attachment not restored"
"$R/src/vw-restore.sh" --status | grep -q "users=1 items=5" || fail "status wrong"

# 5. previous data is kept and limited to 3 copies
for i in 1 2 3 4 5; do sleep 1; "$R/src/vw-restore.sh" >/dev/null; done
[ "$(ls -d "$VW_DATA_DIR".prev-* | wc -l)" = 3 ] || fail "prev copies not limited to 3"

# 6. a damaged or altered file is refused
F=$(ls -1t "$T/out"/vault-*.tar.gpg | head -1); python3 - "$F" <<'PY'
import sys
p = sys.argv[1]; b = bytearray(open(p, "rb").read()); b[100] ^= 0xFF; open(p, "wb").write(b)
PY
sha256sum -c --quiet "${F%.tar.gpg}.sha256" >/dev/null 2>&1 && fail "test setup: tamper did not change the file"
"$R/src/vw-restore.sh" "$F" >/dev/null 2>&1 && fail "restored a tampered file"

# 7. the receiver accepts only valid labels and passphrase-encrypted files
export VW_MIN_BYTES=100 VW_REMOTE_DIR="$T/remote"; mkdir -p "$VW_REMOTE_DIR"
GOOD=$(ls -1t "$T/out"/vault-*.tar.gpg | sed -n 2p)
SSH_ORIGINAL_COMMAND="20260101-000000" "$R/src/vw-receive.sh" < "$GOOD" >/dev/null || fail "receiver refused a valid backup"
SSH_ORIGINAL_COMMAND="../../etc" "$R/src/vw-receive.sh" < "$GOOD" >/dev/null 2>&1 && fail "receiver accepted a path in the label"
head -c 20000 /dev/urandom > "$T/junk"; SSH_ORIGINAL_COMMAND="20260102-000000" "$R/src/vw-receive.sh" < "$T/junk" >/dev/null 2>&1 && fail "receiver accepted a non-GnuPG file"
[ -f "$VW_REMOTE_DIR/vault-20260101-000000.sha256" ] || fail "receiver did not write the checksum"
echo "OK: backup, rotation, encryption, restore, tamper checks and receiver"
