from tinydb import TinyDB


class Match:
    def __init__(self, player1, player2, status=False, winner=None):
        self.player1 = player1
        self.player2 = player2
        self.status = status
        self.winner = winner

    def __str__(self):
        return f"{self.player1} - {self.player2} : {self.status}"

    def serialize(self):
        return {
            "player1": self.player1,
            "player2": self.player2,
            "status": self.status,
        }
