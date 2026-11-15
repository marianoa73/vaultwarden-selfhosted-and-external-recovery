# Limitations

[Versión en español](limitations.md)

- **Recovery point.** A nightly backup can lose up to a day of changes. Back up by hand before big changes, or schedule it more often.
- **No master password reset.** It is the price of client-side encryption. The emergency contact and the paper copies are the only way back.
- **Emergency access needs e-mail** for invitations and notices; without it the owner may not see a request in time.
- **Vaultwarden is unofficial.** It follows the Bitwarden clients' API; check release notes before updating and keep primary and standby on the same image.
- **The remote provider sees metadata**, such as file sizes and times, though not the content. A long random passphrase keeps offline guessing impractical.
- **The private network is a dependency.** If the mesh VPN service is down, devices cannot reach the vault; keep the offline recovery path in mind.
- **Disk encryption is optional.** The vault is encrypted inside, but the machine's disk is not by default; enable it if physical theft is in your threat model.
- **Paper can burn or be lost.** Keep two copies in two places and re-check them when you rehearse.
- **A rehearsal is the only proof.** Until a restore has been tried end to end, treat the procedure as untested.
- **Not a team product.** This design targets one owner and one trusted contact, not an organisation's access policy.
