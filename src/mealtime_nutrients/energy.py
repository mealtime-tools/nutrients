"""The one energy conversion the mealtime tools need.

Labels outside the US print kilojoules; every tool stores kilocalories. This
module is the only place that ratio is written down.
"""

from decimal import Decimal

# Exactly 4.184 J: a definition, not a measurement, so not a float.
KJ_PER_KCAL = Decimal("4.184")

Energy = Decimal | int | str | float


def _exact(value: Energy) -> Decimal:
    """One figure as the decimal it was written as.

    A float goes through `str` so it reads back as the figure a label stated
    rather than the binary approximation stored for it: 0.1 is Decimal("0.1"),
    not Decimal("0.1000000000000000055511151231257827").
    """
    return Decimal(str(value)) if isinstance(value, float) else Decimal(value)


def kcal_from_kj(kilojoules: Energy) -> Decimal:
    """Kilocalories for a figure published in kilojoules."""
    return _exact(kilojoules) / KJ_PER_KCAL


def kj_from_kcal(kilocalories: Energy) -> Decimal:
    """Kilojoules for a figure published in kilocalories."""
    return _exact(kilocalories) * KJ_PER_KCAL
