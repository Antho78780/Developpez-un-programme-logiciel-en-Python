class Round:
    def __init__(self, modelRound, modelMatch, viewPlayer, viewTournament, viewRound, tinyDB, query, console, table,
                 print, prompt):
        # Models
        self.modelRound = modelRound
        self.modelMatch = modelMatch
        # Views
        self.viewPlayer = viewPlayer
        self.viewTournament = viewTournament
        self.viewRound = viewRound
        # Rich
        self.console = console
        self.table = table
        self.print = print
        self.prompt = prompt
        # Database
        self.tinydb = tinyDB
        self.query = query
        self.db = self.tinydb("db.json")
        self.tournaments_table = self.db.table("tournaments")
        self.players_table = self.db.table("players")

    # Créer des rounds
    def create_round(self):
        import main
        verif = self.query()
        if not self.tournaments_table.all() == []:
            table = self.table()
            table.add_column("Tournoi", justify="center", style="cyan", no_wrap=True)
            for tournaments in self.tournaments_table.all():
                table.add_row(tournaments["nom"])
            console = self.console()
            console.print(table)
            search_tournament = self.tournaments_table.search(
                verif.nom == self.viewTournament.prompt_phrasing_name_tournament())
            if search_tournament:
                self.viewTournament.phrasing_tournament(search_tournament)
                for i in range(len(search_tournament[0]["rounds"])):
                    if search_tournament[0]["rounds"][i] == "ROUND 4":
                        search_tournament[0]["joueurs"].sort(key=lambda x: (x.get("score"), x.get("classement")))

                        self.viewTournament.phrasing_end_ranking()

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
                            self.viewPlayer.return_menu(main.comeTournament.menu_tournament, self.create_round)
                        else:
                            self.tournaments_table.update(
                                {"description": self.viewTournament.phrasing_prompt_description()}, verif.nom ==
                                search_tournament[0]["nom"])
                            self.viewPlayer.return_menu(main.comeTournament.menu_tournament, self.create_round)
                self.first_round(search_tournament)
                self.after_first_round(search_tournament)
            else:
                self.viewTournament.phrasing_tournament(search_tournament)
                self.viewPlayer.return_menu(main.comeTournament.menu_tournament, self.create_round)
        else:
            self.viewTournament.phrasing_none_tournaments()
            self.viewPlayer.return_menu(main.comeTournament.menu_tournament, self.create_round)

    # Créer le premier round
    def first_round(self, search_tournament):
        verif = self.query()
        self.viewRound.phrasing_number_round(1)
        rounds = self.modelRound("ROUND 1", self.viewRound.prompt_heure_start_round(),
                                 self.viewRound.prompt_date_start_round(self.viewRound.prompt_date_start_round))

        search_tournament[0]["joueurs"].sort(key=lambda x: x.get("classement"))
        sup_moitie = search_tournament[0]["joueurs"][:4]
        inf_moitie = search_tournament[0]["joueurs"][4:]

        import main
        main.comePlayer.display_style_players_database(search_tournament[0]["joueurs"])

        Matchs = self.modelMatch()

        for i in range(0, 4):
            match = [sup_moitie[i]["prenom"]] + [sup_moitie[i]["score"]], \
                    [inf_moitie[i]["prenom"]] + [inf_moitie[i]["score"]]
            Matchs.matchs.append(match)

        for m in Matchs.matchs:
            self.viewTournament.print_match()
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

            self.viewTournament.print_result_match()
            self.print(m)

        rounds.matchs = Matchs.matchs
        rounds.heure_end = self.viewRound.prompt_heure_end_round()
        rounds.date_end = self.viewRound.prompt_date_end_round(self.viewRound.prompt_date_end_round)
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

        self.viewRound.phrasing_number_end_round(1)

    # Créer les rounds après le 1er round
    def after_first_round(self, search_tournament):
        import main
        verif = self.query()
        round = 1
        while search_tournament[0]["number_round"] > round:
            round += 1

            self.viewRound.phrasing_number_round(round)
            rounds = self.modelRound(
                f"ROUND {round}", self.viewRound.prompt_heure_start_round(),
                self.viewRound.prompt_date_start_round(self.viewRound.prompt_date_start_round))
            main.comePlayer.print_players_score_ranking(search_tournament)
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
            Matchs = self.modelMatch()
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
                self.viewTournament.print_match()
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

                self.viewTournament.print_result_match()
                self.print(m)
            rounds.matchs = Matchs.matchs
            rounds.heure_end = self.viewRound.prompt_heure_end_round()
            rounds.date_end = self.viewRound.prompt_date_end_round(self.viewRound.prompt_date_end_round)
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

            self.viewRound.phrasing_number_end_round(round)
