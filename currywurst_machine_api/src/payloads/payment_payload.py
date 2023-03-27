from decimal import Decimal
from typing import Dict
from pydantic import BaseModel, validator
from ..custom_exceptions import (
    EuroPrecisionMoreThanTwoDecimalsException,
    InvalidCoinNoteException,
    EuroQuantityNotIntegerException,
)

from ..settings import EURO_ACCEPTABLE_VALUES

class Payment(BaseModel):
    eur_inserted: Dict[float, int] = {value:0 for value in EURO_ACCEPTABLE_VALUES}
    currywurst_price: float = 1.23

    @validator("currywurst_price")
    def validate_price(cls, value):
        if (
            not isinstance(value, float)
            or Decimal(str(value)).as_tuple().exponent != -2
        ):
            raise EuroPrecisionMoreThanTwoDecimalsException(
                "Euro must be a float with exactly 2 decimal places"
            )
        return value

    @validator("eur_inserted")
    def validate_eur_inserted(cls, value):
        # Define the allowed Euro coin values
        
        # Check that only the allowed coins/notes were inserted
        for money, qtd in value.items():
            if not isinstance(qtd, int):
                raise EuroQuantityNotIntegerException(
                    "Euro piece quantity must be an integer"
                )
            if not isinstance(money, (float)) or money != round(money, 2):
                raise EuroPrecisionMoreThanTwoDecimalsException(
                    "Euro must be a float with at most 2 decimal values"
                )
            if money not in EURO_ACCEPTABLE_VALUES:
                raise InvalidCoinNoteException(f"Invalid coin/note value: {money}")

        # Return the validated dictionary
        return value
