class Controller:
    def __init__(self, View, Console, Table, print, Tree, Prompt, TinyDB, Query):
        # view
        self.view = View
        # Rich
        self.console = Console
        self.table = Table
        self.print = print
        self.tree = Tree
        self.prompt = Prompt
        # Database
        self.tinydb = TinyDB
        self.query = Query
        self.db = self.tinydb("db.json")
        self.players_table = self.db.table("players")
        self.tournaments_table = self.db.table("tournaments")


class ControllerGen(Controller):
    def __init__(self, Players, Tournaments, Rounds, Matchs, View, Console, Table, print, Tree, Prompt, TinyDB, Query):
        # Models
        super().__init__(View, Console, Table, print, Tree, Prompt, TinyDB, Query)

        self.players = Players
        self.tournaments = Tournaments
        self.rounds = Rounds
        self.matchs = Matchs

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

    def get_players_database(self):
        if not self.players_table.all() == []:
            trie_first_name = self.players_table.all()
            trie_first_name.sort(key=lambda x: x.get("classement"))

            self.display_style_players_database(trie_first_name)
            self.view.phrasing_len_players(self.players_table.all)
            self.view.return_menu(self.menu, self.get_players_database)
        else:
            self.view.phrasing_none_players()
            self.view.return_menu(self.menu, self.get_players_database)

    def editRankPlayer(self):
        self.view.promptEditRank(self.query, self.players_table, self.editRankPlayer, self.editRankPlayer,
                                 self.editRankPlayer)

    @staticmethod
    def delete_date_birth_sex(tournament_joueurs):
        for trt in tournament_joueurs:
            try:
                trt.pop("date_de_naissance")
                trt.pop("sexe")
            except KeyError:
                print("Erreur")

    def infos_players(self, player):
        player.sort(key=lambda x: x.get("prenom", x.get("classement")), reverse=True)
        for i in player:
            prenom = i["prenom"]
            nom = i["nom"]
            classement = i["classement"]
            score = i["score"]
            self.print(f"prenom: {prenom}, nom: {nom}, classement: {classement}, score: {score}")

    def print_players_score_ranking(self, search_tournament):
        search_tournament[0]["joueurs"].sort(key=lambda x: (x.get("score"), x.get("classement")))
        self.print("Joueurs:")
        self.display_style_players_database(search_tournament[0]["joueurs"])

    def display_style_players_database(self, players):
        table = self.table()
        table.add_column("prenom", justify="center", style="cyan", no_wrap=True)
        table.add_column("nom", justify="center", style="cyan", no_wrap=True)
        table.add_column("date_de_naissance", justify="center", style="cyan", no_wrap=True)
        table.add_column("sexe", justify="center", style="cyan", no_wrap=True)
        table.add_column("classement", justify="center", style="cyan", no_wrap=True)
        table.add_column("score", justify="center", style="cyan", no_wrap=True)

        for player in players:
            table.add_row(player["prenom"], player["nom"], player["date_de_naissance"], player["sexe"],
                          str(player["classement"]), str(player["score"]))
        console = self.console()
        console.print(table)

    def create_tournament(self):
        tournaments = self.tournaments(
            self.view.prompt_name_tournament(self.view.prompt_name_tournament),
            self.view.prompt_lieu_tournament(self.view.prompt_lieu_tournament),
            self.view.prompt_date_tournament(self.view.prompt_date_tournament),
            self.view.prompt_time_tournament(self.view.prompt_time_tournament),
        )
        self.view.get_players_tournaments_database(self.get_players_tournament_database)
        self.view.prompt_add_player(self.query, self.players_table, tournaments.add_player, self.create_tournament,
                                    self.create_tournament, self.create_tournament)
        serialized_tournament = {
            "nom": tournaments.name,
            "lieu": tournaments.lieu,
            "date": tournaments.date,
            "temps": tournaments.time,
            "number_round": tournaments.number_round,
            "rounds": tournaments.rounds,
            "joueurs": tournaments.add_player,
            "description": tournaments.description
        }
        self.tournaments_table.insert(serialized_tournament)
        self.view.phrasing_create_tournament()

    # Rapports
    def rapports(self):
        if len(self.tournaments_table.all()) > 1:
            self.print(f"Il y a {len(self.tournaments_table.all())} tournois enregistrés")
        else:
            self.print(f"[bold green]Il y a {len(self.tournaments_table.all())} tournoi enregistré")

        for i in self.tournaments_table.all():
            i["joueurs"].sort(key=lambda x: (x["classement"], x["prenom"]))
            rounds = i["rounds"]
            name = i["nom"]
            lieu = i["lieu"]
            date = i["date"]
            time = i["temps"]
            number_rounds = i["number_round"]
            joueurs = i["joueurs"]
            joueurs.sort(key=lambda x: (x.get("prenom"), x.get("classement")))

            table_tournaments = self.table()
            table_players = self.table()
            table_rounds = self.table()
            table_tournaments.add_column("Nom du Tournoi", justify="center", style="cyan", no_wrap=True)
            table_tournaments.add_column("Lieu", justify="center", style="cyan", no_wrap=True)
            table_tournaments.add_column("Date", justify="center", style="cyan", no_wrap=True)
            table_tournaments.add_column("Temps", justify="center", style="cyan", no_wrap=True)
            table_tournaments.add_column("Nombre de rounds", justify="center", style="cyan", no_wrap=True)
            table_tournaments.add_row(name, lieu, date, time, str(number_rounds))

            table_players.add_column("Joueurs", justify="center", style="cyan", no_wrap=True)
            table_players.add_column("Classement", justify="center", style="cyan", no_wrap=True)
            for a in joueurs:
                table_players.add_row(a["prenom"], str(a["classement"]))

            table_rounds.add_column("Match", justify="center", style="cyan", no_wrap=True)
            numero_round = 0
            for a in rounds[3], rounds[9], rounds[15], rounds[21]:
                numero_round += 1
                table_rounds.add_row(f"[bold green]Round {numero_round}:[/] {a[0][0][0]} vs {a[0][1][0]},"
                                     f" {a[1][0][0]} vs {a[1][1][0]}, {a[2][0][0]} vs {a[2][1][0]},"
                                     f" {a[3][0][0]} vs {a[3][1][0]}")
            arbre_tournaments = self.tree("Tournoi")
            arbre_tournaments.add(table_tournaments)
            arbre_tournaments.add(table_players)
            arbre_tournaments.add(table_rounds)
            self.print(arbre_tournaments)

    # Display of all players who can be registered for the tournament
    def get_players_tournament_database(self):
        if not self.players_table.all() == []:
            self.display_style_players_database(self.players_table.all())
            self.view.phrasing_len_players(self.players_table.all)
        else:
            self.view.phrasing_none_players()

    # Display of all registered tournaments
    def get_tournaments_database(self):
        if not self.tournaments_table.all() == []:
            for i in self.tournaments_table.all():
                name = i["nom"]
                lieu = i["lieu"]
                date = i["date"]
                time = i["temps"]
                number_rounds = i["number_round"]
                description = i["description"]

                table = self.table()
                table.add_column("Nom du tournoi", justify="center", style="cyan", no_wrap=True)
                table.add_column("Lieu", justify="center", style="cyan", no_wrap=True)
                table.add_column("Date", justify="center", style="cyan", no_wrap=True)
                table.add_column("Temps", justify="center", style="cyan", no_wrap=True)
                table.add_column("Nombre de rounds", justify="center", style="cyan", no_wrap=True)
                table.add_column("Description", justify="center", style="cyan", no_wrap=True)

                table.add_row(name, lieu, date, time, str(number_rounds), description)

                console = self.console()
                console.print(table)
        else:
            self.view.phrasing_none_tournaments()

    # Create round
    def create_round(self):
        verif = self.query()
        if not self.tournaments_table.all() == []:
            table = self.table()
            table.add_column("Tournoi", justify="center", style="cyan", no_wrap=True)
            for tournament in self.tournaments_table.all():
                table.add_row(tournament["nom"])
            console = self.console()
            console.print(table)

            search_tournament = self.tournaments_table.search(verif.nom == self.view.prompt_phrasing_name_tournament())
            if search_tournament:
                self.print("[bold green]Vous avez accès au tournoi")
                for i in range(len(search_tournament[0]["rounds"])):
                    if search_tournament[0]["rounds"][i] == "ROUND 4":
                        search_tournament[0]["joueurs"].sort(key=lambda x: (x.get("classement"), x.get("score")))

                        self.print("-------Classement des joueurs de fin de tournoi--------")

                        table2 = self.table()
                        table2.add_column("prenom", justify="center", style="cyan", no_wrap=True)
                        table2.add_column("nom", justify="center", style="cyan", no_wrap=True)
                        table2.add_column("classement", justify="center", style="cyan", no_wrap=True)
                        table2.add_column("score", justify="center", style="cyan", no_wrap=True)

                        for j in search_tournament[0]["joueurs"]:
                            table2.add_row(j["prenom"], j["nom"], str(j["classement"]), str(j["score"]))

                        console2 = self.console()
                        console2.print(table2)
                        if search_tournament[0]["description"] != "":
                            print("retour menu")
                        else:
                            question_description = self.prompt.ask("[bold blue] Ajouter une description")
                            self.tournaments_table.update({"description": question_description}, verif.nom ==
                                                          search_tournament[0]["nom"])
                self.first_round(search_tournament)
                self.after_first_round(search_tournament)
            else:
                self.view.phrasing_tournament()
        else:
            self.view.phrasing_tournament()

    # Create the 1st round
    def first_round(self, search_tournament):
        verif = self.query()
        self.print("[bold green]---Round1 commencé---")
        rounds = self.rounds("ROUND 1", self.view.prompt_heure_start_round(),
                             self.view.prompt_date_start_round(self.view.prompt_date_start_round))

        search_tournament[0]["joueurs"].sort(key=lambda x: x.get("classement"))
        sup_moitie = search_tournament[0]["joueurs"][:4]
        inf_moitie = search_tournament[0]["joueurs"][4:]
        self.print("Joueurs:")
        self.display_style_players_database(search_tournament[0]["joueurs"])

        Matchs = self.matchs()

        for i in range(0, 4):
            match = [sup_moitie[i]["prenom"]] + [sup_moitie[i]["score"]], \
                    [inf_moitie[i]["prenom"]] + [inf_moitie[i]["score"]]
            Matchs.matchs.append(match)

        for m in Matchs.matchs:
            self.print("-------------Match------------")
            self.print(m)

            result_match_first_players = float(self.prompt.ask(f"[bold blue]resultat du match pour {m[0][0]}: "))

            result_match_last_players = float(self.prompt.ask(f"[bold blue]resultat du match pour {m[1][0]}: "))

            for i in search_tournament[0]["joueurs"]:
                if i["prenom"] == m[0][0]:
                    i["score"] += result_match_first_players
                    m[0][1] = i["score"]
                elif i["prenom"] == m[1][0]:
                    i["score"] += result_match_last_players
                    m[1][1] = i["score"]

            self.print("-------------Résultat du Match------------")
            self.print(m)

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

        self.print("--------------Round 1 terminé----------------")

    # Create a round after the first round
    def after_first_round(self, search_tournament):
        verif = self.query()
        round = 1
        while search_tournament[0]["number_round"] > round:
            round += 1

            self.print(f"--------------Round {round} commencé----------------")
            rounds = self.rounds(
                f"ROUND {round}",
                self.view.prompt_heure_start_round(),
                self.view.prompt_date_start_round(self.view.prompt_date_start_round),
            )
            self.print_players_score_ranking(search_tournament)
            joueur1 = [search_tournament[0]["joueurs"][0]["prenom"]] + [search_tournament[0]["joueurs"][0]["score"]]
            joueur2 = [search_tournament[0]["joueurs"][1]["prenom"]] + [search_tournament[0]["joueurs"][1]["score"]]
            joueur3 = [search_tournament[0]["joueurs"][2]["prenom"]] + [search_tournament[0]["joueurs"][2]["score"]]
            joueur4 = [search_tournament[0]["joueurs"][3]["prenom"]] + [search_tournament[0]["joueurs"][3]["score"]]
            joueur5 = [search_tournament[0]["joueurs"][4]["prenom"]] + [search_tournament[0]["joueurs"][4]["score"]]
            joueur6 = [search_tournament[0]["joueurs"][5]["prenom"]] + [search_tournament[0]["joueurs"][5]["score"]]
            joueur7 = [search_tournament[0]["joueurs"][6]["prenom"]] + [search_tournament[0]["joueurs"][6]["score"]]
            joueur8 = [search_tournament[0]["joueurs"][7]["prenom"]] + [search_tournament[0]["joueurs"][7]["score"]]

            match1 = [joueur1, joueur2]
            match2 = [joueur3, joueur4]
            match3 = [joueur5, joueur6]
            match4 = [joueur7, joueur8]

            all_match = [match1, match2, match3, match4]
            Matchs = self.matchs()
            Matchs.matchs = all_match

            if round == 3:
                for i in search_tournament[0]["rounds"][9]:
                    if match1 == i or match2 == i:
                        newMatch1 = [joueur1, joueur3]
                        newMatch2 = [joueur2, joueur4]
                        all_match[0] = newMatch1
                        all_match[1] = newMatch2

                    if match3 == i or match4 == i:
                        newMatch3 = [joueur5, joueur7]
                        newMatch4 = [joueur6, joueur8]
                        all_match[2] = newMatch3
                        all_match[3] = newMatch4

            if round == 4:
                for i in search_tournament[0]["rounds"][15]:
                    match1 = [joueur1, joueur3]
                    match2 = [joueur2, joueur4]
                    match3 = [joueur5, joueur6]
                    match4 = [joueur7, joueur8]

                    if match1 == i or match2 == i:
                        newMatch1 = [joueur1, joueur4]
                        newMatch2 = [joueur3, joueur2]
                        all_match[0] = newMatch1
                        all_match[1] = newMatch2

                    if match3 == i or match4 == i:
                        newMatch3 = [joueur5, joueur8]
                        newMatch4 = [joueur6, joueur7]
                        all_match[2] = newMatch3
                        all_match[3] = newMatch4

            for m in Matchs.matchs:
                self.print("------------Match-----------")

                result_match_first_players = float(self.prompt.ask(f"[bold blue]resultat du match pour {m[0][0]}: "))

                result_match_last_players = float(self.prompt.ask(f"[bold blue]resultat du match pour {m[1][0]}: "))

                for i in search_tournament[0]["joueurs"]:
                    if i["prenom"] == m[0][0]:
                        i["score"] += result_match_first_players
                        m[0][1] = i["score"]
                    elif i["prenom"] == m[1][0]:
                        i["score"] += result_match_last_players
                        m[1][1] = i["score"]

                self.print("----------Résultat du match-----------")
                self.print(m)

            rounds.matchs = Matchs.matchs
            rounds.heure_end = self.view.prompt_heure_end_round()
            rounds.date_end = self.view.prompt_date_end_round(self.view.prompt_date_end_round)
            for i in self.tournaments_table.all():
                if verif.nom == search_tournament[0]["nom"]:
                    i["rounds"].extend([
                        rounds.name, rounds.heure_start, rounds.date_start,
                        rounds.matchs, rounds.heure_end, rounds.date_end
                    ])
                    self.tournaments_table.update({
                        "rounds": i["rounds"],
                        "joueurs": search_tournament[0]["joueurs"]},
                        verif.nom == search_tournament[0]["nom"]
                    )
                    search_tournament[0]["rounds"] = i["rounds"]

            self.print(f"------------Round {round} terminée------------------")
            if round == 4:
                print("Retour menu")

    def menu(self):
        self.view.menu(self.menu_player, self.menu_tournament)

    def menu_player(self):
        self.view.menu_player(self.create_player, self.get_players_database, self.editRankPlayer, self.menu)

    def menu_tournament(self):
        self.view.menu_tournament(self.create_tournament, self.create_round, self.get_tournaments_database, self.menu)

    def run(self):
        self.menu()
