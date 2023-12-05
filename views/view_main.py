from .view_players import PlayerView
from .view_tournaments import TournamentView
from .view_play import PlayView


class MainView:
    def __init__(self):
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()
        self.play_view = PlayView()

    def main_menu(self):
        while True:
            print("Menu principal")
            print("1. Gestion des joueurs")
            print("2. Gestions des tournois")
            print("3. Jouer un tournoi")
            print("4. Quitter")
            choice = input("Votre choix: ")
            if choice == "1":
                self.player_view.player_menu()
            elif choice == "2":
                self.tournament_view.tournament_menu()
            elif choice == "3":
                self.play_view.play_tournament_menu()
            elif choice == "4":
                break
            else:
                print("Choix invalide")
            print()

    def run(self):
        self.main_menu()
