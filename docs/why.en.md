# Why this project, and what to use instead

[Versión en español](why.md)

## The need

Running websites, social accounts, publications, hosting, cloud servers, AI services and brokerage accounts multiplies credentials. Left alone they end up reused, saved in browsers, pasted in notes or lost. This project was created to **secure and control every key of those projects in one place**, with a second factor, an encrypted off-site copy and a tested way back if something fails.

## The model: three tiers of secrets

| Tier | What it is | Where it lives |
|---|---|---|
| Root secrets | master password, second-factor recovery codes, backup passphrase, recovery of the owner e-mail account | **written on paper**, kept offline in separate places; the master password is also memorised |
| Daily credentials | the many logins you use every day | **in the password manager**: generated, unique, autofilled, never retyped |
| Machine secrets | API keys, tokens, deploy keys | in the manager (secure notes), with the smallest scope, spending caps and a rotation date |

The rule: **paper for the few keys that open everything; the manager for the many you use daily**. If the manager fails, the paper brings it back; if the paper is lost, the manager still works.

## Alternatives

This repository describes one proven way, not the only one. Any similar model is fine; check each product's current features, price and privacy terms.

| Need | Examples |
|---|---|
| Self-hosted vault | Vaultwarden (this project; an unofficial server compatible with Bitwarden clients), the official Bitwarden self-hosted edition, KeePassXC with a synced file |
| Hosted vault | Bitwarden, 1Password, Proton Pass, Dashlane |
| Authenticator app (TOTP) | Google Authenticator, Microsoft Authenticator, Aegis (Android, open source), 2FAS, Ente Auth |
| Hardware security keys (FIDO2) | YubiKey, Google Titan; register at least two |
| Passkeys | built into most platforms; use them where a site offers them |

Vaultwarden is not made by Bitwarden Inc.; use the official clients and keep the server image updated.

## Recommendations

- **Browsers should not remember passwords.** Turn off the built-in password saving and autofill and let the manager do it. If a browser does keep some, protect that browser account with a second factor, lock the device and encrypt its disk.
- **Use a second factor everywhere it exists**, preferring hardware keys or an authenticator app to SMS.
- **Keep the root secrets on paper**, in two places that do not depend on each other, and test that you can read them.
- **Never put secrets in chat, tickets, notes, screenshots, repositories or an AI assistant's memory.**
- **Separate owner accounts from operator accounts**, and give each automation the smallest token it needs.
- The full checklist is in [security](security.en.md); the way back is in [recovery](recovery.en.md).
