class ToolkitError(Exception):
    pass


class EmptyExpressionError(ToolkitError):
    pass


class InvalidCharacterError(ToolkitError):
    pass


class MissingOperandError(ToolkitError):
    pass


class ConsecutiveOperatorsError(ToolkitError):
    pass


class DivisionByZeroError(ToolkitError):
    pass


class UnknownUnitError(ToolkitError):
    pass


class IncompatibleUnitsError(ToolkitError):
    pass


class InvalidValueError(ToolkitError):
    pass