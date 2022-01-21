from order import Order
from datetime import datetime

class Transaction:
    def __init__(self, buy_side: Order, sell_side: Order, aggressor: int) -> None:
        self.amount = min(buy_side.quantity, sell_side.quantity)
        if aggressor == 1: # Buy side is the aggressor, price should be sell_side price
            self.price = sell_side.price
        else:
            self.price = buy_side.price
        
        self.buyer_id = buy_side.player_id
        self.seller_id = sell_side.player_id
        self.time = datetime.utcnow()

    def __str__(self) -> str:
        return f"Transaction price: {self.price}, amount = {self.amount}, time = {self.time}" + "\n" + f"Buyer is: {self.buyer_id}, seller is: {self.seller_id}"
