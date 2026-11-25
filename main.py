#!/usr/bin/env python3
"""One Star for Monday.

Writes a single line of plain text to /output/entry.txt: a one-star
review of Monday, written as though Monday were a restaurant.

The entry is a constant, held in this file. Nothing is read from the
network, from the environment, or from any file outside this repo.
"""

LINE = (
    "One star: waited forty minutes, got Sunday's leftovers reheated, "
    "and the server still charged me for Monday's special."
)

MAX_CHARS = 180
MAX_WORDS = 25


def validate(line: str) -> None:
    """Check the line against the competition gate before writing it."""
    assert isinstance(line, str), "entry must be a string"
    assert line.strip(), "entry must not be only whitespace"
    assert line == line.strip(), "entry must not start or end with whitespace"
    assert 1 <= len(line) <= MAX_CHARS, (
        f"entry must be 1-{MAX_CHARS} characters, got {len(line)}"
    )
    assert "\n" not in line and "\r" not in line, "entry must be a single line"
    assert "#" not in line, "entry must not contain a hashtag"
    assert "[" not in line and "]" not in line, "entry must not contain stage directions"
    words = line.split()
    assert 1 <= len(words) <= MAX_WORDS, (
        f"entry must be 1-{MAX_WORDS} words, got {len(words)}"
    )
    assert "  " not in line, "entry must not contain double spaces"


def choose_output_path() -> str:
    """Prefer /output/entry.txt; fall back to ./output/entry.txt.

    Probes writability with os.access so no stray empty file is created
    at a candidate path that is never used.
    """
    import os

    for candidate in ("/output/entry.txt", "./output/entry.txt"):
        directory = candidate.rsplit("/", 1)[0] or "."
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError:
            continue
        if os.access(directory, os.W_OK):
            return candidate
    raise OSError("no writable output path found")


def main() -> None:
    validate(LINE)
    path = choose_output_path()
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(LINE)
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    assert written == LINE, "round-trip mismatch: entry.txt differs from LINE"
    print(LINE)
    print(f"words: {len(LINE.split())}")
    print(f"characters: {len(LINE)}")
    print(f"wrote: {path}")


if __name__ == "__main__":
    main()
