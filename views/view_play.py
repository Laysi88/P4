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
            print("3. Continuer le tournoi")
            print("4. Retour")
            choice = input("Votre choix: ")
            if choice == "1":
                self.started_tournament()
            elif choice == "2":
                self.launch_tournament()
            elif choice == "3":
                self.enter_result()
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

        # Vérifier si le nombre de joueurs est suffisant pour lancer le tournoi
        required_players = 2**tournament.total_rounds
        if len(tournament.players) < required_players:
            print("Il n'y a pas assez de joueurs pour lancer le tournoi")
            print(f"Nombre de joueurs requis: {required_players}")
            return

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
                    new_round = Round(name, start_date, end_date, status)
                    new_round = self.round_controller.create_first_round.create(tournament_id, new_round)
                    print(f"Round: {new_round.name} - {new_round.start_date}")
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
                        round_id = new_round.id
                        self.match_controller.create_match.create(tournament_id, match.serialize(), round_id)
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

    def enter_result(self):
        # Récupération de l'id du tournoi
        tournament_id = input("Id du tournoi: ")
        tournament = self.tournament_controller.load_data_tournament.loaddata(tournament_id)

        # Vérifier si le tournoi existe avant d'accéder à ses propriétés
        if tournament is not None:  # Vérifier si le tournoi existe avant d'accéder à ses propriétés
            if not tournament.status:  # Vérifier si le tournoi est terminé
                print(f"Tournoi: {tournament.name}")  # Afficher le nom du tournoi

                # Récupération des rounds du tournoi
                rounds = tournament.rounds
                if rounds == []:
                    print("Le tournoi n'a pas encore commencé")
                    return
                for round_data in rounds:
                    round_instance = Round(**round_data)

                    # Vérifier si le round est terminé
                    if not round_instance.status:
                        print(f"Round: {round_instance.name}")

                        # Récupération des matchs du round
                        matches = round_instance.matches
                        for match_data in matches:
                            match_instance = Match(**match_data)

                            # Vérifier si le match est terminé
                            # imprimler iddu match  player 1 et player 2
                            if not match_instance.status:
                                print(
                                    f"Match: {match_instance.id} "
                                    f"{match_instance.player1['last_name']} {match_instance.player1['first_name']} "
                                    "vs"
                                    f" {match_instance.player2['last_name']} {match_instance.player2['first_name']}"
                                )
                    # Récupérer l'id du match
                    compteur = len(round_instance.matches)
                    for match_data in round_instance.matches:
                        if match_data["status"]:
                            compteur = compteur - 1

                    while compteur > 0:
                        match_id = input("Id du match: ou 0 pour quitter ")
                        if match_id == "0":
                            compteur = 0
                            break

                        match = self.match_controller.load_match.load(tournament_id, match_id)
                        if match is not None:
                            print(
                                f"Match: {match['id']}"
                                f"{match['player1']['last_name']} {match['player1']['first_name']} "
                                "vs"
                                f" {match['player2']['last_name']} {match['player2']['first_name']}"
                            )

                        # si le match existe et qu'il n'est pas terminé
                        if match is not None and not match["status"]:
                            # On récupère le gagnant du match
                            while True:
                                print("1." f"{match['player1']['last_name']} {match['player1']['first_name']} ")
                                print("2." f"{match['player2']['last_name']} {match['player2']['first_name']} ")
                                print("3. Match nul")
                                choice = input("Votre choix: ")
                                if choice == "1":
                                    winner = f"{match['player1']['last_name']} {match['player1']['first_name']} "
                                    compteur = compteur - 1
                                    break
                                elif choice == "2":
                                    winner = f"{match['player2']['last_name']} {match['player2']['first_name']} "
                                    compteur = compteur - 1
                                    break
                                elif choice == "3":
                                    winner = "Match nul"
                                    compteur = compteur - 1
                                    break
                            self.match_controller.update_match.result(tournament_id, match_id, winner)
                            print("Résultat du match enregistré")
                        else:
                            print("Match introuvable ou déjà terminé")

                if all(match["status"] for match in round_instance.matches):
                    self.round_controller.update_round.update(tournament_id, round_instance.id, round_instance)
                    print("Nouveaux classements des joueurs")

                    # Récupération des joueurs du tournoi
                    players = tournament.players

                    # Trier les joueurs par score
                    sorted_players = sorted(players, key=lambda x: x["score"], reverse=True)

                    for player in sorted_players:
                        print(f"{player['last_name']} {player['first_name']} - {player['score']}")
                    if tournament.curent_round < tournament.total_rounds:
                        # Création du round suivant
                        print("Voulez-vous créer un nouveau round ?")
                        print("1. Oui")
                        print("2. Non")
                        choice = input("Votre choix: ")
                        while True:
                            if choice == "1":
                                tournament.curent_round = tournament.curent_round + 1
                                self.tournament_controller.update_tournament.update(tournament)

                                # Création du nouveau round
                                name = f"Round {tournament.curent_round}"
                                start_date = datetime.now().strftime("%Y-%m-%d")
                                end_date = ""
                                status = False
                                new_round = Round(name, start_date, end_date, status)
                                new_round = self.round_controller.create_first_round.create(tournament_id, new_round)
                                print(f"Round: {new_round.name} - {new_round.start_date}")

                                # Tri des joueurs par score
                                sorted_players = sorted(players, key=lambda x: x["score"], reverse=True)

                                # Création des paires de joueurs par score
                                players_copy = list(sorted_players)

                                # tant qu'il y a plus d'un joueur dans la liste
                                while len(players_copy) > 1:
                                    # Création des matchs
                                    # Récupération du premier joueur
                                    player1 = players_copy.pop(0)
                                    available_opponents = list(
                                        filter(
                                            lambda x: x["id"] not in player1["opponents"],
                                            players_copy,
                                        )
                                    )
                                    if not available_opponents:
                                        # Tous les adversaires possibles ont déjà été rencontrés par player1
                                        # Peut-être afficher un message ou prendre une autre action
                                        break
                                    # trier les joueurs par score
                                    sorted_players_opponents = sorted(
                                        available_opponents, key=lambda x: x["score"], reverse=True
                                    )
                                    # Récupération du deuxième joueur
                                    player2 = sorted_players_opponents.pop(0)
                                    # on les supprime de la liste des joueurs restants
                                    match = Match(player1, player2)
                                    round_id = new_round.id
                                    print("Round ID f", round_id)

                                    # Ajout des matchs au round
                                    self.match_controller.create_match.create(
                                        tournament_id, match.serialize(), round_id
                                    )
                                    new_round.matches.append(match)
                                    if player1 in players_copy:
                                        players_copy.remove(player1)
                                    if player2 in players_copy:
                                        players_copy.remove(player2)
                                # Mise à jour du round
                                self.round_controller.update_new_round.update(tournament_id, new_round.id, new_round)
                                break
                self.tournament_controller.end_tournament.end(tournament)

        else:
            print("Tournoi introuvable. Veuillez entrer un ID de tournoi valide.")
