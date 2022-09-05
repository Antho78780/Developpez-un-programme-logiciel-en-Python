from rich.console import Console
from rich.table import Table
from rich import print
from tinydb import TinyDB, Query

class Controller:
    def __init__(self, Players, Tournaments, Rounds, Matchs, View):
        # Models
        self.players = Players
        self.tournaments = Tournaments
        self.rounds = Rounds
        self.matchs = Matchs

        # View
        self.view = View

        # DATABASE
        self.db = TinyDB("db.json")
        self.players_table = self.db.table("players")
        self.tournaments_table = self.db.table("tournaments")

    # Create a tournament
    def create_tournament(self):
        tournaments = self.tournaments(
            self.view.prompt_name_tournament(self.view.prompt_name_tournament),
            self.view.prompt_lieu_tournament(self.view.prompt_lieu_tournament),
            self.view.prompt_date_tournament(self.view.prompt_date_tournament),
            self.view.prompt_time_tournament(self.view.prompt_time_tournament),
        )
        self.view.get_players_tournaments_database(self.get_players_tournament_database)
        self.view.prompt_add_player(Query, self.players_table, tournaments.add_player)
        serialized_tournament = {
            "nom": tournaments.name,
            "lieu": tournaments.lieu,
            "date": tournaments.date,
            "temps": tournaments.time,
            "number_round": tournaments.number_round,
            "rounds": tournaments.rounds,
            "joueurs": tournaments.add_player
        }
        self.tournaments_table.insert(serialized_tournament)
        self.view.phrasing_create_tournament()
        self.view.return_menu(self.menu, self.create_tournament)

    # Create a player
    def create_player(self):
        players = self.players(
            self.view.prompt_userName_player(self.view.prompt_userName_player),
            self.view.prompt_name_player(self.view.prompt_name_player),
            self.view.prompt_dateBirth_player(self.view.prompt_dateBirth_player),
            self.view.prompt_sex_player(self.view.prompt_sex_player),
            self.view.prompt_ranking_player()
        )
        player_serialized = {
            "prenom": players.first_name,
            "nom": players.name,
            "date_de_naissance": players.date_birth,
            "sexe": players.sex,
            "classement": players.ranking,
            "score": players.score
        }
        self.players_table.insert(player_serialized)
        self.view.phrasing_create_player()
        self.view.return_menu(self.menu, self.create_player)

    # Rapports
    def rapports(self):
        for i in self.tournaments_table.all():
            rounds = i["rounds"]
            name = i["nom"]
            lieu = i["lieu"]
            date = i["date"]
            time = i["temps"]
            number_rounds = i["number_round"]
            joueurs = i["joueurs"]
            array_player = []
            for j in joueurs:
                objet_player = {
                    "prenom": j["prenom"],
                    "classement": j["classement"]
                }
                array_player.append(objet_player)
            array_player.sort(key=lambda x: x.get("prenom", x.get("classement")))

            table = Table()
            table.add_column("Tournoi", justify="center", style="cyan", no_wrap=True)
            table.add_column("Lieu", justify="center", style="cyan", no_wrap=True)
            table.add_column("Date", justify="center", style="cyan", no_wrap=True)
            table.add_column("Temps", justify="center", style="cyan", no_wrap=True)
            table.add_column("Nombre de rounds", justify="center", style="cyan", no_wrap=True)
            table.add_row(name, lieu, date, time, str(number_rounds))

            console = Console()
            console.print(table)

        self.view.return_menu(self.menu, self.rapports)

    # Display of all registered players
    def get_players_database(self):
        if not self.players_table.all() == []:
            trie_first_name = self.players_table.all()
            trie_first_name.sort(key=lambda x: x.get("prenom", x.get("classement")))
            self.display_style_players_database(trie_first_name)

            self.view.phrasing_len_players(self.players_table.all)
            self.view.return_menu(self.menu, self.get_players_database)
        else:
            self.view.phrasing_none_players()
            self.view.return_menu(self.menu, self.get_players_database)

    # Display of all players who can be registered for the tournament
    def get_players_tournament_database(self):
        if not self.players_table.all() == []:
            self.display_style_players_database(self.players_table.all())
            self.view.phrasing_len_players(self.players_table.all)
        else:
            self.view.phrasing_none_players()
            self.view.return_menu(self.menu, self.get_players_database)

    # Display of all registered tournaments
    def get_tournaments_database(self):
        if not self.tournaments_table.all() == []:
            for i in self.tournaments_table.all():
                name = i["nom"]
                lieu = i["lieu"]
                date = i["date"]
                time = i["temps"]
                number_rounds = i["number_round"]

                table = Table()
                table.add_column("Nom du tournoi", justify="center", style="cyan", no_wrap=True)
                table.add_column("Lieu", justify="center", style="cyan", no_wrap=True)
                table.add_column("Date", justify="center", style="cyan", no_wrap=True)
                table.add_column("Temps", justify="center", style="cyan", no_wrap=True)
                table.add_column("Nombre de rounds", justify="center", style="cyan", no_wrap=True)

                table.add_row(name, lieu, date, time, str(number_rounds))

                console = Console()
                console.print(table)

            self.view.return_menu(self.menu, self.get_tournaments_database)
        else:
            self.view.phrasing_none_tournaments()
            self.view.return_menu(self.menu, self.get_tournaments_database)

    # Delete player's date of birth and gender
    @staticmethod
    def delete_date_birth_sex(tournament_joueurs):
        for trt in tournament_joueurs:
            try:
                trt.pop("date_de_naissance")
                trt.pop("sexe")
            except KeyError:
                print("Erreur")

    # Create round
    def create_round(self):
        verif = Query()
        if not self.tournaments_table.all() == []:
            table = Table()
            table.add_column("Tournoi", justify="center", style="cyan", no_wrap=True)
            for tournament in self.tournaments_table.all():
                table.add_row(tournament["nom"])
            console = Console()
            console.print(table)

            search_tournament = self.tournaments_table.search(verif.nom == self.view.prompt_phrasing_name_tournament())
            if search_tournament:
                print("[bold green]Vous avez accès au tournoi")
                for i in range(len(search_tournament[0]["rounds"])):
                    if search_tournament[0]["rounds"][i] == "ROUND 4":
                        search_tournament[0]["joueurs"].sort(key=lambda x: (x.get("score")), reverse=True)

                        print("<------------Classement des joueurs de fin de tournoi------------->")

                        table2 = Table()
                        table2.add_column("prenom", justify="center", style="cyan", no_wrap=True)
                        table2.add_column("nom", justify="center", style="cyan", no_wrap=True)
                        table2.add_column("classement", justify="center", style="cyan", no_wrap=True)
                        table2.add_column("score", justify="center", style="cyan", no_wrap=True)

                        for j in search_tournament[0]["joueurs"]:
                            table2.add_row(j["prenom"], j["nom"], str(j["classement"]), str(j["score"]))

                        console2 = Console()
                        console2.print(table2)
                        self.view.return_menu(self.menu, self.create_round)

                self.first_round(search_tournament)
                self.after_first_round(search_tournament)
            else:
                self.view.phrasing_tournament()
                self.view.return_menu(self.menu, self.create_round)
        else:
            self.view.phrasing_tournament()
            self.view.return_menu(self.menu, self.create_round)

    @staticmethod
    def infos_players(player):
        player.sort(key=lambda x: x.get("prenom", x.get("classement")), reverse=True)
        for i in player:
            prenom = i["prenom"]
            nom = i["nom"]
            classement = i["classement"]
            score = i["score"]
            print(f"prenom: {prenom}, nom: {nom}, classement: {classement}, score: {score}")

    # Create the 1st round
    def first_round(self, search_tournament):
        verif = Query()
        print("[bold green]---Round1 commencé---")
        rounds = self.rounds("ROUND 1", self.view.prompt_heure_start_round(),
                             self.view.prompt_date_start_round(self.view.prompt_date_start_round))

        search_tournament[0]["joueurs"].sort(key=lambda x: x.get("classement"))
        sup_moitie = search_tournament[0]["joueurs"][:4]
        inf_moitie = search_tournament[0]["joueurs"][4:]

        self.display_style_players_database(search_tournament[0]["joueurs"])

        Matchs = self.matchs()

        for i in range(0, 4):
            match = [sup_moitie[i]["prenom"]] + [sup_moitie[i]["score"]], \
                    [inf_moitie[i]["prenom"]] + [inf_moitie[i]["score"]]
            Matchs.matchs.append(match)

        for m in Matchs.matchs:
            print("<------------Match----------->")
            print(m)

            result_match_first_players = float(input(f"resultat du match pour {m[0][0]}: "))

            result_match_last_players = float(input(f"resultat du match pour {m[1][0]}: "))

            for i in search_tournament[0]["joueurs"]:
                if i["prenom"] == m[0][0]:
                    i["score"] += result_match_first_players
                    m[0][1] = i["score"]
                elif i["prenom"] == m[1][0]:
                    i["score"] += result_match_last_players
                    m[1][1] = i["score"]

            print("<----------Résultat du match----------->")
            print(m)

        rounds.matchs = Matchs.matchs
        rounds.heure_end = self.view.prompt_heure_end_round()
        rounds.date_end = self.view.prompt_date_end_round(self.view.prompt_date_end_round)
        self.tournaments_table.update({
            "rounds": [rounds.name, rounds.heure_start, rounds.date_start,
                       rounds.matchs, rounds.heure_end, rounds.date_end
                       ],
            "joueurs": search_tournament[0]["joueurs"]
        },
            verif.nom == search_tournament[0]["nom"]
        )
        search_tournament[0]["rounds"] = [rounds.name, rounds.heure_start, rounds.date_start,
                                          rounds.matchs, rounds.heure_end, rounds.date_end]

        print("<---------------Round 1 terminée-------------------------->")

    # Create a round after the first round
    def after_first_round(self, search_tournament):
        verif = Query()
        round = 1
        while search_tournament[0]["number_round"] > round:
            round += 1

            print(f"<--------------Round {round} commencé---------------->")
            rounds = self.rounds(
                f"ROUND {round}",
                self.view.prompt_heure_start_round(),
                self.view.prompt_date_start_round(self.view.prompt_date_start_round),
            )
            self.print_players_score_ranking(search_tournament)

            match1 = [search_tournament[0]["joueurs"][0]["prenom"]] + [search_tournament[0]["joueurs"][0]["score"]],\
                     [search_tournament[0]["joueurs"][1]["prenom"]] + [search_tournament[0]["joueurs"][1]["score"]]

            match2 = [search_tournament[0]["joueurs"][2]["prenom"]] + [search_tournament[0]["joueurs"][2]["score"]],\
                     [search_tournament[0]["joueurs"][3]["prenom"]] + [search_tournament[0]["joueurs"][3]["score"]]

            match3 = [search_tournament[0]["joueurs"][4]["prenom"]] + [search_tournament[0]["joueurs"][4]["score"]],\
                     [search_tournament[0]["joueurs"][5]["prenom"]] + [search_tournament[0]["joueurs"][5]["score"]]

            match4 = [search_tournament[0]["joueurs"][6]["prenom"]] + [search_tournament[0]["joueurs"][6]["score"]],\
                     [search_tournament[0]["joueurs"][7]["prenom"]] + [search_tournament[0]["joueurs"][7]["score"]]

            all_match = [match1, match2, match3, match4]
            Matchs = self.matchs()
            Matchs.matchs = all_match

            for m in Matchs.matchs:
                print(m)

            for m in Matchs.matchs:
                print("<------------Match----------->")
                print(m)

                result_match_first_players = float(input(f"resultat du match pour {m[0][0]}: "))

                result_match_last_players = float(input(f"resultat du match pour {m[1][0]}: "))

                for i in search_tournament[0]["joueurs"]:
                    if i["prenom"] == m[0][0]:
                        i["score"] += result_match_first_players
                        m[0][1] = i["score"]
                    elif i["prenom"] == m[1][0]:
                        i["score"] += result_match_last_players
                        m[1][1] = i["score"]

                print("<----------Résultat du match----------->")
                print(m)

            rounds.matchs = Matchs.matchs
            self.print_players_score_ranking(search_tournament)
            rounds.heure_end = self.view.prompt_heure_end_round()
            rounds.date_end = self.view.prompt_date_end_round(self.view.prompt_date_end_round)
            for i in self.tournaments_table.all():
                i["rounds"].extend([
                    rounds.name, rounds.heure_start, rounds.date_start,
                    rounds.matchs, rounds.heure_end, rounds.date_end
                ])
                self.tournaments_table.update({
                    "rounds": i["rounds"],
                    "joueurs": search_tournament[0]["joueurs"]},
                    verif.nom == search_tournament[0]["nom"])

            print(f"<------------Round {round} terminée------------------>")
            if round == 4:
                self.view.return_menu(self.menu, self.create_round)

    @staticmethod
    def print_players_score_ranking(search_tournament):
        search_tournament[0]["joueurs"].sort(key=lambda x: (x.get("score"), x.get("classement")))
        print("<------------Classement des joueurs------------->")
        for i in search_tournament[0]["joueurs"]:
            print(i)

    def display_style_players_database(self, players):
        table = Table()
        table.add_column("prenom", justify="center", style="cyan", no_wrap=True)
        table.add_column("nom", justify="center", style="cyan", no_wrap=True)
        table.add_column("date_de_naissance", justify="center", style="cyan", no_wrap=True)
        table.add_column("sexe", justify="center", style="cyan", no_wrap=True)
        table.add_column("classement", justify="center", style="cyan", no_wrap=True)
        table.add_column("score", justify="center", style="cyan", no_wrap=True)

        for player in players:
            table.add_row(player["prenom"], player["nom"], player["date_de_naissance"], player["sexe"],
                          str(player["classement"]), str(player["score"]))
        console = Console()
        console.print(table)

    # Player menu display
    def menu_player(self):
        self.view.menu_player(self.create_player, self.get_players_database, self.menu)

    # Tournament menu display
    def menu_tournament(self):
        self.view.menu_tournament(self.create_tournament, self.create_round, self.get_tournaments_database, self.menu)

    # General menu display
    def menu(self):
        self.view.menu(self.menu_player, self.menu_tournament, self.rapports)

    # Run the code
    def run(self):
        self.menu()
