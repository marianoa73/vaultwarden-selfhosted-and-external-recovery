# Changelog

## 0.1.0

- Design of a self-hosted password vault with an encrypted off-site copy, a switched-off standby and a view-only emergency contact.
- Reference scripts for snapshot, encrypted backup, restricted receiver, send and restore, with an end-to-end test on a fake vault.
- Bilingual documentation (English and Spanish): why and alternatives, architecture and software, install, security checklist, backup, recovery, emergency access and limitations.
- Agent guide (`skill/vaultwarden-recovery-deploy`) and `AGENTS.md` to deploy the design on Linux or Windows (WSL2) without the agent ever seeing a secret; `src/vw-init-passphrase.sh` refuses to run without a real terminal.
- Six diagrams in both languages and an interactive page with an EN / ES switch.
