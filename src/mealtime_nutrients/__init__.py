"""The nutrient vocabulary and energy constant shared by the mealtime tools.

A data package: no parsing, no validation, no dependencies.
"""

from mealtime_nutrients.energy import (
    KJ_PER_KCAL,
    kcal_from_kj,
    kj_from_kcal,
)
from mealtime_nutrients.vocabulary import (
    API_FIELDS,
    API_NUTRIENTS,
    CORE_NUTRIENTS,
    ENERGY_NUTRIENT,
    ENERGY_UNIT,
    NUTRIENT_TYPES,
    NUTRIENT_UNIT,
    NUTRIENTS,
    UNREACHABLE_NUTRIENT_TYPES,
)

__all__ = [
    "API_FIELDS",
    "API_NUTRIENTS",
    "CORE_NUTRIENTS",
    "ENERGY_NUTRIENT",
    "ENERGY_UNIT",
    "KJ_PER_KCAL",
    "NUTRIENTS",
    "NUTRIENT_TYPES",
    "NUTRIENT_UNIT",
    "UNREACHABLE_NUTRIENT_TYPES",
    "kcal_from_kj",
    "kj_from_kcal",
]
