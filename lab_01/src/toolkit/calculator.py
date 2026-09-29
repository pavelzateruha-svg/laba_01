from decimal import Decimal, getcontext, ROUND_HALF_UP, ROUND_FLOOR, InvalidOperation
from toolkit.errors import (
    EmptyVirazenieError,
    InvalidCharacterError,
    MissingOperandError,
    DivisionByZeroError,
)

getcontext().prec = 28
getcontext().rounding = ROUND_HALF_UP


def get_priority(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/', '%', '//'):
        return 2
    return 0


def to_rpn(massiv):
    stek = []
    output = []
    ops = {"+", "-", "*", "/", "%", "//", ")", "("}

    for current in massiv:
        if current not in ops:
            output.append(current)
        elif current == "(":
            stek.append(current)
        elif current == ")":
            while stek and stek[-1] != "(":
                output.append(stek.pop())
            if stek and stek[-1] == "(":
                stek.pop()
        else:
            while stek and stek[-1] != "(" and get_priority(stek[-1]) >= get_priority(current):
                output.append(stek.pop())
            stek.append(current)

    while len(stek) != 0:
        output.append(stek.pop())

    return output


def validate(string):
    if not string or not string.strip():
        raise EmptyVirazenieError("Выражение не может быть пустым")

    allowed = set("0123456789.+-*/%() ")
    for char in string:
        if char not in allowed:
            raise InvalidCharacterError(f"Недопустимый символ: '{char}'")

    balance = 0
    for char in string:
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
        if balance < 0:
            raise InvalidCharacterError("Лишняя закрывающая скобка")
    if balance != 0:
        raise InvalidCharacterError("Несбалансированные скобки")


def tokenizator(string):
    tokens = []
    single_char = "*%()"
    first_char_ops = "/"
    second_char_ops = "/"
    flag_operand = 0
    flag_operation = 0

    for current in string:
        if current == " ":
            continue

        if current in single_char:
            flag_operation = 0
            flag_operand = 0
            tokens.append(current)

        elif current in "+-":
            is_unary = False
            if len(tokens) == 0:
                is_unary = True
            else:
                last_token = tokens[-1]
                if last_token in ("(", "+", "-", "*", "/", "%", "//"):
                    is_unary = True

            if is_unary:
                flag_operand = 1
                tokens.append(current)
            else:
                flag_operation = 0
                flag_operand = 0
                tokens.append(current)

        elif (current in first_char_ops) and flag_operation == 0:
            flag_operation = 1
            flag_operand = 0
            tokens.append(current)

        elif (current in second_char_ops) and flag_operation == 1:
            flag_operation = 0
            tokens[-1] += current

        else:
            if flag_operand == 0:
                flag_operand = 1
                tokens.append(current)
            else:
                tokens[-1] += current

    return to_rpn(tokens)


def calc(string):
    # 1. Validation
    validate(string)

    # 2. Tokenization + RPN
    massiv = tokenizator(string)

    if len(massiv) == 0:
        raise MissingOperandError("Не найдено операндов в выражении")

    # 3. Calculation
    stek = []
    ops = {"+", "-", "*", "/", "%", "//"}

    for current in massiv:
        if current not in ops:
            try:
                stek.append(Decimal(current))
            except InvalidOperation:
                raise InvalidCharacterError(f"Некорректное число: '{current}'")
        else:
            if len(stek) < 2:
                raise MissingOperandError("Недостаточно операндов для операции")
            right = stek.pop()
            left = stek.pop()

            if current == "+":
                stek.append(left + right)
            elif current == "-":
                stek.append(left - right)
            elif current == "*":
                stek.append(left * right)
            elif current == "/":
                if right == 0:
                    raise DivisionByZeroError("Деление на ноль")

                stek.append(left / right)
            elif current == "//":
                if right == 0:
                    raise DivisionByZeroError("Деление на ноль")
                division = left / right
                result = division.to_integral_value(rounding=ROUND_FLOOR)
                stek.append(result)
            elif current == "%":
                if right == 0:
                    raise DivisionByZeroError("Деление на ноль")
                stek.append(left % right)

    if len(stek) != 1:
        raise MissingOperandError("Некорректное выражение")

    result = stek[0]

    if result == 0:
        return abs(result)

    return result