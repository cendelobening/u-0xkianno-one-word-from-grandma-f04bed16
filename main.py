#!/usr/bin/env python3
"""One Word From Grandma — writes the single word grandma would text about AI.

Chosen word: Chatwhat
Why: grandma mishears "ChatGPT" as "chat what?" — warm, baffled, funny in
one word, unmistakably about AI, and fresh (a typo she would actually make).
"""

import os
import tempfile

WORD = "Chatwhat"


def main():
    word = WORD

    # Guards: exactly one word, 1-30 characters, no whitespace at all,
    # and only printable characters (no control characters or newlines).
    if not word:
        raise ValueError("word must not be empty")
    if len(word) < 1 or len(word) > 30:
        raise ValueError("word must be 1-30 characters")
    if len(word.split()) != 1:
        raise ValueError("word must be a single token")
    if any(ch.isspace() or not ch.isprintable() for ch in word):
        raise ValueError("word must contain no whitespace or control characters")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")

    # Write via a temp file in the same directory, then atomic replace.
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(word)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, out_path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    os.chmod(out_path, 0o644)

    # Read back and confirm the file on disk is exactly the word, nothing else.
    with open(out_path, "rb") as f:
        written = f.read()
    if written != word.encode("utf-8"):
        raise ValueError("written file does not match the chosen word")


if __name__ == "__main__":
    main()
