from models import Tournament
from tinydb import TinyDB, Query
from datetime import datetime


class CreateTournament:
    def __init__(self, filename):
        self.db = TinyDB(filename).table("tournaments_table")

    def create(self, tournament):
        tournament.id = str(tournament.id)
        self.db.insert(tournament.serialize())


class LoadTournament:
    def __init__(self, filename):
        self.db = TinyDB(filename).table("tournaments_table")

    def load(self):
        tournaments = []
        for tournament_data in self.db.all():
            tournament = Tournament(
                id=tournament_data["id"],
                name=tournament_data["name"],
                location=tournament_data["location"],
                start_date=tournament_data["start_date"],
                end_date=tournament_data["end_date"],
                rounds=tournament_data["rounds"],
                description=tournament_data["description"],
                players=tournament_data["players"],
                status=tournament_data["status"],
                curent_round=tournament_data["curent_round"],
                total_rounds=tournament_data["total_rounds"],
            )
            tournaments.append(tournament)
        return tournaments


class LoadDataTournament:
    def __init__(self, filename):
        self.db = TinyDB(filename).table("tournaments_table")

    def loaddata(self, id):
        # Assurez-vous que id est une chaîne de caractères
        id_str = str(id)
        tournament_data = self.db.get(Query().id == id_str)
        if tournament_data is None:
            return None
        tournament = Tournament(
            id=tournament_data["id"],
            name=tournament_data["name"],
            location=tournament_data["location"],
            start_date=tournament_data["start_date"],
            end_date=tournament_data["end_date"],
            rounds=tournament_data["rounds"],
            description=tournament_data["description"],
            players=tournament_data["players"],
            status=tournament_data["status"],
            curent_round=tournament_data["curent_round"],
            total_rounds=tournament_data["total_rounds"],
        )

        return tournament


class UpdateTournament:
    def __init__(self, filename):
        self.db = TinyDB(filename).table("tournaments_table")

    def update(self, updated_tournament):
        tournament_id = str(updated_tournament.id)
        if self.db.contains(Query().id == tournament_id):
            serialized_tournament = updated_tournament.serialize()
            if serialized_tournament != self.db.get(Query().id == tournament_id):
                self.db.update(serialized_tournament, Query().id == tournament_id)
                print(f"Tournoi avec l'identifiant {tournament_id} mis à jour.")
            else:
                print(f"Aucune modification détectée pour le tournoi avec l'identifiant {tournament_id}.")
        else:
            print(f"Aucun tournoi trouvé avec l'identifiant {tournament_id}")


class EndTournament:
    def __init__(self, filename):
        self.db = TinyDB(filename).table("tournaments_table")

    def end(self, tournament):
        # récupère l'id du tournoi
        tournament_id = str(tournament.id)
        # vérifie que le tournoi existe
        if self.db.contains(Query().id == tournament_id):
            # récupère les données du tournoi
            tournament_data = self.db.get(Query().id == tournament_id)
            # vérifie que le tournoi est en cours
            if not tournament_data["status"]:
                # verifications des rounds
                if all(round["status"] for round in tournament_data["rounds"]):
                    # vériifcation du nombre de rounds
                    if tournament_data["curent_round"] == tournament_data["total_rounds"]:
                        # mise à jour du statut du tournoi staut et end_date
                        self.db.update(
                            {"status": True, "end_date": datetime.now().strftime("%Y-%m-%d")},
                            Query().id == tournament_id,
                        )
                        print(f"Le tournoi {tournament.name} est terminé.")
