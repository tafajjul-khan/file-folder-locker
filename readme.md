## File & Folder Vault (v3.1)

- A lightweight, secure, and intuitive Python desktop application built with Tkinter to password-protect your private files and folders. The app safely moves targeted data into an isolated hidden vault directory, tracks unauthorized decryption attempts, and implements safety guards against accidental self-locking or system-critical path modification.

---

## Features

- **Dual Mode Protection:** Seamlessly locks both individual files and entire directory structures.
- **SHA-256 Encryption:** Securely hashes passwords using SHA-256 before writing to the database registry—ensuring your master keys are never stored in plaintext.
- **Anti-Brute Force (Self-Destruct System):** Tracks failed unlock attempts on a per-item basis. After 20 failed attempts, the locked item is moved to the system Recycle Bin (`send2trash`) to protect against compromise without causing irreversible data deletion.
- **Robust Edge Case Guarding (New in v3.1):** - Prevents the script from locking its own working directory or script assets.
  - Blocks users from accidentally locking the underlying `.my_private_vault` metadata root.
  - Explicitly restricts tampering with critical OS paths like `C:\\`, `C:\\Windows`, or `Program Files`.
- **Dynamic Restoration:** Intelligently restores items back to their original absolute path. If the parent directory no longer exists, it cleanly falls back to recovering the item safely onto the user's Desktop.
- **Interactive UI:** Quick toggles to show/hide passphrases during entry, native OS file browsing, and instant vault population updates.

---

## Requirements & Installation

This application depends on Python 3.x and the `send2trash` cross-platform library to handle safe deletions.

1. **Clone or Download** the project script into its own dedicated folder.
2. **Install the dependencies:**