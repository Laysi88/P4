from models import Player
from controllers import PlayerController
from datetime import datetime


class PlayerView:
    def __init__(self):
        self.player_controller = PlayerController()

    def is_valid_date(self, date):
        try:
            datetime.strptime(date, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def is_valid_chess_id(self, chess_id):
        return len(chess_id) == 6 and chess_id[:2].isalpha() and chess_id[2:].isdigit()

    def is_valid_name(self, name):
        return name.isalpha()

    def player_menu(self):
        while True:
            print("Menu joueurs")
            print("1. Créer un joueur")
            print("2. Modifier un joueur")
            print("3. Afficher les joueurs")
            print("4. Retour")
            choice = input("Votre choix: ")
            if choice == "1":
                self.create_player()
            elif choice == "2":
                self.update_player()
            elif choice == "3":
                self.show_players()
            elif choice == "4":
                break
            else:
                print("Choix invalide")
            print()

    def create_player(self):
        print("Création d'un joueur")
        while True:
            last_name = input("Nom: ")
            if self.is_valid_name(last_name):
                break
            else:
                print("Nom invalide")
        while True:
            first_name = input("Prénom: ")
            if self.is_valid_name(first_name):
                break
            else:
                print("Prénom invalide")
        while True:
            birth_date = input("Date de naissance (format JJ/MM/AAAA): ")
            if self.is_valid_date(birth_date):
                break
            else:
                print("Date invalide")
        while True:
            chess_id = input("Identifiant FFE: ")
            if self.is_valid_chess_id(chess_id):
                break
            else:
                print("Identifiant invalide")
        player = Player(
            last_name=last_name,
            first_name=first_name,
            birth_date=birth_date,
            chess_id=chess_id,
        )
        self.player_controller.create_players.create(player)
        print("Joueur créé")

    def update_player(self):
        print("Modification d'un joueur")

        id_to_update = input("Identifiant: ")

        while True:
            last_name = input("Nom: ")
            if self.is_valid_name(last_name):
                break
            else:
                print("Nom invalide")
        while True:
            first_name = input("Prénom: ")
            if self.is_valid_name(first_name):
                break
            else:
                print("Prénom invalide")
        while True:
            birth_date = input("Date de naissance (format JJ/MM/AAAA): ")
            if self.is_valid_date(birth_date):
                break
            else:
                print("Date invalide")
        while True:
            chess_id = input("Identifiant FFE: ")
            if self.is_valid_chess_id(chess_id):
                break
            else:
                print("Identifiant invalide")

        updated_player = Player(
            last_name=last_name,
            first_name=first_name,
            birth_date=birth_date,
            chess_id=chess_id,
            id=id_to_update,
        )
        self.player_controller.update_players.update(updated_player)
        print("Joueur modifié")

    def show_players(self):
        print("Liste des joueurs")
        players = self.player_controller.load_players.load()
        for player in players:
            print(player)
