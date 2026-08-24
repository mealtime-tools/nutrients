import re

from mealtime_nutrients.labels import row_pattern
from mealtime_nutrients.vocabulary import NUTRIENTS


def _matches(name: str, label: str) -> bool:
    return re.search(row_pattern(name), label, re.IGNORECASE) is not None


def test_a_single_word_name_matches_its_row():
    assert _matches("calcium", "Calcium")
    assert _matches("iron", "Iron (mg)")


def test_an_underscore_matches_however_the_label_separates_it():
    for label in ("Vitamin B12", "Vitamin-B12", "VitaminB12"):
        assert _matches("vitamin_b12", label), label


def test_a_name_does_not_match_a_neighbours_row():
    assert not _matches("vitamin_b6", "Vitamin B12")
    assert not _matches("vitamin_b12", "Vitamin B6")
    assert not _matches("folate", "Folic Acid")


def test_only_the_fat_family_claims_another_names_label():
    """First match wins in a parser, so every overlap needs known ordering.

    The fat names nest -- polyunsaturated contains unsaturated contains
    saturated contains fat -- and a parser orders them longest first. A name
    added upstream that overlaps anything else would be a new ambiguity, so
    this fails rather than letting one appear unnoticed.
    """
    overlaps = {}
    for name in NUTRIENTS:
        label = name.replace("_", " ")
        claimants = [
            other
            for other in NUTRIENTS
            if other != name and _matches(other, label)
        ]
        if claimants:
            overlaps[name] = sorted(claimants)

    assert overlaps == {
        "monounsaturated_fat": ["fat", "saturated_fat", "unsaturated_fat"],
        "polyunsaturated_fat": ["fat", "saturated_fat", "unsaturated_fat"],
        "saturated_fat": ["fat"],
        "trans_fat": ["fat"],
        "unsaturated_fat": ["fat", "saturated_fat"],
    }
