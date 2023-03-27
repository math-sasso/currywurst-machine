from typing import Dict, List
from .custom_exceptions import (
    InsuficientInsertedMoneyException,
    NotExactChangeAvailableException,
)

class CurrywurstMachine:
    """
    CurrywurstMachine machine class responsible for manage the money
    it receives and return the optimized number of coins to the cient.
    """
    COIN_RESERVATORY_PHYSICAL_LIMIT = 500

    def __init__(self) -> None:
        """Constructor
        """

        self.coins = {
            2: self.COIN_RESERVATORY_PHYSICAL_LIMIT,
            1: self.COIN_RESERVATORY_PHYSICAL_LIMIT,
            0.5: self.COIN_RESERVATORY_PHYSICAL_LIMIT,
            0.2: self.COIN_RESERVATORY_PHYSICAL_LIMIT,
            0.1: self.COIN_RESERVATORY_PHYSICAL_LIMIT,
            0.05: self.COIN_RESERVATORY_PHYSICAL_LIMIT,
            0.02: self.COIN_RESERVATORY_PHYSICAL_LIMIT,
            0.01: self.COIN_RESERVATORY_PHYSICAL_LIMIT,
        }

        self.notes = {
            5: 0,
            10: 0,
            20: 0,
            50: 0,
            100: 0,
            200: 0,
            500: 0,
        }
     
    
    def refill_coins(self):
        """Refill the coins to the maximum phisical limit of the machine
        """
        self.coins = {
            2: self.COIN_RESERVATORY_PHYSICAL_LIMIT,
            1: self.COIN_RESERVATORY_PHYSICAL_LIMIT,
            0.5: self.COIN_RESERVATORY_PHYSICAL_LIMIT,
            0.2: self.COIN_RESERVATORY_PHYSICAL_LIMIT,
            0.1: self.COIN_RESERVATORY_PHYSICAL_LIMIT,
            0.05: self.COIN_RESERVATORY_PHYSICAL_LIMIT,
            0.02: self.COIN_RESERVATORY_PHYSICAL_LIMIT,
            0.01: self.COIN_RESERVATORY_PHYSICAL_LIMIT,
        }

    def _get_eur_notes_inserted(self, eur_inserted:Dict)->Dict[float,int]:
        """Method responsible for separating only the Dict of notes
        in the dict of Euros inserted

        Args:
            eur_inserted ('Dict'): Dict with {euro value:quantity} pairs for coins and notes.

        Returns:
            Dict[float,int]: Dict with {euro value:quantity} pairs only for notes.
        """
        notes = {}

        for key, value in eur_inserted.items():
            if key > 2:
                notes[key] = value
        
        return notes
    
    def _check_if_coin_is_available(self, coin: float, coins_dict:Dict)->bool:
        """Check if coin is available in the machine

        Args:
            coin (float): The specific coin
            coins_dict (Dict): Dict of coins

        Returns:
            bool: True if available else False
        """
        
        if coins_dict[coin] == 0:
            return False
        return True

    def _get_coin_possitilities(self)->List[float]:
        """A function to simplifies the coins possiblities to be returned

        Returns:
            List[float]: List of coins possibilities
        """
        return list(self.coins.keys())
    
    def _calculate_required_change(self, currywurst_price: float, eur_inserted: Dict)->float:
        """Calculate the total change

        Args:
            currywurst_price (float): Currywurst price
            eur_inserted (Dict): Dict with {euro value:quantity} pairs for coins and notes.

        Raises:
            InsuficientInsertedMoneyException: _description_

        Returns:
            float: Total change to be returned to the user
        """

        # Calculate the amount of change required
        amount_inserted = sum(k * v for k, v in eur_inserted.items())
        change = amount_inserted - currywurst_price

        # If the user inserted insufficient funds, raise an exception
        if change < 0:
            raise InsuficientInsertedMoneyException("Insufficient money inserted")

        return change

    def _check_if_exact_change_is_possible(self, change: float)->None:
        """Check if change can be exactly zero with the coins available.

        Args:
            change (float): The calculated change

        Raises:
            NotExactChangeAvailableException: Only raised if change different of zero
        """
        # Check if exact change was given
        if change != 0:
            raise NotExactChangeAvailableException("Exact change not possible")

    def return_coins(self, currywurst_price: float, eur_inserted: Dict[float, int])->Dict[float, int]:
        """ The currywurst machine accepts any coins or banknotes but returns only
        coins and works only with EUR currency.

        Args:
            currywurst_price (float): Price of the Currywurst
            eur_inserted (Dict[float, int]): Dict with {euro value:quantity} pairs for coins and notes.

        Returns:
            eur_inserted (Dict[float, int]): Dict with {euro value:quantity} pairs for coins that should be 
            returned tothe client
        """

        # Calculates change and raise exception if funds are not suficient
        change = self._calculate_required_change(
            currywurst_price=currywurst_price, eur_inserted=eur_inserted
        )

        
        # Calculate the quantity of each coin required
        coin_counts = {}
        coins_copy = self.coins.copy()
        for coin in sorted(self._get_coin_possitilities(),reverse=True):
            coin_counts[coin] = 0
            while change >= coin and self._check_if_coin_is_available(coin=coin,coins_dict=coins_copy):
                # if change <0.06:
                #     import pdb;pdb.set_trace()
                coin_counts[coin] +=1
                coins_copy[coin] -=1
                change -= coin
                change = round(change,2)

        # check if exact change is possible
        self._check_if_exact_change_is_possible(change)

        # update attributes
        self.coins = coins_copy
        self.notes = self._get_eur_notes_inserted(eur_inserted=eur_inserted)
        
        return coin_counts