from tinydb import TinyDB, Query


class Round:
    id_counter = 0

    def __init__(self, name, start_date, end_date, matches=None, status=False, id=id_counter):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.matches = matches or []  # Utilisez la valeur par défaut si matches n'est pas fourni
        self.status = status
        self.id = id if id else self.generate_id()

    @classmethod
    def generate_id(cls):
        db = TinyDB("database/tournaments.json").table("tournaments_table")
        all_rounds = db.all()

        if all_rounds:
            matches = [int(round["id"]) for tournament in all_rounds for round in tournament.get("rounds", [])]
            if matches:
                max_id = max(matches)
                return str(max_id + 1)
        return "1"

    def __str__(self):
        return (
            f"{self.name}({self.start_date}) - {self.end_date}" f"Status: {'Terminé' if self.status else 'En cours'}"
        )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "matches": self.matches,
            "status": self.status,
        }
