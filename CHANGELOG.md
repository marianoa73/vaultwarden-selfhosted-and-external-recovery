# Changelog

## 0.2.0

- New guide on hosting, backup destinations and encryption options (English and Spanish): server and standby as a physical machine, a virtual machine, a VPS or a local machine; encrypted copies to a cloud drive, object storage, external disk, NAS or SFTP; highest-level encryption and a public-key variant; where the passphrase lives (paper, two places, never beside the archives or inside the vault); disaster-recovery levels and a checklist.
- `src/vw-copy.sh`: copies the already encrypted archive to a mounted directory (`VW_COPY_DIR`) and/or an rclone remote (`VW_RCLONE_REMOTE`), verifies the copy, rotates, and refuses any file that is not GnuPG-encrypted. Wired into `vw-backup.sh`, covered by the test suite.

## 0.1.0

- Design of a self-hosted password vault with an encrypted off-site copy, a switched-off standby and a view-only emergency contact.
- Reference scripts for snapshot, encrypted backup, restricted receiver, send and restore, with an end-to-end test on a fake vault.
- Bilingual documentation (English and Spanish): why and alternatives, architecture and software, install, security checklist, backup, recovery, emergency access and limitations.
- Agent guide (`skill/vaultwarden-recovery-deploy`) and `AGENTS.md` to deploy the design on Linux or Windows (WSL2) without the agent ever seeing a secret; `src/vw-init-passphrase.sh` refuses to run without a real terminal.
- Six diagrams in both languages and an interactive page with an EN / ES switch.
