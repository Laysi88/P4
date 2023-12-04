from tinydb import TinyDB


class Player:
    id_counter = 0

    def __init__(
        self,
        last_name,
        first_name,
        birth_date,
        chess_id,
        id=id_counter,
    ):
        self.id = id if id else self.generate_id()
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.chess_id = chess_id
        self.score = 0.0
        self.opponents = []

    @classmethod
    def generate_id(cls):
        db = TinyDB("database/players.json").table("players_table")
        all_players = db.all()

        if all_players:
            max_id = max(int(player["id"]) for player in all_players)
            return str(max_id + 1)
        else:
            return "1"

    def __str__(self):
        return f"ID {self.id} : {self.last_name} {self.first_name}({self.birth_date}) - Chess_ID : {self.chess_id}"

    def serialize(self):
        return {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "chess_id": self.chess_id,
            "score": self.score,
            "opponents": self.opponents,
        }
