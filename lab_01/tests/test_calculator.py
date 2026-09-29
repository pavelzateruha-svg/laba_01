import pytest
from toolkit.calculator import calc
from toolkit.errors import (
    EmptyVirazenieError,
    InvalidCharacterError,
    DivisionByZeroError,
)

def test_simple_addition():
    assert str(calc("2 + 2")) == "4"


def test_subtraction():
    assert str(calc("10 - 3")) == "7"


def test_multiplication():
    assert str(calc("5 * 6")) == "30"


def test_division():
    assert str(calc("15 / 3")) == "5"


def test_priority_operations():
    assert str(calc("2 + 3 * 4")) == "14"


def test_parentheses():
    assert str(calc("(2 + 3) * 4")) == "20"


def test_unary_minus():
    assert str(calc("-5 + 3")) == "-2"


def test_unary_plus():
    assert str(calc("+5 + 3")) == "8"


def test_floor_division():
    assert str(calc("10 // 3")) == "3"


def test_floor_division_negative():
    assert str(calc("4 // -5")) == "-1"


def test_modulo():
    assert str(calc("10 % 3")) == "1"


def test_decimal_precision():
    assert str(calc("0.1 + 0.2")) == "0.3"


def test_complex_expression():
    assert str(calc("(4 + 5) * 67 * (23 // -52)")) == "-603"


def test_empty_expression():
    with pytest.raises(EmptyVirazenieError):
        calc("")


def test_only_spaces():
    with pytest.raises(EmptyVirazenieError):
        calc("   ")


def test_invalid_character():
    with pytest.raises(InvalidCharacterError):
        calc("2 + a")


def test_unbalanced_parentheses_open():
    with pytest.raises(InvalidCharacterError):
        calc("(2 + 3")


def test_unbalanced_parentheses_close():
    with pytest.raises(InvalidCharacterError):
        calc("2 + 3)")


def test_division_by_zero():
    with pytest.raises(DivisionByZeroError):
        calc("5 / 0")


def test_floor_division_by_zero():
    with pytest.raises(DivisionByZeroError):
        calc("5 // 0")


def test_modulo_by_zero():
    with pytest.raises(DivisionByZeroError):
        calc("5 % 0")