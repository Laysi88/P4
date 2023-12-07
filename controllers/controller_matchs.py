from managers import CreateMatch, UpdateMatch, LoadMatch


class MatchController:
    def __init__(self, filename="database/tournaments.json"):
        self.filename = filename
        self.create_match = CreateMatch(self.filename)
        self.update_match = UpdateMatch(self.filename)
        self.load_match = LoadMatch(self.filename)
