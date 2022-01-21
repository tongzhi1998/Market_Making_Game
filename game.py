from datetime import datetime
from player import Player
from orderbook import OrderBook, OrderBookType

# TODO: Need to make these configurable (Maybe reading from a init file?)
budget = 10000
answer = 2000
strike_price = 1000
game_duration = 1000

class Game:
    def __init__(self, player_ids: list[int]) -> None:
        self.players = []
        for player_id in player_ids:
            player = Player(player_id, budget)
            self.players.append(player)
        self.number_of_players = len(player_ids)

        self.budget = budget
        self.answer = answer
        self.start_time = datetime.utcnow()
        self.duration = game_duration

        self.over_under_book = OrderBook(OrderBookType.over_under)
        self.future_book = OrderBook(OrderBookType.future)
        self.option_book = OrderBook(OrderBookType.option, strike_price)





