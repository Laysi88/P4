from views import PlayerView


class MainView:
    def __init__(self):
        self.player_view = PlayerView()

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
                pass
            elif choice == "3":
                pass
            elif choice == "4":
                break
            else:
                print("Choix invalide")
            print()

    def run(self):
        self.main_menu()
