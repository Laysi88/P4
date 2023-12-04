from models import Player
from tinydb import TinyDB, Query


class UpdatePlayers:
    def __init__(self, filename):
        self.db = TinyDB(filename).table("players_table")

    def update(self, updated_player):
        player_id = str(updated_player.id)
        if self.db.contains(Query().id == player_id):
            serialized_player = updated_player.serialize()
            if serialized_player != self.db.get(Query().id == player_id):
                self.db.update(serialized_player, Query().id == player_id)
                print(f"Joueur avec l'identifiant {player_id} mis à jour.")
            else:
                print(f"Aucune modification détectée pour le joueur avec l'identifiant {player_id}.")
        else:
            print(f"Aucun joueur trouvé avec l'identifiant {player_id}")


class LoadPlayers:
    def __init__(self, filename):
        self.db = TinyDB(filename).table("players_table")

    def load(self):
        players = []
        for player_data in self.db.all():
            player = Player(
                id=player_data["id"],
                last_name=player_data["last_name"],
                first_name=player_data["first_name"],
                birth_date=player_data["birth_date"],
                chess_id=player_data["chess_id"],
            )
            player.score = player_data["score"]
            players.append(player)
        return players


class CreatePlayer:
    def __init__(self, filename):
        self.db = TinyDB(filename).table("players_table")

    def create(self, player):
        player.id = str(player.id)
        self.db.insert(player.serialize())
