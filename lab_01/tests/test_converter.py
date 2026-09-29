import pytest
from toolkit.converter import convert
from toolkit.errors import (
    UnknownUnitError,
    NesovmestimieUnitsError,
    InvalidValueError,
)

def test_cm_to_m():
    assert convert(100, "cm", "m") == 1.0


def test_m_to_km():
    assert convert(1000, "m", "km") == 1.0


def test_mm_to_cm():
    assert convert(10, "mm", "cm") == 1.0


def test_g_to_kg():
    assert convert(1000, "g", "kg") == 1.0


def test_celsius_to_fahrenheit():
    assert convert(0, "c", "f") == 32.0


def test_celsius_to_kelvin():
    assert convert(0, "c", "k") == 273.15


def test_case_insensitive():
    assert convert(100, "CM", "M") == 1.0


def test_unknown_unit_from():
    with pytest.raises(UnknownUnitError):
        convert(100, "xyz", "m")


def test_unknown_unit_to():
    with pytest.raises(UnknownUnitError):
        convert(100, "m", "xyz")


def test_incompatible_units():
    with pytest.raises(NesovmestimieUnitsError):
        convert(100, "m", "kg")


def test_temperature_below_absolute_zero():
    with pytest.raises(InvalidValueError):
        convert(-300, "c", "k")


def test_invalid_value():
    with pytest.raises(InvalidValueError):
        convert("abc", "m", "km")