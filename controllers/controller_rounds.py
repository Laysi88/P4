from managers import CreateRound


class RoundController:
    def __init__(self, filename="database/tournaments.json"):
        self.filename = filename
        self.create_first_round = CreateRound(self.filename)
