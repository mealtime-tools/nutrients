"""The wire nutrient vocabulary, and where each name goes in Google Health.

`NUTRIENTS` holds the names the tools exchange -- FORMAT.md's item shape --
not Google Health's spelling of them. The two disagree often enough that a
list of API names would leave every consumer writing its own translation:
the format says `kcal`, `fat`, `carbs`, `fiber` where the API says `energy`,
`totalFat`, `CARBOHYDRATES`, `DIETARY_FIBER`.

So the mapping is the point, and it has two halves because the log has two
places to put a figure: `API_NUTRIENTS` for the `nutrients` array, and
`API_FIELDS` for a dedicated object. Both were read off nutrilog.

Every nutrient is grams. `kcal` alone is kilocalories.
"""

# Google Health's NutrientType, transcribed verbatim and alphabetical.
NUTRIENT_TYPES: tuple[str, ...] = (
    "BIOTIN",
    "CAFFEINE",
    "CALCIUM",
    "CARBOHYDRATES",
    "CHLORIDE",
    "CHOLESTEROL",
    "CHROMIUM",
    "COPPER",
    "DIETARY_FIBER",
    "FOLATE",
    "FOLIC_ACID",
    "IODINE",
    "IRON",
    "MAGNESIUM",
    "MANGANESE",
    "MOLYBDENUM",
    "MONOUNSATURATED_FAT",
    "NIACIN",
    "PANTOTHENIC_ACID",
    "PHOSPHORUS",
    "POLYUNSATURATED_FAT",
    "POTASSIUM",
    "PROTEIN",
    "RIBOFLAVIN",
    "SATURATED_FAT",
    "SELENIUM",
    "SODIUM",
    "SUGAR",
    "THIAMIN",
    "TRANS_FAT",
    "UNSATURATED_FAT",
    "VITAMIN_A",
    "VITAMIN_B12",
    "VITAMIN_B6",
    "VITAMIN_C",
    "VITAMIN_D",
    "VITAMIN_E",
    "VITAMIN_K",
    "ZINC",
)

# Unreachable by design: `carbs` already carries this to totalCarbohydrate.
UNREACHABLE_NUTRIENT_TYPES: frozenset[str] = frozenset({"CARBOHYDRATES"})

# Wire names that differ from the lowercased enum spelling.
_WIRE_NAMES = {"DIETARY_FIBER": "fiber"}


def _wire_name(nutrient_type: str) -> str:
    return _WIRE_NAMES.get(nutrient_type, nutrient_type.lower())


# Derived, so the identity rows cannot drift from NUTRIENT_TYPES.
API_NUTRIENTS: dict[str, str] = {
    _wire_name(nutrient_type): nutrient_type
    for nutrient_type in NUTRIENT_TYPES
    if nutrient_type not in UNREACHABLE_NUTRIENT_TYPES
}

# Dedicated objects, not array entries; `energy` takes kcal, not grams.
API_FIELDS: dict[str, str] = {
    "kcal": "energy",
    "carbs": "totalCarbohydrate",
    "fat": "totalFat",
}

# Required by every tool; ordered as they read on a label.
CORE_NUTRIENTS: tuple[str, ...] = ("kcal", "protein", "fat", "carbs")

# History: with the core four, the first seven keys of every share link.
_LEGACY_NUTRIENTS: tuple[str, ...] = ("fiber", "sodium", "sugar")

_REST: tuple[str, ...] = tuple(
    sorted(
        (set(API_NUTRIENTS) | set(API_FIELDS))
        - set(CORE_NUTRIENTS)
        - set(_LEGACY_NUTRIENTS)
    )
)

# Every wire name, in the order every tool renders them.
NUTRIENTS: tuple[str, ...] = CORE_NUTRIENTS + _LEGACY_NUTRIENTS + _REST

# What a record may leave unstated, per FORMAT.md.
OPTIONAL_NUTRIENTS: tuple[str, ...] = _LEGACY_NUTRIENTS + _REST

# The one wire name measured in kcal rather than grams.
ENERGY_NUTRIENT = "kcal"

NUTRIENT_UNIT = "g"
ENERGY_UNIT = "kcal"
