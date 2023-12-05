from controllers import TournamentController, RoundController, MatchController
from datetime import datetime
from tinydb import TinyDB
from models import Tournament, Round, Match
import random


class PlayView:
    def __init__(self):
        self.tournament_controller = TournamentController()
        self.round_controller = RoundController()
        self.match_controller = MatchController()

    def play_tournament_menu(self):
        while True:
            print("Menu tournois")
            print("1. Liste des tournois en cours")
            print("2. Lancer le tournoi")
            print("3. Retour")
            choice = input("Votre choix: ")
            if choice == "1":
                self.started_tournament()
            elif choice == "2":
                self.launch_tournament()
            elif choice == "3":
                break
            else:
                print("Choix invalide")

    def started_tournament(self):
        print("Liste des tournois en cours")
        tournaments = self.tournament_controller.load_tournaments.load()
        for tournament in tournaments:
            if tournament.status == False:
                print(f"{tournament.id}. {tournament.name}")
            else:
                print("Aucun tournoi en cours")

    def launch_tournament(self):
        print("Lancement d'un tournoi")
        # Récupération de l'id du tournoi
        tournament_id = input("Id du tournoi: ")
        tournament = self.tournament_controller.load_data_tournament.loaddata(tournament_id)
        if tournament.status == False:
            print(f"Tournoi: {tournament.name}")

            # Création du premier round
            if tournament.rounds == []:
                name = "Round 1"
                start_date = datetime.now().strftime("%Y-%m-%d")
                end_date = ""
                status = False
                round = Round(
                    name,
                    start_date,
                    end_date,
                    status,
                )
                round = self.round_controller.create_first_round.create(tournament_id, round)
                print(f"Round: {round.name} - {round.start_date}")
                # Récupération des joueurs du tournoi
                players_copy = list(self.tournament_controller.load_data_tournament.loaddata(tournament_id).players)
                while len(players_copy) > 1:
                    # Création des matchs
                    player1 = random.choice(players_copy)
                    players_copy.remove(player1)
                    player2 = random.choice(players_copy)
                    players_copy.remove(player2)
                    match = Match(player1, player2)
                    self.match_controller.create_match.create(tournament_id, match)
                    # afficher les match avec seulement le nom des joueurs
                    print(
                        f"Match: {player1['last_name']}{player1['first_name']} vs {player2['last_name']}{player2['first_name']}"
                    )

            else:
                print("Le tournoi a déjà commencé")
        else:
            print("Le tournoi est terminé")
