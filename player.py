from order import Order
from transaction import Transaction

class Player:
    def __init__(self, player_id, budget) -> None:
        self.player_id = player_id
        self.budget = budget
        self.buying_power = budget

        self.pending_orders = []
        self.positions = {} # key = tuple(type, side, price), value = quantity

    # This is only called for the passive side of the transaction
    def complete_order(self, transaction, side) -> None:
        flip_side = "sell"
        if side == "sell":
           flip_side = "buy"
        if side == "sell": # if a selling order is fulfilled, then buying_power is guranteed to increase! (TODO: think about it!)
            self.buying_power += transaction.amount * transaction.price

        for order in self.pending_orders:
            if order.type == transaction.type and order.side == side and order.price == transaction.price: #if matched
                order.amount -= transaction.amount
                if (order.type, side, order.price) in self.positions:
                    self.positions[(order.type, order.side, order.price)] += transaction.amount
                elif (order.type, flip_side, order.price) in self.positions:
                    if self.positions[(order.type, flip_side, order.price)] > transaction.amount:
                        self.positions[(order.type, flip_side, order.price)] -= transaction.amount
                    else:
                        to_add = transaction.amount - self.positions[(order.type, flip_side, order.price)]
                        self.positions.pop((order.type, flip_side, order.price))
                        self.positions[(order.type, side, order.price)] = to_add
                else:
                    self.positions[(order.type, side, order.price)] = transaction.amount
                if order.amount == 0:
                    self.pending_orders.remove(order)
                break
                   
    