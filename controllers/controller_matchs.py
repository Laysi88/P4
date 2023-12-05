from managers import CreateMatch, UpdateMatch


class MatchController:
    def __init__(self, filename="database/tournaments.json"):
        self.filename = filename
        self.create_match = CreateMatch(self.filename)
        self.update_match = UpdateMatch(self.filename)
