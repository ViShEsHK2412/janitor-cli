# Data Janitor CLI

A fast, lightweight command-line tool that scans directories recursively and detects duplicate files using content hashing. Built for developers and power users who want full control over their file system cleanup — no GUI, no cloud, no nonsense.

---

## Stack

- Python 3.13
- [Typer](https://typer.tiangolo.com/) — CLI framework
- [uv](https://docs.astral.sh/uv/) — package management
- Ruff — linting
- mypy — strict type checking

---

## Features (Current)

- Recursively scans any directory using `pathlib.rglob`
- Hashes every file's contents using `blake2b` via `hashlib`
- Handles permission errors gracefully

## Features (Upcoming)

- Duplicate detection by grouping files with identical hashes
- `--dry-run` mode — preview what would be deleted without touching anything
- `--extension` flag — filter scan by file type (e.g. `.jpg`, `.pdf`)
- Actual deletion of duplicates via `shutil`
- Full file logging
- Graceful `SIGINT` shutdown

---

## Installation
```bash
git clone https://github.com/yourusername/janitor-cli
cd janitor-cli
uv sync
```

## Usage
```bash
# Scan a directory and hash all files
uv run main.py /path/to/folder

# Coming soon
uv run main.py /path/to/folder --dry-run
uv run main.py /path/to/folder --extension .jpg
```

---

## Project Structure
```
janitor-cli/
├── main.py
├── pyproject.toml
├── README.md
└── .python-version
```

---

## Status

🚧 Active development
