<p align="center">
  <img src="assets/icon.png" alt="Bee DB Manager" width="128">
</p>

<h1 align="center">Bee DB Manager</h1>

<p align="center">
  <strong>Lightweight CLI database manager</strong><br>
  PostgreSQL · MySQL · MongoDB
</p>

<p align="center">
  <a href="https://github.com/dmkuzin2011-code/BEE_DB_Manager/releases">
    <img src="https://img.shields.io/github/v/release/dmkuzin2011-code/BEE_DB_Manager?style=flat-square" alt="Release">
  </a>
  <a href="https://github.com/dmkuzin2011-code/BEE_DB_Manager/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/dmkuzin2011-code/BEE_DB_Manager/github-workflows-build.yml?style=flat-square" alt="Build">
  </a>
  <img src="https://img.shields.io/badge/python-3.12+-blue?style=flat-square" alt="Python">
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-GPL--3.0-blue?style=flat-square" alt="License">
  </a>
</p>

---

## Features

- Connect to **PostgreSQL**, **MySQL**, and **MongoDB**
- Interactive REPL with autocomplete
- Run raw SQL queries and MongoDB commands (JSON)
- Pretty output powered by [Rich](https://github.com/Textualize/rich)
- Transaction support (`BEGIN` / `COMMIT` / `ROLLBACK`)
- Single-binary builds for Linux and Windows via GitHub Actions

---

## Installation

### From source

```bash
git clone https://github.com/dmkuzin2011-code/BEE_DB_Manager.git
cd BEE_DB_Manager
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Run:

```bash
cd "Source code"
python main.py
```

### Pre-built binaries

Download the latest release from the [Releases](https://github.com/dmkuzin2011-code/BEE_DB_Manager/releases) page:

| File | Platform |
|------|----------|
| `bee-db` | Linux |
| `bee-db.exe` | Windows |

---

## Usage

After starting the app you will see the prompt:

```
db>
```

### Commands

| Command | Description | Example |
|---------|-------------|---------|
| `connect` | Connect to a database | `connect postgres postgresql+asyncpg://user:pass@localhost/dbname` |
| `disconnect` | Close the current connection | `disconnect` |
| `help` | Show help | `help` |
| `exit` / `quit` | Exit the application | `exit` |

### SQL (PostgreSQL / MySQL)

```
postgres> SELECT * FROM users;
postgres> BEGIN;
postgres> INSERT INTO users (name) VALUES ('Alice');
postgres> COMMIT;
```

### MongoDB (JSON commands)

```
mongo> {"ping": 1}
mongo> {"find": "users", "filter": {}}
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `prompt-toolkit` | Interactive input |
| `rich` | Pretty terminal output |
| `sqlalchemy[asyncio]` + `asyncpg` / `aiomysql` | Async SQL |
| `motor` | Async MongoDB |

Full list: [`requirements.txt`](requirements.txt).

---

## Building with GitHub Actions

The workflow automatically:

1. Builds single-file binaries for **Linux** and **Windows**
2. On tags matching `v*` publishes a **GitHub Release** with the artifacts

### How to push and tag (so the Release is created)

```bash
# 1. Commit your changes
git add -A
git commit -m "Your commit message"
git push origin main

# 2. Create an annotated tag (must start with v)
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

Only tags starting with **`v`** (e.g. `v1.0.0`, `v0.2.1`) trigger the release job.

After the workflow finishes, binaries appear at:  
https://github.com/dmkuzin2011-code/BEE_DB_Manager/releases

---

## License

This project is licensed under the **GNU General Public License v3.0**.

You are free to use, modify, and redistribute this software under the terms of the GPL-3.0.  
See the [LICENSE](LICENSE) file for the full text.

```
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
```

Official license page: https://www.gnu.org/licenses/gpl-3.0.html
