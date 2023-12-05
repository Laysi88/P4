from tinydb import TinyDB, Query


class CreateRound:
    def __init__(self, filename):
        self.db = TinyDB(filename).table("tournaments_table")

    def create(self, tournament_id, round):
        tournament = self.db.get(Query().id == tournament_id)
        if tournament:
            tournament["rounds"].append(round.serialize())
            self.db.update({"rounds": tournament["rounds"]}, Query().id == tournament_id)
            return round
