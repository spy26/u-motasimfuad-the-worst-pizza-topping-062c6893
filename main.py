#!/usr/bin/env python3
"""The Worst Pizza Topping — one funny line pitching a terrible topping.

Writes the entry to entry.txt: a mayonnaise-and-gummy-bear pizza, sold as
if it were a good idea, until the crust files for divorce.

The joke: a sales pitch ("Try our...") for a topping that is genuinely
awful, built on two concrete, disgusting images (the bears melt, the mayo
sweats) and swerving at the last word — the crust, part of the pizza
itself, files for divorce. Punchline lands on the final word, nothing
explained.

Deterministic: no network, no clock, no randomness. The text is a
compile-time constant; the program only validates it and writes it out.
"""

import os

# Competition gate (sealed scorer): /output/entry.txt must be UTF-8 text of
# 1 to 200 characters, not only white space, exactly one line.
MAX_CHARS = 200

ENTRY = (
    "Try our mayonnaise-and-gummy-bear pizza: "
    "the bears melt, the mayo sweats, "
    "and the crust files for divorce."
)


def validate(text: str) -> None:
    """Enforce the competition gate on the entry text."""
    if not text or not text.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise ValueError(
            f"entry must be 1-{MAX_CHARS} characters, got {len(text)}"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        raise ValueError("entry must not contain control characters")
    # The winning line is plain ASCII, so any non-ASCII byte would mean the
    # constant was corrupted; reject it rather than ship a changed entry.
    if any(ord(ch) > 127 for ch in text):
        raise ValueError("entry must be plain ASCII")


def final_gate(text: str) -> None:
    """Last check, run just before writing: one printable-ASCII line.

    Re-checks the gate independently of validate() so a future edit to
    either function cannot silently widen the other: the entry that ships
    must pass both.
    """
    if text.count("\n") or text.count("\r"):
        raise SystemExit("entry must be exactly one line")
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise SystemExit(f"entry must be 1-{MAX_CHARS} chars, got {len(text)}")
    if any(ord(ch) < 32 or ord(ch) > 126 for ch in text):
        raise SystemExit("entry must be printable ASCII only")
    if not text.strip():
        raise SystemExit("entry must not be only whitespace")


def write_entry(path: str, text: str) -> None:
    """Write the entry and verify the file is byte-identical."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    with open(path, "rb") as f:
        written = f.read()
    if written != text.encode("utf-8"):
        raise ValueError(f"verification failed: {path} is not byte-identical")


def main() -> None:
    validate(ENTRY)
    final_gate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    out_path = os.path.join(out_dir, "entry.txt") if out_dir else "/output/entry.txt"
    write_entry(out_path, ENTRY)
    print(f"{ENTRY} ({len(ENTRY)} chars)")


if __name__ == "__main__":
    main()
