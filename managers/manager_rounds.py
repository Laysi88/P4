from tinydb import TinyDB, Query
from datetime import datetime


class CreateRound:
    def __init__(self, filename):
        self.db = TinyDB(filename).table("tournaments_table")

    def create(self, tournament_id, round):
        tournament = self.db.get(Query().id == tournament_id)
        if tournament:
            tournament["rounds"].append(round.serialize())
            self.db.update({"rounds": tournament["rounds"]}, Query().id == tournament_id)
            return round


class UpdateRound:
    def __init__(self, filename):
        self.db = TinyDB(filename).table("tournaments_table")

    def update(self, tournament_id, round_id, round):
        tournament = self.db.get(Query().id == tournament_id)
        if tournament:
            for round_data in tournament["rounds"]:
                if round_data["id"] == round_id:
                    round_data["status"] = True
                    end_date = datetime.now().strftime("%Y-%m-%d")
                    round_data["end_date"] = end_date
                    self.db.update({"rounds": tournament["rounds"]}, Query().id == tournament_id)
                    return round_data


class UpdateNewRound:
    def __init__(self, filename):
        self.db = TinyDB(filename).table("tournaments_table")

    def update(self, tournament_id, round_id, round):
        tournament = self.db.get(Query().id == tournament_id)
        if tournament:
            for round_data in tournament["rounds"]:
                if round_data["id"] == round_id:
                    round_data["status"] = False
                    self.db.update({"rounds": tournament["rounds"]}, Query().id == tournament_id)
                    return round_data


class LoadLastRound:
    def __init__(self, filename):
        self.db = TinyDB(filename).table("tournaments_table")

    def load(self, tournament_id):
        tournament = self.db.get(Query().id == tournament_id)
        if tournament:
            for round_data in tournament["rounds"]:
                if round_data["status"] == False:
                    return round_data
            return None
