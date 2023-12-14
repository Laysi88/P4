from managers import CreateTournament, LoadTournament, LoadDataTournament, UpdateTournament, EndTournament
from tinydb import TinyDB


class TournamentController:
    def __init__(self, filename="database/tournaments.json"):
        self.filename = filename
        self.db = TinyDB(self.filename)
        self.tournaments = []
        self.create_tournaments = CreateTournament(self.filename)
        self.load_tournaments = LoadTournament(self.filename)
        self.load_data_tournament = LoadDataTournament(self.filename)
        self.update_tournament = UpdateTournament(self.filename)
        self.end_tournament = EndTournament(self.filename)
