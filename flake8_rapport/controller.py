class Controller:
    def __init__(self, Players, Tournaments, Rounds, Matchs, View, Console, Table, print, Tree, Prompt, Tinydb, Query):
        # Models
        self.players = Players
        self.tournaments = Tournaments
        self.rounds = Rounds
        self.matchs = Matchs
        # View
        self.view = View
        # Rich
        self.console = Console
        self.table = Table
        self.print = print
        self.prompt = Prompt
        self.tree = Tree
        # DATABASE
        self.tinydb = Tinydb
        self.query = Query
        self.db = self.tinydb("db.json")
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
        self.view.prompt_add_player(self.query, self.players_table, tournaments.add_player, self.view.return_menu,
                                    self.menu, self.create_tournament)
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

            table = self.table()
            table2 = self.table()
            table3 = self.table()
            table.add_column("Nom du Tournoi", justify="center", style="cyan", no_wrap=True)
            table.add_column("Lieu", justify="center", style="cyan", no_wrap=True)
            table.add_column("Date", justify="center", style="cyan", no_wrap=True)
            table.add_column("Temps", justify="center", style="cyan", no_wrap=True)
            table.add_column("Nombre de rounds", justify="center", style="cyan", no_wrap=True)
            table.add_row(name, lieu, date, time, str(number_rounds))

            table2.add_column("Joueurs", justify="center", style="cyan", no_wrap=True)
            table2.add_column("Classement", justify="center", style="cyan", no_wrap=True)
            for a in joueurs:
                table2.add_row(a["prenom"], str(a["classement"]))

            table3.add_column("Match", justify="center", style="cyan", no_wrap=True)
            test = 0
            for a in rounds[3], rounds[9], rounds[15], rounds[21]:
                test += 1
                table3.add_row(f"[bold green]Round { test}:[/] {a[0][0][0]} vs {a[0][1][0]},"
                               f" {a[1][0][0]} vs {a[1][1][0]}, {a[2][0][0]} vs {a[2][1][0]},"
                               f" {a[3][0][0]} vs {a[3][1][0]}")
            arbre = self.tree("Tournoi")
            arbre.add(table)
            arbre.add(table2)
            arbre.add(table3)
            self.print(arbre)

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
                        search_tournament[0]["joueurs"].sort(key=lambda x: x.get("score"), reverse=True)

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
                        question_description = self.prompt.ask("[bold blue] Ajouter une description")
                        self.tournaments_table.update({"description": question_description}, verif.nom ==
                                                      search_tournament[0]["nom"])
                        self.view.return_menu(self.menu, self.create_round)

                self.first_round(search_tournament)
                self.after_first_round(search_tournament)
            else:
                self.view.phrasing_tournament()
                self.view.return_menu(self.menu, self.create_round)
        else:
            self.view.phrasing_tournament()
            self.view.return_menu(self.menu, self.create_round)

    def infos_players(self, player):
        player.sort(key=lambda x: x.get("prenom", x.get("classement")), reverse=True)
        for i in player:
            prenom = i["prenom"]
            nom = i["nom"]
            classement = i["classement"]
            score = i["score"]
            self.print(f"prenom: {prenom}, nom: {nom}, classement: {classement}, score: {score}")

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
                self.print(m)

            for m in Matchs.matchs:
                self.print("------------Match-----------")
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

                self.print("----------Résultat du match-----------")
                self.print(m)

            rounds.matchs = Matchs.matchs
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

            self.print(f"------------Round {round} terminée------------------")
            if round == 4:
                self.view.return_menu(self.menu, self.create_round)

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