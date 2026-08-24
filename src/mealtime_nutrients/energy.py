"""The one energy conversion the mealtime tools need.

Labels outside the US print kilojoules; every tool stores kilocalories. This
module is the only place that ratio is written down.
"""

# Exactly 4.184 J. Divide by it; the old 0.239006 reciprocal was wrong.
KJ_PER_KCAL = 4.184


def kcal_from_kj(kilojoules: float) -> float:
    """Kilocalories for a figure published in kilojoules."""
    return kilojoules / KJ_PER_KCAL


def kj_from_kcal(kilocalories: float) -> float:
    """Kilojoules for a figure published in kilocalories."""
    return kilocalories * KJ_PER_KCAL
