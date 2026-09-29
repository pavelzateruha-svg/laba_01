from decimal import Decimal, ROUND_HALF_UP
from toolkit.errors import (
    UnknownUnitError,
    NesovmestimieUnitsError,
    InvalidValueError,
)

length_to_base = {
    "mm": Decimal("0.001"),
    "cm": Decimal("0.01"),
    "m": Decimal("1"),
    "km": Decimal("1000"),
}

mass_to_base = {
    "g": Decimal("0.001"),
    "kg": Decimal("1"),
}

temperature_units = {"c", "f", "k"}

unit_groups = {
    "length": set(length_to_base.keys()),
    "mass": set(mass_to_base.keys()),
    "temp": temperature_units,
}


def _get_unit_group(unit):
    unit_lower = unit.lower()
    for group, units in unit_groups.items():
        if unit_lower in units:
            return group
    return None


def _celsius_to_kelvin(c):
    return c + Decimal("273.15")


def _kelvin_to_celsius(k):
    return k - Decimal("273.15")


def _fahrenheit_to_kelvin(f):
    return (f - Decimal("32")) * Decimal("5") / Decimal("9") + Decimal("273.15")


def _kelvin_to_fahrenheit(k):
    return (k - Decimal("273.15")) * Decimal("9") / Decimal("5") + Decimal("32")


def _convert_temperature(value, from_unit, to_unit):
    from_u = from_unit.lower()
    to_u = to_unit.lower()

    if from_u == "c":
        kelvin = _celsius_to_kelvin(value)
    elif from_u == "f":
        kelvin = _fahrenheit_to_kelvin(value)
    else:
        kelvin = value

    if kelvin < 0:
        raise InvalidValueError("Температура ниже абсолютного нуля")

    if to_u == "c":
        return _kelvin_to_celsius(kelvin)
    elif to_u == "f":
        return _kelvin_to_fahrenheit(kelvin)
    else:
        return kelvin


def convert(value, from_unit, to_unit):
    try:
        value = Decimal(str(value))
    except Exception:
        raise InvalidValueError("Неверное числовое значение: " + str(value))

    from_u = from_unit.lower()
    to_u = to_unit.lower()

    from_group = _get_unit_group(from_u)
    to_group = _get_unit_group(to_u)

    if from_group is None:
        raise UnknownUnitError("Неизвестная единица: " + from_unit)
    if to_group is None:
        raise UnknownUnitError("Неизвестная единица: " + to_unit)

    if from_group != to_group:
        raise NesovmestimieUnitsError(
            "Несовместимые единицы: " + from_unit + " и " + to_unit
        )

    if from_group == "temp":
        result = _convert_temperature(value, from_u, to_u)
    else:
        if from_group == "length":
            table = length_to_base
        else:
            table = mass_to_base

        base_value = value * table[from_u]
        result = base_value / table[to_u]

    return float(result.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))