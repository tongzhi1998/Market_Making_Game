from datetime import datetime

class Order:
    def __init__(self, player_id: int, type: str, side: str, price: float, quantity: int, timestamp) -> None:
        self.player_id = player_id #int8
        self.side = side 
        self.type = type 
        self.price = price # float32
        self.quantity = quantity #int8
        self.timestamp = timestamp # Python DateTime 
    
    def __lt__(self, other):
        if self.side == 1:
            return self.price > other.price or (self.price == other.price and self.timestamp < other.timestamp )
        else:
            return self.price < other.price or (self.price == other.price and self.timestamp < other.timestamp )

