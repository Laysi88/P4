from models import Match
from tinydb import TinyDB, Query


class CreateMatch:
    def __init__(self, filename):
        self.db = TinyDB(filename).table("tournaments_table")

    def create(self, tournament_id, match):
        # enregistrement du match dans le round du tournoi
        tournament = self.db.get(Query().id == tournament_id)
        if tournament:
            for round in tournament["rounds"]:
                if round["status"] == False:
                    round["matches"].append(match.serialize())
                    self.db.update({"rounds": tournament["rounds"]}, Query().id == tournament_id)
                    return match
