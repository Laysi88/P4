from managers import CreateRound, UpdateRound, LoadLastRound, UpdateNewRound


class RoundController:
    def __init__(self, filename="database/tournaments.json"):
        self.filename = filename
        self.create_first_round = CreateRound(self.filename)
        self.update_round = UpdateRound(self.filename)
        self.update_new_round = UpdateNewRound(self.filename)
        self.load_last_round = LoadLastRound(self.filename)
