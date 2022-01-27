from order import Order
from transaction import Transaction

class Player:
    def __init__(self, player_id, budget) -> None:
        self.player_id = player_id
        self.budget = budget
        self.buying_power = budget

        self.pending_orders = []
        self.positions = []

    def complete_order(self, transaction) -> None:
        if self.player_id == transaction.buyer_id: # if player is the buy side
            for order in self.pending_orders:
                if order.type == transaction.type and order.side == transaction.side:
                    order.amount -= transaction.amount
                    if order.amount == 0:
                        self.pending_orders.remove(order)
                    break
        
        elif self.player_id == transaction.seller_id:
            for order in self.pending_orders:
                if order.type == transaction.type and order.side == transaction.side:
                    order.amount -= transaction.amount
                    if order.amount == 0:
                        self.pending_orders.remove(order)
                    break
        