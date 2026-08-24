"""Emit the vocabulary as JSON for the JavaScript tool to import.

A Python module cannot be the source of truth for `../plate`, so the
vocabulary is rendered to a committed JSON file and a test asserts the commit
matches what this module emits. Run after editing the vocabulary:

    python -m mealtime_nutrients.generate_json
"""

import json
from pathlib import Path

from mealtime_nutrients.vocabulary import (
    API_FIELDS,
    API_NUTRIENTS,
    CORE_NUTRIENTS,
    ENERGY_NUTRIENT,
    ENERGY_UNIT,
    NUTRIENT_UNIT,
    NUTRIENTS,
)

# Repository root: present in a checkout, absent from an installed wheel.
JSON_PATH = Path(__file__).resolve().parents[2] / "nutrients.json"


def render() -> str:
    """The exact bytes of nutrients.json, newline included.

    Carries the wire names, because those are what plate parses out of an
    item, plus the routing so plate can build a nutrition log without a second
    copy of the mapping in JavaScript. Keys are camelCase to read naturally
    there; the nutrient names themselves are the wire names verbatim.
    """
    document = {
        "unit": NUTRIENT_UNIT,
        "energyUnit": ENERGY_UNIT,
        "energyNutrient": ENERGY_NUTRIENT,
        "coreNutrients": list(CORE_NUTRIENTS),
        "nutrients": list(NUTRIENTS),
        "apiNutrients": dict(sorted(API_NUTRIENTS.items())),
        "apiFields": dict(sorted(API_FIELDS.items())),
    }
    return json.dumps(document, indent=2) + "\n"


if __name__ == "__main__":
    JSON_PATH.write_text(render())
    print(f"wrote {JSON_PATH}")
