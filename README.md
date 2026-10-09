# media-tidy

My photo library was a mess of folders with names like "New folder (3)". I wrote this to sort it out.

![CI](https://github.com/Rey-EL/media-tidy/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

## Features

- Sorts photos into `Images/` and videos into `Videos/`
- Renames every file to `YYYY-MM-DD_HH-MM-SS` based on EXIF "Date Taken"
- Falls back to the file's modification time when no EXIF date exists
- Appends a counter (`(1)`, `(2)`, …) when two files would get the same name
- Deletes leftover empty folders when the run finishes

## Install

```bash
git clone https://github.com/Rey-EL/media-tidy.git
cd media-tidy
pip install -r requirements.txt
```

## Usage

```bash
python3 media_tidy.py
```

Pick your media library folder in the dialog. The tool moves everything into `Images/` and `Videos/` inside that folder and cleans up the empties. Run it on a copy first if the library matters to you.

## How it works

Two passes. First it walks the library and collects every media file outside the two destination folders. Then it dates each file (EXIF first, mtime as fallback), renames it, moves it, and finally removes empty directories bottom-up. Tests live in `tests/` and run on Python 3.10–3.12 in CI.

## Project structure

```
media-tidy/
├── media_tidy.py             # the tool
├── requirements.txt
├── tests/                    # pytest suite (pure functions only)
└── .github/workflows/ci.yml  # CI workflow
```

## License

MIT — see [LICENSE.md](LICENSE.md).
