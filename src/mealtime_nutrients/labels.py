"""How a nutrition label spells a wire name.

A panel prints "Vitamin B12" and "Folic Acid" where the vocabulary holds
`vitamin_b12` and `folic_acid`, so a reader matching rows against names needs
the separator to be flexible. Deriving that here keeps it with the vocabulary
it is derived from, and means a name added upstream is recognised without an
edit downstream.

This is only the per-name derivation. Which rows a parser recognises, and in
what order it tries them, is the parser's own policy: a panel's sub-rows
overlap their totals, and only ordering keeps "- Saturated" off the fat row.
"""

import re

_SEPARATOR = r"[\s-]?"


def row_pattern(name: str) -> str:
    """The regex source matching the label row for one wire name."""
    return _SEPARATOR.join(re.escape(part) for part in name.split("_"))
