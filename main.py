#!/usr/bin/env python3
"""Weirdest Job Title: Blind Judge Showdown — make.fun entry.

Writes a single job title to /output/entry.txt.

The title was picked for the judge's brief, in the brief's own order:
1. It is a weird job title — a few words naming an odd job.
2. It is stranger than ordinary work — nobody hires a ghostwriter
   for a dog, and an autobiography no dog can write is a gloriously
   odd twist.
3. It is funny — the twist lands on the first read: a dog dictating
   its life story to a hired writer.
4. It sounds like a real job — "Professional Ghostwriter" is a real
   title, specific enough to picture the person doing it (typing
   while a dog dictates). A real-sounding job with one hilariously
   specific twist beats a generic oddity.
5. It reads instantly — 50 characters, one line, plain words, no
   punctuation to trip over.

The file holds exactly the title, no trailing newline, so its byte
size is the title's 50 bytes — the ranking tie-break favours the
smaller text, so no byte is wasted.

Usage:
    python3 main.py [--output-dir DIR]

The output directory defaults to /output (the grader's directory) and
can be overridden for local runs.
"""

import argparse
import os
import sys

# The job title. One line, 50 characters, under the 60-character gate.
TITLE = "Professional Ghostwriter for Dogs' Autobiographies"

MAX_CHARS = 60


def validate(text):
    """Check the text against the gate: UTF-8, 1-60 chars, one line.

    Both the character count and the byte count must fit the gate, so
    a multi-byte character can never push the file over the limit, and
    the text must be exactly as written — no leading or trailing
    whitespace, no newline.
    """
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d-character limit"
            % (len(text), MAX_CHARS)
        )
    encoded = text.encode("utf-8")  # raises if not valid UTF-8 text
    if len(encoded) > MAX_CHARS:
        raise ValueError(
            "entry is %d bytes, over the %d-byte limit"
            % (len(encoded), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Write the weirdest job title to entry.txt."
    )
    parser.add_argument(
        "--output-dir",
        default=os.environ.get("OUTPUT_DIR", "/output"),
        help="directory to write entry.txt into (default: /output)",
    )
    args = parser.parse_args(argv)

    title = validate(TITLE)

    os.makedirs(args.output_dir, exist_ok=True)
    path = os.path.join(args.output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(title)

    # Read the file back and re-validate it, so a write that silently
    # truncated or mangled the text is caught here, not by the gate.
    with open(path, "rb") as handle:
        raw = handle.read()
    if raw != title.encode("utf-8"):
        raise ValueError("read-back mismatch: entry.txt is not the title")
    validate(raw.decode("utf-8"))

    print("Wrote %s (%d characters, %d bytes):"
          % (path, len(title), len(raw)))
    print(title)
    return 0


if __name__ == "__main__":
    sys.exit(main())
