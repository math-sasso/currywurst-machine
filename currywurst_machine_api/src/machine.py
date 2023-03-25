from typing import Dict
# Some typos: EUR
# CoinWallet

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
            0.01: 100
        }

    def get_coin_possibilities(self):
        return list(self.coins.keys())
    
    def check_if_coin_is_valid(self, coin:str):
        if coin not in self.coins:
            raise ValueError("Invalid coin")
    
    def check_if_coin_is_available(self, coin:str):
        if self.coins[coin] == 0:
            return False
        return True

    def insert_coin(self, coin:str):
        self.check_if_coin_is_valid(coin=coin)
        self.coins[coin] += 1

    def remove_coin(self, coin:str):
            self.check_if_coin_is_valid(coin=coin)
            self.coins[coin] -= 1

class CurrywurstMachine():
    def __init__(self) -> None:

        self.coin_wallet = CoinWallet()

    def __check_suficient_funds(self,change:float):
        # If the user inserted insufficient funds, raise an exception
        if change < 0:
            raise ValueError("Insufficient funds")
    
    def __check_if_exact_change_available(self, change:float):

        # Iterate over the possible Euro coins in descending order
        for coin in sorted(self.coin_wallet.get_coin_possibilities(), reverse=True):
            # Count the number of times the current coin can be used for change
            while change >= coin:
                change -= coin
        
        # Check if exact change was given
        if change != 0:
            raise ValueError("Exact change not possible")


    def return_coins(self, currywurst_price:float, eur_inserted:Dict):
        """
         The currywurst machine accepts any coins or banknotes but returns only
        coins and works only with EUR currency.
        """
        # Calculate the amount of change required
        change = sum(k*v for k,v in eur_inserted.items()) - currywurst_price

        self.__check_suficient_funds(change)
        # self.__check_if_exact_change_available(change)

        
        # Initialize a dictionary to keep track of the number of coins needed for change
        coin_counts = {coin: 0 for coin in self.coin_wallet.get_coin_possibilities()}
       
        # Calculate the quantity of each coin required
        for coin in self.coin_wallet.get_coin_possibilities():
            while change >= coin and self.coin_wallet.check_if_coin_is_available(coin):
                self.coin_wallet.remove_coin(coin=coin)
                coin_counts[coin] +=1
                change -= coin

        return coin_counts 

        # Steps
        # Verify the amount of coins available and check if it is possible to be done othwerise trow and error
        # In the error, suggest the maximum accepted amount
        # Calculate the optimal return 

    
