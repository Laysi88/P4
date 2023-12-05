from tinydb import TinyDB


class Match:
    def __init__(self, player1, player2, status=False, winner=None, id=None):
        self.player1 = player1
        self.player2 = player2
        self.status = status
        self.winner = winner
        self.id = id if id else self.generate_id()

    @classmethod
    def generate_id(cls):
        db = TinyDB("database/tournaments.json").table("tournaments_table")
        all_matches = db.all()

        match_ids = []
        for tournament in all_matches:
            for round in tournament.get("rounds", []):
                match_ids.extend([int(match["id"]) for match in round.get("matches", [])])

        if match_ids:
            max_id = max(match_ids)
            return str(max_id + 1)
        return "1"

    def __str__(self):
        return f"{self.player1} - {self.player2} : {self.status}"

    def serialize(self):
        return {
            "id": self.id,
            "player1": self.player1,
            "player2": self.player2,
            "status": self.status,
        }
