from typing import Dict
from .custom_exceptions import (
    InsuficientInsertedMoneyException,
    NotExactChangeAvailableException,
)

class CurrywurstMachine:
    

    def __init__(self) -> None:

        self.refil_value = 500

        self.coins = {
            2: self.refil_value,
            1: self.refil_value,
            0.5: self.refil_value,
            0.2: self.refil_value,
            0.1: self.refil_value,
            0.05: self.refil_value,
            0.02: self.refil_value,
            0.01: self.refil_value,
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
     
    def __get_eur_notes_inserted(self, eur_inserted:Dict)->Dict[float,int]:
        notes = {}

        for key, value in eur_inserted.items():
            if key > 2:
                notes[key] = value
        
        return notes
    
    def __check_if_coin_is_available(self, coin: float, coins_dict:Dict):
        if coins_dict[coin] == 0:
            return False
        return True
    
    def __get_empty_coin_dict(self):
        return {coin: 0 for coin in self.coins.keys()}

    def __get_coin_possitilities(self):
        return list(self.coins.keys())
    
    def __check_suficient_funds(self, currywurst_price: float, eur_inserted: Dict):
        # Calculate the amount of change required
        amount_inserted = sum(k * v for k, v in eur_inserted.items())
        change = amount_inserted - currywurst_price

        # If the user inserted insufficient funds, raise an exception
        if change < 0:
            raise InsuficientInsertedMoneyException("Insufficient money inserted")

        return change

    def __check_if_exact_change_available(self, change: float):
        # Check if exact change was given
        if change != 0:
            raise NotExactChangeAvailableException("Exact change not possible")

    def return_coins(self, currywurst_price: float, eur_inserted: Dict[float, int]):
        """
         The currywurst machine accepts any coins or banknotes but returns only
        coins and works only with EUR currency.
        """

        # Calculates change and raise exception if funds are not suficient
        change = self.__check_suficient_funds(
            currywurst_price=currywurst_price, eur_inserted=eur_inserted
        )

        # Calculate the quantity of each coin required
        coin_counts = {}
        coins_copy = self.coins.copy()
        for coin in sorted(self.__get_coin_possitilities(),reverse=True):
            coin_counts[coin] = 0
            while change >= coin and self.__check_if_coin_is_available(coin=coin,coins_dict=coins_copy):
                coin_counts[coin] +=1
                coins_copy[coin] -=1
                change -= coin
        change= round(change,2)

        # check if exact change available
        self.__check_if_exact_change_available(change)

        # update attributes
        self.coins = coins_copy
        self.notes = self.__get_eur_notes_inserted(eur_inserted=eur_inserted)
        
        return coin_counts