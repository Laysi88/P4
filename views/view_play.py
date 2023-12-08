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

        at_least_one_tournament_in_progress = False  # Nouveau drapeau pour suivre si au moins un tournoi est en cours

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

                # Définir le drapeau sur True si au moins un tournoi est en cours
                at_least_one_tournament_in_progress = True

        # Afficher le message seulement s'il n'y a aucun tournoi en cours
        if not at_least_one_tournament_in_progress:
            print("Aucun tournoi en cours")

    def launch_tournament(self):
        print("Lancement d'un tournoi")
        # Récupération de l'id du tournoi
        tournament_id = input("Id du tournoi: ")
        tournament = self.tournament_controller.load_data_tournament.loaddata(tournament_id)

        # Vérifier si le tournoi existe avant d'accéder à ses propriétés
        if tournament is not None:
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
                    players_copy = list(
                        self.tournament_controller.load_data_tournament.loaddata(tournament_id).players
                    )
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
        else:
            print("Tournoi introuvable. Veuillez entrer un ID de tournoi valide.")

    def enter_results(self):
        print("Résultats des matchs")

        # Récupération de l'id du tournoi
        while True:
            tournament_id = input("Id du tournoi: ")
            tournament = self.tournament_controller.load_data_tournament.loaddata(tournament_id)
            if tournament is not None:
                break
            else:
                print("Tournoi introuvable. Veuillez entrer un ID de tournoi valide.")
                break

        # Vérifier si le tournoi n'est pas terminé et a des rounds
        if tournament is not None and not tournament.status and tournament.rounds != []:
            for round_data in tournament.rounds:  # Pour chaque round du tournoi
                round_instance = Round(**round_data)  # Créez une instance de la classe Round
                if not round_instance.status and round_instance.matches != []:  # Si le round n'est pas terminé
                    for match_data in round_instance.matches:  # Pour chaque match du round
                        match_instance = Match(**match_data)
                        if not match_instance.status:
                            print(
                                f"{match_instance.id}.  "
                                f"{match_instance.player1['last_name']} {match_instance.player1['first_name']} "
                                f"vs {match_instance.player2['last_name']} {match_instance.player2['first_name']}"
                            )
                        else:
                            # Clôturer le round
                            self.round_controller.update_round.update(tournament_id, round_instance.id, round_instance)
                            # Lancer le round suivant

            # Récupération de l'id du match
            while True:
                print("Id du match: ")
                match_id = input()
                match = self.match_controller.load_match.load(tournament_id, match_id)
                if match:
                    break
                else:
                    print("Id du match invalide")
                    break
