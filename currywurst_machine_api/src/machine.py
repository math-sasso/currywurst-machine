from typing import Dict
from .custom_exceptions import (
    InsuficientFundsException,
    NotExactChangeAvailableException,
)


class CoinWallet:
    def __init__(self):
        self.coins = {
            2: 100,
            1: 100,
            0.5: 100,
            0.2: 100,
            0.1: 100,
            0.05: 100,
            0.02: 100,
            0.01: 100,
        }

    def get_empty_coin_dict(self):
        return {coin: 0 for coin in self.coins.keys()}

    def get_coin_possitilities(self):
        return list(self.coins.keys())

    def insert_coin(self, coin: float):
        self.coins[coin] += 1

    def remove_coin(self, coin: float):
        self.coins[coin] -= 1

    def check_if_coin_is_available(self, coin: float):
        if self.coins[coin] == 0:
            return False
        return True


class CurrywurstMachine:
    def __init__(self) -> None:
        self.coin_wallet = CoinWallet()
        
    def __check_suficient_funds(self, currywurst_price: float, eur_inserted: Dict):
        # Calculate the amount of change required
        amount_inserted = sum(k * v for k, v in eur_inserted.items())
        change = amount_inserted - currywurst_price

        # If the user inserted insufficient funds, raise an exception
        if change < 0:
            raise InsuficientFundsException("Insufficient funds")

        return change

    def __check_if_exact_change_available(self, change: float):
        # Iterate over the possible Euro coins in descending order
        for coin in sorted(self.coin_wallet.get_coin_possibilities(), reverse=True):
            # Count the number of times the current coin can be used for change
            while change >= coin:
                change -= coin

        # Check if exact change was given
        if change != 0:
            raise NotExactChangeAvailableException("Exact change not possible")

    def return_coins(self, currywurst_price: float, eur_inserted: Dict[float, int]):
        """
         The currywurst machine accepts any coins or banknotes but returns only
        coins and works only with EUR currency.
        """
        import pdb;pdb.set_trace()
  
        # Initialize a dictionary to keep track of the number of coins needed for change
        coin_counts = self.coin_wallet.get_empty_coin_dict()

        # Calculates change and raise exception if funds are not suficient
        change = self.__check_suficient_funds(
            currywurst_price=currywurst_price, eur_inserted=eur_inserted
        )

        import pdb;pdb.set_trace()

        # Calculate the quantity of each coin required
        self.coin_wallet.coins.copy()
        for coin in sorted(self.coin_wallet.get_coin_possitilities(),reverse=True):
            while change >= coin and self.coin_wallet.check_if_coin_is_available(coin):
                self.coin_wallet.remove_coin(coin=coin)
                coin_counts[coin] += 1
                change -= coin
        
        import pdb;pdb.set_trace()

        # self.__check_if_exact_change_available(change)

        return coin_counts