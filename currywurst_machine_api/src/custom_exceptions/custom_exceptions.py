class InsuficientFundsException(Exception):
    """Exception raised when funds are not sufficient."""


class NotExactChangeAvailableException(Exception):
    """Exception raised when there are not exact changes available."""


class EuroPrecisionMoreThanTwoDecimalsException(ValueError):
    """Exception raised when the price passed is not a two decimal float."""


class EuroQuantityNotIntegerException(ValueError):
    """Exception raised when the euro quantity passed is not an integers."""


class InvalidCoinNoteException(ValueError):
    """Exception raised when invalid coin/note was inserted."""
