from managers import UpdatePlayers, LoadPlayers, CreatePlayer


class PlayerController:
    def __init__(self, filename="database/players.json"):
        self.filename = filename
        self.players = []
        self.update_players = UpdatePlayers(self.filename)
        self.load_players = LoadPlayers(self.filename)
        self.create_players = CreatePlayer(self.filename)
