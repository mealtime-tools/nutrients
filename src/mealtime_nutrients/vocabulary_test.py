from mealtime_nutrients.vocabulary import (
    API_FIELDS,
    API_NUTRIENTS,
    CORE_NUTRIENTS,
    ENERGY_NUTRIENT,
    ENERGY_UNIT,
    NUTRIENT_TYPES,
    NUTRIENT_UNIT,
    NUTRIENTS,
    OPTIONAL_NUTRIENTS,
    UNREACHABLE_NUTRIENT_TYPES,
)

# 39 enum members - 1 unreachable + 3 dedicated wire names = 41.
EXPECTED_TYPE_COUNT = 39
EXPECTED_WIRE_COUNT = 41

# FORMAT.md's seven. An earlier draft shipped API names and omitted four.
FORMAT_MD_NAMES = (
    "kcal",
    "protein",
    "fat",
    "carbs",
    "fiber",
    "sodium",
    "sugar",
)


def test_format_md_names_are_all_wire_names():
    for name in FORMAT_MD_NAMES:
        assert name in NUTRIENTS


def test_vocabulary_size():
    assert len(NUTRIENT_TYPES) == EXPECTED_TYPE_COUNT
    assert len(NUTRIENTS) == EXPECTED_WIRE_COUNT


def test_names_are_unique():
    assert len(set(NUTRIENTS)) == len(NUTRIENTS)
    assert len(set(NUTRIENT_TYPES)) == len(NUTRIENT_TYPES)


def test_names_are_in_canonical_wire_order():
    """The first seven are every share link's key order and cannot move."""
    assert NUTRIENTS[:7] == (
        "kcal",
        "protein",
        "fat",
        "carbs",
        "fiber",
        "sodium",
        "sugar",
    )
    tail = list(NUTRIENTS[7:])
    assert tail == sorted(tail)
    assert list(NUTRIENT_TYPES) == sorted(NUTRIENT_TYPES)


def test_the_optional_names_are_everything_but_the_core():
    assert OPTIONAL_NUTRIENTS == NUTRIENTS[len(CORE_NUTRIENTS) :]
    assert not set(OPTIONAL_NUTRIENTS) & set(CORE_NUTRIENTS)


def test_wire_names_are_lowercase():
    for name in NUTRIENTS:
        assert name == name.lower()
        assert name.replace("_", "").isalnum()


def test_api_names_are_uppercase():
    for name in NUTRIENT_TYPES:
        assert name == name.upper()


def test_mapping_is_total():
    # Exactly one destination per wire name; none unaccounted for.
    for name in NUTRIENTS:
        in_array = name in API_NUTRIENTS
        in_field = name in API_FIELDS
        assert in_array != in_field, name


def test_vocabulary_is_exactly_the_mapped_names():
    assert set(NUTRIENTS) == set(API_NUTRIENTS) | set(API_FIELDS)


def test_mapping_is_injective():
    destinations = list(API_NUTRIENTS.values()) + list(API_FIELDS.values())
    assert len(set(destinations)) == len(destinations)


def test_every_nutrient_type_is_reachable_except_the_documented_one():
    # Nothing storable may be unreachable except by justified allowlist.
    reachable = set(API_NUTRIENTS.values())
    assert reachable == set(NUTRIENT_TYPES) - UNREACHABLE_NUTRIENT_TYPES


def test_the_unreachable_allowlist_is_exactly_one_member():
    # Allowlisting means the nutrient cannot be logged at all: needs a real reason.
    assert UNREACHABLE_NUTRIENT_TYPES == frozenset({"CARBOHYDRATES"})


def test_unreachable_types_are_real_members():
    assert UNREACHABLE_NUTRIENT_TYPES <= set(NUTRIENT_TYPES)


def test_carbohydrates_is_not_a_second_wire_name_for_carbs():
    # The regression: both keys would send the figure to two API slots.
    assert "carbohydrates" not in NUTRIENTS
    assert "carbohydrates" not in API_NUTRIENTS
    assert API_FIELDS["carbs"] == "totalCarbohydrate"


# Spellings a future enum member might use to collide with a dedicated field.
DEDICATED_FIELD_DUPLICATES = {
    "energy": ("ENERGY", "CALORIES", "KCAL", "FOOD_ENERGY"),
    "totalFat": ("FAT", "TOTAL_FAT", "TOTAL_LIPID"),
    "totalCarbohydrate": (
        "CARBOHYDRATES",
        "CARBOHYDRATE",
        "TOTAL_CARBOHYDRATE",
    ),
}


def test_dedicated_fields_have_no_parallel_wire_route():
    for field, duplicates in DEDICATED_FIELD_DUPLICATES.items():
        present = [name for name in duplicates if name in NUTRIENT_TYPES]
        unreachable = set(present) <= UNREACHABLE_NUTRIENT_TYPES
        assert unreachable, f"{field} is reachable twice via {present}"


def test_no_total_fat_or_energy_member_exists():
    # No total-fat and no energy member, so `fat` and `kcal` cannot collide.
    assert "TOTAL_FAT" not in NUTRIENT_TYPES
    assert "FAT" not in NUTRIENT_TYPES
    for name in NUTRIENT_TYPES:
        assert "ENERG" not in name
        assert "CALORI" not in name


def test_fat_breakdowns_all_stay_reachable():
    # Subtypes of totalFat, not duplicates: not the CARBOHYDRATES hazard.
    for name in (
        "saturated_fat",
        "trans_fat",
        "monounsaturated_fat",
        "polyunsaturated_fat",
        "unsaturated_fat",
    ):
        assert API_NUTRIENTS[name] == name.upper()


def test_array_destinations_are_nutrient_types():
    for name, destination in API_NUTRIENTS.items():
        assert destination in NUTRIENT_TYPES, name


def test_non_identity_mappings():
    # Why this is a mapping rather than a list.
    assert API_NUTRIENTS["protein"] == "PROTEIN"
    assert API_NUTRIENTS["fiber"] == "DIETARY_FIBER"
    assert API_FIELDS["kcal"] == "energy"
    assert API_FIELDS["carbs"] == "totalCarbohydrate"
    assert API_FIELDS["fat"] == "totalFat"


def test_identity_mappings():
    for name in ("saturated_fat", "sodium", "sugar", "vitamin_b12"):
        assert API_NUTRIENTS[name] == name.upper()


def test_protein_is_array_eligible_but_carbs_and_fat_are_not():
    # protein goes to the array; kcal, carbs and fat to dedicated objects.
    assert "protein" in API_NUTRIENTS
    for name in ("kcal", "carbs", "fat"):
        assert name not in API_NUTRIENTS
        assert name in API_FIELDS


def test_core_nutrients():
    assert CORE_NUTRIENTS == ("kcal", "protein", "fat", "carbs")
    for name in CORE_NUTRIENTS:
        assert name in NUTRIENTS


def test_energy_is_a_wire_name_but_not_a_nutrient_type():
    assert ENERGY_NUTRIENT == "kcal"
    assert ENERGY_NUTRIENT in NUTRIENTS
    assert "ENERGY" not in NUTRIENT_TYPES
    assert ENERGY_NUTRIENT not in API_NUTRIENTS


def test_units():
    assert NUTRIENT_UNIT == "g"
    assert ENERGY_UNIT == "kcal"
