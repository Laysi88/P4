from managers import CreateMatch


class MatchController:
    def __init__(self, filename="database/tournaments.json"):
        self.filename = filename
        self.create_match = CreateMatch(self.filename)
