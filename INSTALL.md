# TACFLOW — Installation Guide

TACFLOW is a local‑first platform for building, running and managing AI agent
swarms. It runs entirely on your own machine: a message broker, an API, a web
dashboard and a set of local AI dependencies (speech‑to‑text, text‑to‑speech,
OCR, local LLMs) are installed and supervised for you by a single installer.

This guide covers a complete installation on **every supported operating
system**. Pick your OS below and follow the steps.

- [System requirements](#system-requirements)
- [Before you begin](#before-you-begin)
- [What the installer sets up](#what-the-installer-sets-up)
- [Install on macOS](#install-on-macos-apple-silicon--intel)
- [Install on Windows](#install-on-windows-x64)
- [Install on Linux](#install-on-linux-amd64--arm64)
- [First launch & verification](#first-launch--verification)
- [Verifying your download (SHA‑256)](#verifying-your-download-sha-256)
- [Updating](#updating)
- [Uninstalling](#uninstalling)
- [Troubleshooting](#troubleshooting)
- [Release channels (advanced)](#release-channels-advanced)
- [Getting help](#getting-help)

---

## System requirements

| Platform | Architectures | Notes |
|----------|---------------|-------|
| **macOS** | Apple Silicon (`arm64`), Intel (`amd64`) | macOS 11 Big Sur or newer recommended |
| **Windows** | 64‑bit (`amd64` / x64) | Windows 10 or 11. Windows on ARM runs the x64 build under emulation |
| **Linux** | `amd64` (x86‑64), `arm64` (aarch64) | glibc‑based distributions. A desktop (X11/Wayland) is required only for the graphical installer |

**Hardware**

- **CPU:** any modern 64‑bit processor.
- **RAM:** 8 GB minimum. **16 GB or more recommended** if you plan to run local
  LLMs and speech models.
- **Disk:** at least ~5 GB free for the application and its runtime
  dependencies. Local models you choose to download need additional space
  (some models are several GB each).
- **GPU:** optional. A supported GPU accelerates local model inference and
  transcription but is not required.

**Network**

- An internet connection is required during installation (to download
  components) and for account activation. After setup, most features run
  locally.

---

## Before you begin

1. **Get a TACFLOW account and API key.** Sign in to your account dashboard at
   <https://app.xtended.one> and copy your API key (it starts with `sa_`). The
   installer will ask for this key to activate the platform.
2. Make sure the ports the platform uses are free (see
   [What the installer sets up](#what-the-installer-sets-up)).
3. All commands below download signed release assets from the official
   repository:
   <https://github.com/tacflow1-tech/tacflow/releases/latest>.

---

## What the installer sets up

The installer (graphical wizard or terminal) provisions and supervises the
whole stack for you:

| Component | Purpose | Local port |
|-----------|---------|-----------|
| **Message broker** (NATS / `tac_broker`) | Real‑time messaging between agents, flows and the UI | `4222` |
| **TACFLOW API** | Core backend / agent runtime | `8088` |
| **Web dashboard** (client app) | The user interface | `8999` → <http://localhost:8999> |
| **Local AI dependencies** | Ollama + local models, Whisper / Fast‑Whisper (speech‑to‑text), text‑to‑speech (eSpeak / Piper / Fish), Tesseract (OCR), RobotGO automation | — |
| **Background services** | Autostart on login via `launchd` (macOS), `systemd` user services (Linux) or a Windows service | — |

After installation the dashboard is available in your browser at
**<http://localhost:8999>**.

---

## Install on macOS (Apple Silicon & Intel)

> **Which chip do I have?** Run `uname -m` in Terminal. `arm64` = Apple Silicon
> (M‑series); `x86_64` = Intel. The installer detects this automatically.

### Method A — One‑line graphical installer (recommended)

Open **Terminal** and run:

```bash
curl -fsSL https://github.com/tacflow1-tech/tacflow/releases/latest/download/install_mac.sh | bash
```

This downloads the correct `TACFLOW Installer.app` for your chip, extracts it to
`~/Applications/`, removes the macOS quarantine flag, and launches the graphical
setup wizard. Follow the wizard and paste your API key when prompted.

### Method B — Manual download

1. Go to the [latest release](https://github.com/tacflow1-tech/tacflow/releases/latest).
2. Download the installer for your chip:
   - Apple Silicon: **`tacflow-installer-darwin-arm64.zip`**
   - Intel: **`tacflow-installer-darwin-amd64.zip`**
3. Unzip it (double‑click, or `unzip tacflow-installer-darwin-arm64.zip`).
4. Remove the quarantine attribute so Gatekeeper allows it to run:
   ```bash
   xattr -cr "TACFLOW Installer.app"
   ```
5. Open **`TACFLOW Installer.app`**. If macOS still blocks it, right‑click the
   app → **Open**, or go to **System Settings → Privacy & Security → Open
   Anyway**.

### Method C — Terminal‑only (no GUI)

Ideal for remote Macs or when you prefer a headless install:

```bash
curl -fsSL https://github.com/tacflow1-tech/tacflow/releases/latest/download/install.sh | bash
```

The terminal installer verifies the download against `SHA256SUMS.txt` before
running it.

---

## Install on Windows (x64)

1. Go to the [latest release](https://github.com/tacflow1-tech/tacflow/releases/latest).
2. Download **`tacflow-installer-windows-amd64.exe`**.
3. Double‑click the file to run it.
4. **Microsoft Defender SmartScreen** may show *"Windows protected your PC"*
   because the app is newly published. Click **More info → Run anyway**.
5. Follow the setup wizard and paste your API key (`sa_…`) when prompted.

**Notes**

- The installer runs **per‑user** — administrator rights are not required.
- It registers a background service so TACFLOW starts automatically when you log
  in.
- If your antivirus quarantines the download, restore it or add an exclusion —
  the binary is unsigned‑by‑a‑third‑party but published from the official
  release repository. You can verify its checksum against `SHA256SUMS.txt`
  (see [Verifying your download](#verifying-your-download-sha-256)).
- Windows on ARM: run the `amd64` build; Windows provides x64 emulation.

Optional — download from PowerShell instead of the browser:

```powershell
$u = "https://github.com/tacflow1-tech/tacflow/releases/latest/download/tacflow-installer-windows-amd64.exe"
Invoke-WebRequest -Uri $u -OutFile "$env:USERPROFILE\Downloads\tacflow-installer-windows-amd64.exe"
Start-Process "$env:USERPROFILE\Downloads\tacflow-installer-windows-amd64.exe"
```

---

## Install on Linux (amd64 & arm64)

Two installers are available: a **graphical wizard** for desktop machines and a
**terminal installer** for servers and headless systems.

### Method A — One‑line graphical installer (desktop)

Requires a graphical session (X11 or Wayland) with OpenGL:

```bash
curl -fsSL https://github.com/tacflow1-tech/tacflow/releases/latest/download/install_linux.sh | bash
```

This installs the `tacflow-installer` binary to `~/.local/bin/` and launches the
graphical setup wizard, which performs all the real work (broker, Ollama,
models, speech engines, configuration).

### Method B — Terminal installer (servers / headless)

No display needed — the entire install runs in the terminal:

```bash
curl -fsSL https://github.com/tacflow1-tech/tacflow/releases/latest/download/install.sh | bash
```

**Non‑interactive** (CI, provisioning, cloud servers) — supply the API key and
accept the terms up front:

```bash
TACFLOW_API_KEY=sa_your_key_here TACFLOW_ACCEPT_TERMS=1 \
  bash <(curl -fsSL https://github.com/tacflow1-tech/tacflow/releases/latest/download/install.sh)
```

The terminal installer verifies the binary against `SHA256SUMS.txt` before
executing it and refuses to run an unverified download.

### Distribution notes

- **Debian / Ubuntu**, **Fedora / RHEL / CentOS Stream**, **Arch** and other
  glibc distributions are supported. The installer downloads self‑contained
  binaries, so there are no distro‑specific packages to add.
- The **graphical** installer needs the usual desktop GL/X11 libraries
  (`libGL`, `libX11`, `libxkbcommon`, …), which are already present on standard
  desktop installs. On a minimal/server system without a display, use the
  **terminal installer (Method B)** instead.
- Background services are installed as **`systemd` user services** and start on
  login.
- Make sure **`~/.local/bin` is on your `PATH`** (most shells add it
  automatically; if not, add `export PATH="$HOME/.local/bin:$PATH"` to your
  shell profile).

---

## First launch & verification

1. Once the wizard finishes, open **<http://localhost:8999>** in your browser —
   this is the TACFLOW dashboard.
2. Sign in / activate with your account if prompted.
3. The API runs on `http://localhost:8088` and the message broker on port
   `4222`. These are used internally by the dashboard.

If the page does not load immediately, give the background services a few
seconds to start, then refresh.

---

## Verifying your download (SHA‑256)

Every release includes a **`SHA256SUMS.txt`** file listing the checksum of each
asset. The scripted installers verify this automatically; to check a manual
download yourself:

**macOS / Linux**

```bash
# from the folder containing the downloaded asset
curl -fsSLO https://github.com/tacflow1-tech/tacflow/releases/latest/download/SHA256SUMS.txt
shasum -a 256 -c SHA256SUMS.txt 2>/dev/null | grep -i "tacflow-installer"
# (on Linux you can also use: sha256sum -c SHA256SUMS.txt)
```

**Windows (PowerShell)**

```powershell
Get-FileHash .\tacflow-installer-windows-amd64.exe -Algorithm SHA256
# Compare the printed hash against the matching line in SHA256SUMS.txt
```

---

## Updating

- TACFLOW updates itself in place — the app checks the release channel and
  applies updates through its built‑in updater / tray launcher.
- You can also update at any time by **re‑running the installer** for your OS
  using the commands above; it will refresh the installed components to the
  latest release.

---

## Uninstalling

The setup wizard includes a **Remove / Uninstall** option — re‑launch the
installer and choose it to stop the services and remove the installed
components. If you prefer to clean up manually:

**macOS**

```bash
# Stop and remove per-user launchd services (names begin with tacflow / tac_)
launchctl list | grep -i tac
# Remove the installer app
rm -rf "$HOME/Applications/TACFLOW Installer.app"
```

**Linux**

```bash
# Stop and disable the per-user services, then remove the installer binary
systemctl --user stop    'tac*' 'tacflow*' 2>/dev/null || true
systemctl --user disable 'tac*' 'tacflow*' 2>/dev/null || true
rm -f "$HOME/.local/bin/tacflow-installer"
```

**Windows**

- Use the installer's **Remove** option, or remove the TACFLOW background
  service and delete the installed program folder from your user profile.

> Data, models and configuration created after install are kept in your user
> profile; delete those directories separately if you want a completely clean
> removal.

---

## Troubleshooting

**macOS: "TACFLOW Installer.app" is damaged / cannot be opened**
The app picked up the quarantine flag. Clear it and reopen:
```bash
xattr -cr "$HOME/Applications/TACFLOW Installer.app"
```

**macOS: Gatekeeper blocks the app**
Right‑click the app → **Open**, or **System Settings → Privacy & Security →
Open Anyway**.

**Windows: SmartScreen warning**
Click **More info → Run anyway**. This appears for newly‑published apps.

**Linux: the graphical installer will not start**
You are likely on a headless/minimal system with no display or GL libraries.
Use the **terminal installer**:
```bash
curl -fsSL https://github.com/tacflow1-tech/tacflow/releases/latest/download/install.sh | bash
```

**A port is already in use (`4222`, `8088`, or `8999`)**
Another program (or a previous TACFLOW instance) is using the port. Stop the
conflicting process or the existing TACFLOW services and re‑run the installer.

**Linux: `tacflow-installer: command not found`**
`~/.local/bin` is not on your `PATH`. Add it and restart your shell:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.profile && source ~/.profile
```

**Download fails / checksum mismatch**
Re‑run the command (the scripts retry automatically). A checksum mismatch means
the download was corrupted or tampered with — the installer will refuse to run
it; simply try again on a stable connection.

---

## Release channels (advanced)

By default every command targets the **latest stable release**. To install a
specific build or an internal validation build, point the installer at another
release base with the `TACFLOW_RELEASE_BASE` environment variable:

```bash
TACFLOW_RELEASE_BASE=https://github.com/tacflow1-tech/tacflow/releases/download/<tag> \
  bash <(curl -fsSL https://github.com/tacflow1-tech/tacflow/releases/download/<tag>/install.sh)
```

Replace `<tag>` with the release tag you want to install.

---

## Getting help

- **Releases & downloads:** <https://github.com/tacflow1-tech/tacflow/releases>
- **Account dashboard:** <https://app.xtended.one>
- **Website:** <https://xtended.one>

If you hit a problem not covered here, open an issue on the
[repository](https://github.com/tacflow1-tech/tacflow/issues) with your OS,
architecture (`uname -m` / Windows x64) and the output of the installer.
