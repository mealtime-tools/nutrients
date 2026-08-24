from mealtime_nutrients.energy import (
    KJ_PER_KCAL,
    kcal_from_kj,
    kj_from_kcal,
)


def test_constant_is_the_thermochemical_definition():
    assert KJ_PER_KCAL == 4.184


def test_kcal_from_kj_shrinks_the_figure():
    # A 2000 kJ label is roughly 478 kcal, not roughly 8368.
    assert round(kcal_from_kj(2000), 1) == 478.0


def test_kj_from_kcal_grows_the_figure():
    assert round(kj_from_kcal(478.0), 0) == 2000


def test_round_trip_from_kj():
    assert kj_from_kcal(kcal_from_kj(1234.5)) == 1234.5


def test_round_trip_from_kcal():
    assert kcal_from_kj(kj_from_kcal(295.05)) == 295.05


def test_rounded_reciprocal_is_not_reintroduced():
    # 0.239006 was in use and disagrees with the exact reciprocal.
    assert 1 / KJ_PER_KCAL != 0.239006
    assert round(1 / KJ_PER_KCAL, 6) == 0.239006
