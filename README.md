<p align="center">
  <img src="assets/icon.png" alt="Bee DB Manager" width="128">
</p>

<h1 align="center">Bee DB Manager</h1>

<p align="center">
  <strong>Light weigth manager</strong><br>
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
</p>
---

## Features

- Connect to **PostgreSQL**, **MySQL**, and **MongoDB**
- Interactive REPL with autocomplete
- Execute SQL queries and MongoDB commands (JSON)
- Beautiful result output via [Rich](https://github.com/Textualize/rich)
- Transaction support (`BEGIN` / `COMMIT` / `ROLLBACK`)
- Single-binary build via GitHub Actions (Linux + Windows)

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

- `bee-db` — Linux
- `bee-db.exe` — Windows

---

## Usage

After launching, a prompt will appear:

```
db>
```

### Basic Commands

| Command | Description | Example |
|---------|----------|--------|
| `connect` | Connect to the database | `connect postgres postgresql+asyncpg://user:pass@localhost/dbname` |
| `disconnect` | Disconnect | `disconnect` |
| `help` | Help | `help` |
| `exit` / `quit` | Exit | `exit` |
| `version` | Show current version | `version` |

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

- `prompt-toolkit` — interactive input
- `rich` — beautiful output
- `sqlalchemy[asyncio]` + `asyncpg` / `aiomysql` — SQL
- `motor` — MongoDB

Full list in [`requirements.txt`](requirements.txt).

---

## Build via GitHub Actions

The workflow automatically:

1. Builds binaries for **Linux** and **Windows**
2. Publishes a **GitHub Release** with artifacts when a `v*` tag is created

---

## License

Open-source project. Feel free to use it.