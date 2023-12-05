from models import Tournament
from tinydb import TinyDB, Query


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
        tournament_data = self.db.get(Query().id == id)
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
