from managers import CreateRound, UpdateRound


class RoundController:
    def __init__(self, filename="database/tournaments.json"):
        self.filename = filename
        self.create_first_round = CreateRound(self.filename)
        self.update_round = UpdateRound(self.filename)
