"""The wire nutrient vocabulary, and where each name goes in Google Health.

`NUTRIENTS` holds the names that appear in the JSON the mealtime tools exchange
-- the item shape in FORMAT.md -- not Google Health's API spelling of them. The
two disagree often enough that a bare list of API names would leave every
consumer writing its own translation layer: the format says `kcal`, `fat`,
`carbs` and `fiber` where the API says `energy`, `totalFat`, `CARBOHYDRATES`
and `DIETARY_FIBER`.

The mapping is therefore the point of this module, and it has two halves,
because Google Health's nutrition log has two places to put a figure:

- `API_NUTRIENTS` -- names that go into the `nutrients` array, as an enum
  member. Membership here is what "array-eligible" means.
- `API_FIELDS` -- names that go into a dedicated object on the log instead.

Both were read off nutrilog rather than invented: `MealLog.to_api_payload`
for the split, `cli.STANDARD_NUTRIENTS` and `NutrientType.from_string` for the
non-identity spellings.

Units: every nutrient here is expressed in GRAMS, and every dedicated field
takes its figure under a `grams` key. Google Health accepts no milligram or
microgram variant, not even for the trace minerals and vitamins whose labels
print mg or ug, so a record holding milligrams holds a figure a thousand times
too large. `kcal` is the sole exception: it is kilocalories, and its dedicated
`energy` object takes a `kcal` key.
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

# Exactly one name per nutrient: a second spelling could double-declare.
NUTRIENTS: tuple[str, ...] = tuple(
    sorted(set(API_NUTRIENTS) | set(API_FIELDS))
)

# Required by every tool; ordered as they read on a label.
CORE_NUTRIENTS: tuple[str, ...] = ("kcal", "protein", "fat", "carbs")

# The one wire name measured in kcal rather than grams.
ENERGY_NUTRIENT = "kcal"

NUTRIENT_UNIT = "g"
ENERGY_UNIT = "kcal"
