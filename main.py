"""Write the make.fun competition entry to entry.txt.

This program uses only the Python standard library and makes no network requests.
"""

import errno
import tempfile
from pathlib import Path


ENTRY_TEXT = "I lost the bounty because I logged a successful upload after clicking Submit in a screenshot."

# Permission-style errors that trigger the ./output fallback.
FALLBACK_ERRNOS = frozenset((errno.EACCES, errno.EPERM, errno.EROFS))


def entry_bytes() -> bytes:
    """Return the entry and its trailing newline as UTF-8 bytes."""
    return (ENTRY_TEXT + "\n").encode("utf-8")


def write_entry(directory: Path) -> None:
    """Stage the entry in directory and atomically replace entry.txt."""
    directory.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=directory) as temporary_directory:
        staged_entry = Path(temporary_directory) / "entry.txt"
        staged_entry.write_bytes(entry_bytes())
        staged_entry.chmod(0o644)
        staged_entry.replace(directory / "entry.txt")


def main() -> None:
    """Write to /output, falling back to ./output on permission errors."""
    try:
        write_entry(Path("/output"))
    except OSError as error:
        if error.errno not in FALLBACK_ERRNOS:
            raise
        write_entry(Path("output"))


if __name__ == "__main__":
    main()
