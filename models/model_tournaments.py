from tinydb import TinyDB


class Tournament:
    id_counter = 0

    def __init__(
        self,
        name,
        location,
        start_date,
        end_date,
        players,
        rounds,
        curent_round,
        total_rounds,
        id=id_counter,
        description="",
        status=False,
    ):
        self.id = id if id else self.generate_id()
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.total_rounds = total_rounds if total_rounds is not None else 4
        self.curent_round = curent_round
        self.players = players
        self.rounds = rounds
        self.description = description
        self.status = status

    @classmethod
    def generate_id(cls):
        db = TinyDB("database/tournaments.json").table("tournaments_table")
        all_tournaments = db.all()

        if all_tournaments:
            max_id = max(int(tournament["id"]) for tournament in all_tournaments)
            return str(max_id + 1)
        else:
            return "1"

    def __str__(self):
        return (
            f"ID {self.id} : {self.name} {self.location}({self.start_date}) - "
            f"{self.end_date} : {self.total_rounds} rounds - {self.curent_round} round - "
            f"Status: {'Terminé' if self.status else 'En cours'}"
        )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_rounds": self.total_rounds,
            "curent_round": self.curent_round,
            "players": self.players,
            "rounds": self.rounds,
            "description": self.description,
            "status": self.status,
        }
