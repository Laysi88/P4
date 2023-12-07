from controllers import TournamentController, RoundController, MatchController
from datetime import datetime
from models import Round, Match
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
            print("3. Résultats des matchs")
            print("4. Retour")
            choice = input("Votre choix: ")
            if choice == "1":
                self.started_tournament()
            elif choice == "2":
                self.launch_tournament()
            elif choice == "3":
                self.enter_results()
            elif choice == "4":
                break
            else:
                print("Choix invalide")

    def started_tournament(self):
        print("Liste des tournois en cours")
        tournaments = self.tournament_controller.load_tournaments.load()

        for tournament in tournaments:
            if not tournament.status:
                print(f"{tournament.id}. {tournament.name}")

                for round_data in tournament.rounds:
                    round_instance = Round(**round_data)  # Créez une instance de la classe Round
                    if not round_instance.status:
                        print(f"   - {round_instance.name} - {round_instance.start_date}")

                        at_least_one_match_in_progress = False
                        for match_data in round_instance.matches:
                            match_instance = Match(**match_data)  # Créez une instance de la classe Match
                            if not match_instance.status:
                                print(
                                    f"{match_instance.player1['last_name']} {match_instance.player1['first_name']} "
                                    f"vs {match_instance.player2['last_name']} {match_instance.player2['first_name']}"
                                )
                                # Définir le drapeau sur True si au moins un match n'est pas terminé
                                at_least_one_match_in_progress = True

                        if not at_least_one_match_in_progress:
                            print("Tous les matchs sont terminés")
                    else:
                        print("Tous les rounds sont terminés")
            else:
                print("Aucun tournoi en cours")

    def launch_tournament(self):
        print("Lancement d'un tournoi")
        # Récupération de l'id du tournoi
        tournament_id = input("Id du tournoi: ")
        tournament = self.tournament_controller.load_data_tournament.loaddata(tournament_id)
        if not tournament.status:
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
                        f"Match: {player1['last_name']} {player1['first_name']} vs "
                        f"{player2['last_name']} {player2['first_name']}"
                    )

            else:
                print("Le tournoi a déjà commencé")
        else:
            print("Le tournoi est terminé")

    def enter_results(self):
        print("Résultats des matchs")
        # Récupération de l'id du tournoi
        tournament_id = input("Id du tournoi: ")
        tournament = self.tournament_controller.load_data_tournament.loaddata(tournament_id)

        if not tournament.status and tournament.rounds != []:
            for round_data in tournament.rounds:
                round_instance = Round(**round_data)  # Créez une instance de la classe Round
                if not round_instance.status and round_instance.matches != []:  # Si le round n'est pas terminé
                    print(f"   - {round_instance.name} - {round_instance.start_date}")
                    for match_data in round_instance.matches and not match_instance.status:
                        match_instance = Match(**match_data)
                        print(
                            f"{match_instance.player1['last_name']} {match_instance.player1['first_name']} "
                            f"vs {match_instance.player2['last_name']} {match_instance.player2['first_name']}"
                        )

                        if not match_instance.status:
                            print(
                                f"{match_instance.player1['last_name']} {match_instance.player1['first_name']} vs "
                                f"{match_instance.player2['last_name']} {match_instance.player2['first_name']}"
                            )
                            print(
                                "1. "
                                + match_instance.player1["last_name"]
                                + " "
                                + match_instance.player1["first_name"]
                            )
                            print(
                                "2. "
                                + match_instance.player2["last_name"]
                                + " "
                                + match_instance.player2["first_name"]
                            )
                            print("3.Match nul")
                            print("4. Retour")

                            result = input("Résultat du match: ")

                            if result == "1":
                                result = f"{match_instance.player1['last_name']}{match_instance.player1['first_name']}"
                            elif result == "2":
                                result = f"{match_instance.player2['last_name']}{match_instance.player2['first_name']}"
                            elif result == "3":
                                result = "Match nul"
                            elif result == "4":
                                break
                            # Mise à jour du résultat du match
                            self.match_controller.update_match.result(tournament_id, match_instance.id, result)
                            print("Résultat enregistré")
                    else:
                        print("Tous les matchs sont terminés")
                        match_instance.status = True
                        self.round_controller.update_round.update(tournament_id, round_instance.id, round_instance)
        else:
            print("Aucun match en cours")
