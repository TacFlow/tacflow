# TACFLOW

**TACFLOW** is a local‑first platform for building, running and managing AI
agent swarms. Everything runs on your own machine — a message broker, an API, a
web dashboard and a set of local AI dependencies (speech‑to‑text,
text‑to‑speech, OCR and local LLMs) are installed and supervised for you by a
single installer.

This repository hosts the **official releases and installers**. For the full,
step‑by‑step setup instructions for every operating system, see
**[INSTALL.md](INSTALL.md)**.

## Quick start

Get your API key from <https://app.xtended.one> first, then run the installer
for your platform.

### macOS (Apple Silicon & Intel)

```bash
curl -fsSL https://github.com/tacflow1-tech/tacflow/releases/latest/download/install_mac.sh | bash
```

### Linux (amd64 & arm64)

```bash
# Desktop (graphical wizard)
curl -fsSL https://github.com/tacflow1-tech/tacflow/releases/latest/download/install_linux.sh | bash

# Servers / headless (terminal installer)
curl -fsSL https://github.com/tacflow1-tech/tacflow/releases/latest/download/install.sh | bash
```

### Windows (x64)

Download **`tacflow-installer-windows-amd64.exe`** from the
[latest release](https://github.com/tacflow1-tech/tacflow/releases/latest) and
run it. If SmartScreen appears, choose **More info → Run anyway**.

## After installation

Open the dashboard at **<http://localhost:8999>**.

| Component | Local port |
|-----------|-----------|
| Web dashboard | `8999` |
| API | `8088` |
| Message broker (NATS) | `4222` |

## Documentation

- 📘 **[Installation guide (all operating systems)](INSTALL.md)**
- 📦 [Releases & downloads](https://github.com/tacflow1-tech/tacflow/releases)
- 🔑 [Account dashboard](https://app.xtended.one)
- 🌐 [Website](https://xtended.one)

## Supported platforms

| OS | Architectures |
|----|---------------|
| macOS | Apple Silicon (`arm64`), Intel (`amd64`) |
| Windows | 64‑bit (`amd64` / x64) |
| Linux | `amd64` (x86‑64), `arm64` (aarch64) |
