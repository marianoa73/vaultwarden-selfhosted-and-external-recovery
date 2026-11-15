#!/usr/bin/env bash
# Sends an ALREADY ENCRYPTED backup to the remote host over SSH. The key used here is restricted on the remote side
# to one forced command (see src/vw-receive.sh and examples/authorized_keys.example): it cannot open a shell.
. "$(dirname "$0")/vw-common.sh"
: "${VW_REMOTE:?set VW_REMOTE (ssh alias of the receiver)}"
FILE="${1:?usage: vw-send.sh <file.tar.gpg>}"
[[ "$(basename "$FILE")" =~ ^vault-([0-9]{8}-[0-9]{6})\.tar\.gpg$ ]] || die "unexpected file name"
LABEL="${BASH_REMATCH[1]}"
ssh -o BatchMode=yes -o ConnectTimeout=20 "$VW_REMOTE" "$LABEL" < "$FILE"
