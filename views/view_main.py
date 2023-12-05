from .view_players import PlayerView
from .view_tournaments import TournamentView


class MainView:
    def __init__(self):
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()

    def main_menu(self):
        while True:
            print("Menu principal")
            print("1. Gestion des joueurs")
            print("2. Créer un tournoi")
            print("3. Charger un tournoi")
            print("4. Quitter")
            choice = input("Votre choix: ")
            if choice == "1":
                self.player_view.player_menu()
            elif choice == "2":
                self.tournament_view.tournament_menu()
            elif choice == "3":
                pass
            elif choice == "4":
                break
            else:
                print("Choix invalide")
            print()

    def run(self):
        self.main_menu()
