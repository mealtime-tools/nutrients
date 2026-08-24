from decimal import Decimal

from mealtime_nutrients.energy import (
    KJ_PER_KCAL,
    kcal_from_kj,
    kj_from_kcal,
)


def test_constant_is_the_thermochemical_definition():
    assert KJ_PER_KCAL == Decimal("4.184")


def test_the_constant_is_exact_where_a_float_would_not_be():
    # The value a float actually holds, which is what this type avoids.
    assert Decimal(4.184) != KJ_PER_KCAL
    assert str(KJ_PER_KCAL) == "4.184"


def test_kcal_from_kj_shrinks_the_figure():
    # A 2000 kJ label is roughly 478 kcal, not roughly 8368.
    assert round(kcal_from_kj(2000), 1) == Decimal("478.0")


def test_kj_from_kcal_grows_the_figure():
    assert round(kj_from_kcal(478), 0) == Decimal("2000")


def test_round_trip_from_kj():
    assert kj_from_kcal(kcal_from_kj(1234.5)) == Decimal("1234.5")


def test_round_trip_from_kcal():
    assert kcal_from_kj(kj_from_kcal("295.05")) == Decimal("295.05")


def test_a_decimal_caller_needs_no_conversion():
    # The AFCD importer holds Decimal, and could not use a float constant.
    assert kcal_from_kj(Decimal("531")) == Decimal("531") / KJ_PER_KCAL


def test_a_float_reads_back_as_the_figure_it_was_written_as():
    assert kcal_from_kj(0.1) == Decimal("0.1") / KJ_PER_KCAL


def test_rounded_reciprocal_is_not_reintroduced():
    # 0.239006 was in use and disagrees with the exact reciprocal.
    assert 1 / KJ_PER_KCAL != Decimal("0.239006")
    assert round(1 / KJ_PER_KCAL, 6) == Decimal("0.239006")
