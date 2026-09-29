import pytest
from toolkit.calculator import calc
from toolkit.errors import (
    EmptyExpressionError,
    InvalidCharacterError,
    MissingOperandError,
    DivisionByZeroError,
)


# === Позитивные тесты для калькулятора (7 штук) ===

def test_simple_addition():
    """Простое сложение"""
    assert str(calc("2 + 2")) == "4"


def test_subtraction():
    """Вычитание"""
    assert str(calc("10 - 3")) == "7"


def test_multiplication():
    """Умножение"""
    assert str(calc("5 * 6")) == "30"


def test_division():
    """Деление"""
    assert str(calc("15 / 3")) == "5"


def test_priority_operations():
    """Приоритет умножения над сложением"""
    assert str(calc("2 + 3 * 4")) == "14"


def test_parentheses():
    """Скобки меняют приоритет"""
    assert str(calc("(2 + 3) * 4")) == "20"


def test_unary_minus():
    """Унарный минус"""
    assert str(calc("-5 + 3")) == "-2"


def test_unary_plus():
    """Унарный плюс"""
    assert str(calc("+5 + 3")) == "8"


def test_floor_division():
    """Целочисленное деление"""
    assert str(calc("10 // 3")) == "3"


def test_floor_division_negative():
    """Целочисленное деление с отрицательным числом"""
    assert str(calc("4 // -5")) == "-1"


def test_modulo():
    """Остаток от деления"""
    assert str(calc("10 % 3")) == "1"


def test_decimal_precision():
    """Точность Decimal (0.1 + 0.2 = 0.3)"""
    assert str(calc("0.1 + 0.2")) == "0.3"


def test_complex_expression():
    """Сложное выражение со скобками"""
    assert str(calc("(4 + 5) * 67 * (23 // -52)")) == "-603"


# === Негативные тесты для калькулятора (5 штук) ===

def test_empty_expression():
    """Пустое выражение"""
    with pytest.raises(EmptyExpressionError):
        calc("")


def test_only_spaces():
    """Только пробелы"""
    with pytest.raises(EmptyExpressionError):
        calc("   ")


def test_invalid_character():
    """Недопустимый символ"""
    with pytest.raises(InvalidCharacterError):
        calc("2 + a")


def test_unbalanced_parentheses_open():
    """Незакрытая скобка"""
    with pytest.raises(InvalidCharacterError):
        calc("(2 + 3")


def test_unbalanced_parentheses_close():
    """Лишняя закрывающая скобка"""
    with pytest.raises(InvalidCharacterError):
        calc("2 + 3)")


def test_division_by_zero():
    """Деление на ноль"""
    with pytest.raises(DivisionByZeroError):
        calc("5 / 0")


def test_floor_division_by_zero():
    """Целочисленное деление на ноль"""
    with pytest.raises(DivisionByZeroError):
        calc("5 // 0")


def test_modulo_by_zero():
    """Остаток от деления на ноль"""
    with pytest.raises(DivisionByZeroError):
        calc("5 % 0")