from models import Tournament
from controllers import TournamentController
from datetime import datetime
from tinydb import TinyDB


class TournamentView:
    def __init__(self):
        self.tournament_controller = TournamentController()

    def is_valid_date(self, date):
        try:
            datetime.strptime(date, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def is_valid_name(self, name):
        return name.isalpha()

    def tournament_menu(self):
        while True:
            print("Menu tournois")
            print("1. Créer un tournoi")
            print("2. Modifier un tournoi")
            print("3. Afficher les tournois")
            print("4. Retour")
            choice = input("Votre choix: ")
            if choice == "1":
                self.create_tournament()
            elif choice == "2":
                self.update_tournament()
            elif choice == "3":
                self.load_tournaments()
            elif choice == "4":
                break
            else:
                print("Choix invalide")
            print()

    def create_tournament(self):
        print("Création d'un tournoi")

        # Nom du tournoi
        while True:
            name = input("Nom: ")
            if self.is_valid_name(name):
                break
            else:
                print("Nom invalide")
        # Lieu du tournoi
        while True:
            location = input("Lieu: ")
            if self.is_valid_name(location):
                break
            else:
                print("Lieu invalide")

        # Date de début du tournoi
        start_date_default = datetime.now().strftime("%Y-%m-%d")
        start_date = f"{start_date_default}"

        # Date de fin du tournoi
        end_date = None

        # Nombre de tours
        while True:
            rounds_input = input("Nombre de tours (4 par défaut) : ")
            if rounds_input == "":
                total_rounds = 4
                break
            elif rounds_input.isdigit():
                total_rounds = int(rounds_input)
                break
            else:
                print("Nombre invalide")

        # Tour actuel
        current_round_default = 1
        current_round = current_round_default

        # Description du tournoi
        description = input("Description du tournoi (max 50 caractères) : ")

        # Limiter la description à 50 caractères
        if len(description) > 50:
            print("La description est trop longue. Limitez à 50 caractères.")
            description = description[:50]

        # Status du tournoi
        default_status = False
        status = default_status

        # Joueurs du tournoi
        players_db = TinyDB("database/players.json").table("players_table")
        players_data = players_db.all()
        players_list = {player["chess_id"]: player for player in players_data}

        selected_players_id = input("Entrez les chess_ids des joueurs à ajouter (séparés par des virgules) : ").split(
            ","
        )

        selected_players = [players_list.get(str(player_id)) for player_id in selected_players_id]

        # Rounds du tournoi
        rounds = []

        new_tournament = Tournament(
            name=name,
            location=location,
            start_date=start_date,
            end_date=end_date,
            total_rounds=total_rounds,
            curent_round=current_round,
            description=description,
            status=status,
            players=selected_players,
            rounds=rounds,
        )
        self.tournament_controller.create_tournaments.create(new_tournament)
        print(f"Tournoi {name} créé avec succès")

    def load_tournaments(self):
        print("Liste des tournois")
        tournaments = self.tournament_controller.load_tournaments.load()
        for tournament in tournaments:
            print(tournament)

    def update_tournament(self):
        print("Sélectionnez le tournoi à modifier")

        # Sélection de l'id du tournoi à modifier
        id_to_update = input("Identifiant: ")

        # Charge le tournoi à modifier
        tournament_to_update = self.tournament_controller.load_data_tournament.loaddata(id_to_update)
        print(f"Tournoi à modifier : {tournament_to_update}")

        # Nom du tournoi
        while True:
            name = input("Nom: ")
            if name == "":
                name = tournament_to_update.name
                break
            else:
                if self.is_valid_name(name):
                    break
                else:
                    print("Nom invalide")

        # Lieu du tournoi
        while True:
            location = input("Lieu: ")
            if location == "":
                location = tournament_to_update.location
                break
            else:
                if self.is_valid_name(location):
                    break
                else:
                    print("Lieu invalide")

        # Date de début du tournoi
        start_date = tournament_to_update.start_date

        # Date de fin du tournoi
        end_date = tournament_to_update.end_date

        # Nombre de tours
        while True:
            rounds_input = input("Nombre de tours (4 par défaut) : ")
            if rounds_input == "":
                total_rounds = tournament_to_update.total_rounds
                break
            elif rounds_input.isdigit():
                total_rounds = int(rounds_input)
                break
            else:
                print("Nombre invalide")

        # Tour actuel
        current_round = tournament_to_update.curent_round

        # Description du tournoi
        description = input("Description du tournoi (max 50 caractères) : ")

        # Limiter la description à 50 caractères
        if len(description) > 50:
            print("La description est trop longue. Limitez à 50 caractères.")
            description = description[:50]

        # Status du tournoi
        status = tournament_to_update.status

        # Joueurs du tournoi
        news_data = []
        selected_players = tournament_to_update.players
        news_data.append(selected_players)
        players_db = TinyDB("database/players.json").table("players_table")
        players_data = players_db.all()
        players_list = {player["chess_id"]: player for player in players_data}
        selected_players_id = input("Entrez les chess_ids des joueurs à ajouter (séparés par des virgules) : ").split(
            ","
        )
        for player_id in selected_players_id:
            selected_players.append(players_list.get(str(player_id)))
        news_data.append(selected_players)

        # Rounds du tournoi
        rounds = tournament_to_update.rounds

        # Mise à jour du tournoi
        updated_tournament = Tournament(
            id=id_to_update,
            name=name,
            location=location,
            start_date=start_date,
            end_date=end_date,
            total_rounds=total_rounds,
            curent_round=current_round,
            description=description,
            status=status,
            players=selected_players,
            rounds=rounds,
        )
        self.tournament_controller.update_tournament.update(updated_tournament)
        print(f"Tournoi {name} modifié avec succès")
