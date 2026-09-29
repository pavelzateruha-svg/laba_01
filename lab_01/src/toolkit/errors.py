class ToolkitError(Exception):
    pass


class EmptyVirazenieError(ToolkitError):
    pass


class InvalidCharacterError(ToolkitError):
    pass


class MissingOperandError(ToolkitError):
    pass


class DivisionByZeroError(ToolkitError):
    pass


class UnknownUnitError(ToolkitError):
    pass


class NesovmestimieUnitsError(ToolkitError):
    pass


class InvalidValueError(ToolkitError):
    pass