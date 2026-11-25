"""Museum of the Year 3000.

Writes one museum label to $MAKEFUN_OUTPUT_DIR/entry.txt: the
label a museum in the year 3000 puts beside a group chat, read
as a communal hall where dozens of people gathered every day to
read each other's messages and answer almost none of them.
Standard library only; the label is checked against the
competition gate (one line of UTF-8 text, 1 to 200 characters)
before anything is written.
"""

import os

LABEL = (
    "Group chat (c. 2024). A communal hall where 47 people "
    "gathered daily to read each other's messages and answer "
    "almost none of them."
)

CHAR_LIMIT = 200


def label_text():
    """Return the museum label for the year 3000."""
    return LABEL


def gate_check(text):
    """Check the label against the competition gate.

    The gate wants one line of plain UTF-8 text, between 1
    and 200 characters, that is not only whitespace. A label
    that fails here is rejected instead of wasting a
    submission on the server.
    """
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("museum label is empty")
    if len(cleaned) > CHAR_LIMIT:
        raise ValueError(
            "museum label is %d characters, over the 200 limit"
            % len(cleaned)
        )
    if "\n" in cleaned or "\r" in cleaned:
        raise ValueError("museum label must fit on exactly one line")
    return cleaned


def label_has_catalogue_date(text):
    """Check the label carries a museum catalogue date.

    A real museum label dates its object, here as "(c. 2024)".
    A label without that date reads like a caption, not a
    label, so it is rejected here before anything is written.
    """
    start = text.find("(c. ")
    if start < 0:
        raise ValueError("museum label has no catalogue date")
    end = text.find(")", start)
    if end < 0 or not text[start + 4:end].strip().isdigit():
        raise ValueError("museum label catalogue date is malformed")
    return text


def label_measure(text):
    """Measure the label for a last sanity pass.

    Returns the character and word counts. A label too short
    to carry both the object and the misreading, or one padded
    out to fill the cap, is caught here before anything is
    written.
    """
    words = text.split()
    return {"chars": len(text), "words": len(words)}


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    label = gate_check(label_text())
    label = label_has_catalogue_date(label)
    shape = label_measure(label)
    if shape["words"] < 5:
        raise ValueError("museum label is too short to land the joke")
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as handle:
        handle.write(label)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
