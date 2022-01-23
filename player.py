
class Player:
    def __init__(self, player_id, budget) -> None:
        self.player_id = player_id
        self.budget = budget
        self.buying_power = budget

        self.active_orders = []
        self.completed_orders = []
        