from tinydb import TinyDB, Query


class CreateMatch:
    def __init__(self, filename):
        self.db = TinyDB(filename).table("tournaments_table")

    def create(self, tournament_id, match):
        # enregistrement du match dans le round du tournoi
        tournament = self.db.get(Query().id == tournament_id)
        if tournament:
            for round in tournament["rounds"]:
                if not round["status"]:
                    round["matches"].append(match.serialize())
                    self.db.update({"rounds": tournament["rounds"]}, Query().id == tournament_id)
                    return match


class UpdateMatch:
    def __init__(self, filename):
        self.db = TinyDB(filename).table("tournaments_table")

    def result(self, tournament_id, match_id, winner):
        tournament = self.db.get(Query().id == tournament_id)
        if tournament:
            for round in tournament["rounds"]:
                if not round["status"]:
                    for match in round["matches"]:
                        if match["id"] == match_id:
                            match["status"] = True
                            match["winner"] = winner
                            self.db.update({"rounds": tournament["rounds"]}, Query().id == tournament_id)
                            return match
