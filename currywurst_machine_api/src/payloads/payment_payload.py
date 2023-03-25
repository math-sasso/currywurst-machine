from decimal import Decimal
from typing import Dict
from pydantic import BaseModel, validator, root_validator




class Payment(BaseModel):
    eur_inserted: Dict[float, int] = {500.00: 0,200.00: 0,100.00: 0,50.00: 0,20.00: 0, 10.00: 0,5.00: 0,2.00: 0, 1.00: 0, 0.50: 0, 0.20: 0, 0.10: 0, 0.05: 0, 0.02: 0, 0.01: 0}
    currywurst_price: float = 1.23

    @validator("currywurst_price")
    def validate_price(cls, value):
        if not isinstance(value, float):
            raise ValueError("Price must be a float")
        if Decimal(str(value)).as_tuple().exponent != -2:
            raise ValueError("Price must have exactly 2 decimal places")
        return value

    @validator("eur_inserted")
    def validate_eur_inserted(cls, value):
        # Define the allowed Euro coin values
        allowed_amounts = [500.00,200.00,100.00,50.00,20.00,10.00,5.00,2.00, 1.00, 0.50, 0.20, 0.10, 0.05, 0.02, 0.01]

        # Check that only the allowed coins/notes were inserted
        for money in value:
            if money not in allowed_amounts:
                raise ValueError(f"Invalid coin/note value: {money}")

        # Return the validated dictionary
        return value

    # @root_validator
    # def validate_payment(cls, values):
    #     # Get the user-inserted coins and the price
    #     eur_inserted = values.get("eur_inserted")
    #     price = values.get("currywurst_price")

    #     # Check that the sum of the inserted coins is equal to or greater than the price
    #     import pdb;pdb.set_trace()
    #     if sum(k*v for k,v in eur_inserted.items()) < price:
    #         raise ValueError("Not enough money inserted")

    #     # Return the values dictionary
    #     return values