import pytest
from toolkit.converter import convert
from toolkit.errors import (
    UnknownUnitError,
    IncompatibleUnitsError,
    InvalidValueError,
)


# === Позитивные тесты для конвертера ===

def test_cm_to_m():
    """Сантиметры в метры"""
    assert convert(100, "cm", "m") == 1.0


def test_m_to_km():
    """Метры в километры"""
    assert convert(1000, "m", "km") == 1.0


def test_mm_to_cm():
    """Миллиметры в сантиметры"""
    assert convert(10, "mm", "cm") == 1.0


def test_g_to_kg():
    """Граммы в килограммы"""
    assert convert(1000, "g", "kg") == 1.0


def test_celsius_to_fahrenheit():
    """Цельсий в Фаренгейт (0°C = 32°F)"""
    assert convert(0, "c", "f") == 32.0


def test_celsius_to_kelvin():
    """Цельсий в Кельвин (0°C = 273.15K)"""
    assert convert(0, "c", "k") == 273.15


def test_case_insensitive():
    """Регистр не учитывается"""
    assert convert(100, "CM", "M") == 1.0


# === Негативные тесты для конвертера ===

def test_unknown_unit_from():
    """Неизвестная исходная единица"""
    with pytest.raises(UnknownUnitError):
        convert(100, "xyz", "m")


def test_unknown_unit_to():
    """Неизвестная целевая единица"""
    with pytest.raises(UnknownUnitError):
        convert(100, "m", "xyz")


def test_incompatible_units():
    """Несовместимые единицы (длина в массу)"""
    with pytest.raises(IncompatibleUnitsError):
        convert(100, "m", "kg")


def test_temperature_below_absolute_zero():
    """Температура ниже абсолютного нуля"""
    with pytest.raises(InvalidValueError):
        convert(-300, "c", "k")


def test_invalid_value():
    """Неверное числовое значение"""
    with pytest.raises(InvalidValueError):
        convert("abc", "m", "km")