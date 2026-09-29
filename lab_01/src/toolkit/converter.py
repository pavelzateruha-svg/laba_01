from decimal import Decimal, ROUND_HALF_UP
from toolkit.errors import (
    UnknownUnitError,
    IncompatibleUnitsError,
    InvalidValueError,
)

length_to_base = {
    "mm": Decimal("0.001"),
    "cm": Decimal("0.01"),
    "m":  Decimal("1"),
    "km": Decimal("1000"),
}

mass_to_base = {
    "g":  Decimal("0.001"),
    "kg": Decimal("1"),
}

temperature_units = {"c", "f", "k"}

unit_groups = {
    "length": set(length_to_base.keys()),
    "mass":   set(mass_to_base.keys()),
    "temp":   temperature_units,
}


def _get_unit_group(unit: str) -> str | None:
    unit_lower = unit.lower()
    for group, units in unit_groups.items():
        if unit_lower in units:
            return group
    return None


def _celsius_to_kelvin(c: Decimal) -> Decimal:
    return c + Decimal("273.15")


def _kelvin_to_celsius(k: Decimal) -> Decimal:
    return k - Decimal("273.15")


def _fahrenheit_to_kelvin(f: Decimal) -> Decimal:
    return (f - Decimal("32")) * Decimal("5") / Decimal("9") + Decimal("273.15")


def _kelvin_to_fahrenheit(k: Decimal) -> Decimal:
    return (k - Decimal("273.15")) * Decimal("9") / Decimal("5") + Decimal("32")


def _convert_temperature(value: Decimal, from_unit: str, to_unit: str) -> Decimal:
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


def convert(value, from_unit: str, to_unit: str) -> float:
    try:
        value = Decimal(str(value))
    except Exception:
        raise InvalidValueError(f"Неверное числовое значение: '{value}'")

    from_u = from_unit.lower()
    to_u = to_unit.lower()

    from_group = _get_unit_group(from_u)
    to_group = _get_unit_group(to_u)

    if from_group is None:
        raise UnknownUnitError(f"Неизвестная единица: '{from_unit}'")
    if to_group is None:
        raise UnknownUnitError(f"Неизвестная единица: '{to_unit}'")

    if from_group != to_group:
        raise IncompatibleUnitsError(
            f"Несовместимые единицы: '{from_unit}' ({from_group}) и '{to_unit}' ({to_group})"
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