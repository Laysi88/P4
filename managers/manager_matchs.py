from tinydb import TinyDB, Query


class CreateMatch:
    def __init__(self, filename):
        self.db = TinyDB(filename).table("tournaments_table")

    def create(self, tournament_id, match, round_id):
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
            for round_data in tournament["rounds"]:
                if not round_data["status"]:
                    for match_data in round_data["matches"]:
                        if match_data["id"] == match_id:
                            match_data["status"] = True
                            match_data["winner"] = winner

                            # Trouver les indices des joueurs
                            player1_id = match_data["player1"]["id"]
                            player2_id = match_data["player2"]["id"]

                            # Mettre à jour les scores des joueurs
                            player1_index = next(
                                i for i, player in enumerate(tournament["players"]) if player["id"] == player1_id
                            )
                            player2_index = next(
                                i for i, player in enumerate(tournament["players"]) if player["id"] == player2_id
                            )

                            if (
                                winner
                                == f"{match_data['player1']['last_name']} {match_data['player1']['first_name']} "
                            ):
                                tournament["players"][player1_index]["score"] += 1
                            elif (
                                winner
                                == f"{match_data['player2']['last_name']} {match_data['player2']['first_name']} "
                            ):
                                tournament["players"][player2_index]["score"] += 1
                            else:
                                tournament["players"][player1_index]["score"] += 0.5
                                tournament["players"][player2_index]["score"] += 0.5

                            self.db.update(
                                {"rounds": tournament["rounds"], "players": tournament["players"]},
                                Query().id == tournament_id,
                            )
                            return match_data


class LoadMatch:
    def __init__(self, filename):
        self.db = TinyDB(filename).table("tournaments_table")

    def load(self, tournament_id, match_id):
        tournament = self.db.get(Query().id == tournament_id)
        if tournament:
            for round in tournament["rounds"]:
                if not round["status"]:
                    for match in round["matches"]:
                        if match["id"] == match_id:
                            return match
