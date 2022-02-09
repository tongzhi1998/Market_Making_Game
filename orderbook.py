from order import Order
from transaction import Transaction
import heapq
import enum
import globals
from player import Player

class OrderBookType(enum.Enum):
    over_under = 1
    future = 2
    option = 3

class OrderBook:
    def __init__(self, type: OrderBookType, strike_price: int = 0) -> None:
        self.type = type
        self.strike_price = strike_price

        self.heap_bid = []
        self.heap_ask = []
        self.map_bid = {}
        self.map_ask = {}
        self.current_price = 0.0
        self.transactions = []
        
    def match_order(self, order: Order) -> tuple[int, list[tuple[float, int]], list[tuple[float, int]], list[Transaction]]:
        transactions = []
        if order.side == 'buy': # Buying Order
            while order.quantity > 0 and len(self.heap_ask) > 0:
                to_match = heapq.heappop(self.heap_ask)
                if to_match.price > order.price:
                    heapq.heappush(self.heap_ask,to_match)
                    break
                else:
                    matched_amount = min(order.quantity, to_match.quantity)
                    transaction = Transaction(order,to_match,1)
                    self.transactions.append(transaction)
                    transactions.append(transaction)
                    order.quantity -= matched_amount
                    to_match.quantity -= matched_amount
                    self.current_price = to_match.price
                    
                    globals.game.players[order.player_id].complete_order(transaction,"buy")
                    globals.game.players[to_match.player_id].complete_order(transaction,"sell")
                    
                    if to_match.quantity != 0:
                        heapq.heappush(self.heap_ask,to_match)
                        self.map_ask[to_match.price] -= matched_amount
                    else:
                        self.map_ask.pop(to_match.price)
        else: # Selling Order
            while order.quantity > 0 and len(self.heap_bid) > 0:
                to_match = heapq.heappop(self.heap_bid)
                if to_match.price < order.price:
                    heapq.heappush(self.heap_bid,to_match)
                    break
                else:
                    matched_amount = min(order.quantity, to_match.quantity)
                    transaction = Transaction(to_match, order, 2)
                    self.transactions.append(transaction)

                    order.quantity -= matched_amount
                    to_match.quantity -= matched_amount
                    self.current_price = to_match.price

                    globals.game.players[order.player_id].complete_order(transaction,"sell")
                    globals.game.players[to_match.player_id].complete_order(transaction,"buy")
                    if to_match.quantity != 0:
                        heapq.heappush(self.heap_bid,to_match)
                        self.map_bid[to_match.price] -= matched_amount
                    else:
                        self.map_bid.pop(to_match.price)
        
        self.__add_order_to_book(order)

        return self.current_price, self.__get_order_list("buy"), self.__get_order_list("sell"), transactions

    def __get_order_list(self, side: str) -> list[tuple[int, float]]:
        ans = []
        if side == "buy": # Bid Side
            for key, value in self.map_bid.items():
                ans.append((key, value))
            ans.sort(reverse = True)
        else: # Sell Side
            for key, value in self.map_ask.items():
                ans.append((key,value))
            ans.sort()
        return ans
    
    def __add_order_to_book(self, order: Order) -> None:
        if order.quantity == 0:
            return
        if order.side == "buy": # Buying Order
            heapq.heappush(self.heap_bid,order)
            if order.price in self.map_bid:
                self.map_bid[order.price] += order.quantity
            else:
                self.map_bid[order.price] = order.quantity
        else: # Buying Order
            heapq.heappush(self.heap_ask,order)
            if order.price in self.map_ask: 
                self.map_ask[order.price] += order.quantity
            else:
                self.map_ask[order.price] = order.quantity



class OverUnderBook(OrderBook):
    def __init__(self) -> None:
        super().__init__()

class FutureBook(OrderBook):
    def __init__(self) -> None:
        super().__init__()

class OptionBook(OrderBook):
    def __init__(self, strike_price) -> None:
        super().__init__()
        self.strike_price = strike_price