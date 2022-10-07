class Tournament:
    def __init__(self, modelTournament, modelRounds, modelMatchs, viewTournament, viewPlayer, viewRound,
                 tinyDB, query, table, console, tree, print, prompt):
        # Model
        self.modelTournament = modelTournament
        self.modelRounds = modelRounds
        self.modelMatchs = modelMatchs
        # views
        self.viewTournament = viewTournament
        self.viewPlayer = viewPlayer
        self.viewRound = viewRound
        # rich
        self.tree = tree
        self.print = print
        self.table = table
        self.console = console
        self.prompt = prompt
        # database
        self.tinyDB = tinyDB
        self.query = query
        self.db = self.tinyDB("db.json")
        self.tournaments_table = self.db.table("tournaments")
        self.players_table = self.db.table("players")

    def create_tournament(self):
        tournaments = self.modelTournament(
            self.viewTournament.prompt_name_tournament(self.viewTournament.prompt_name_tournament),
            self.viewTournament.prompt_lieu_tournament(self.viewTournament.prompt_lieu_tournament),
            self.viewTournament.prompt_date_tournament(self.viewTournament.prompt_date_tournament),
            self.viewTournament.prompt_time_tournament(self.viewTournament.prompt_time_tournament),
        )
        self.get_players_tournament_database()
        self.viewPlayer.prompt_add_player(self.query, self.players_table, tournaments.add_player, self.create_tournament,
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
        self.viewTournament.phrasing_create_tournament()
        self.viewTournament.return_menu(self.menu_tournament, self.create_tournament)

    def get_players_tournament_database(self):
        import main
        from controllers.player import Player
        comePlayer = Player(main.Players, main.PromptPlayer, main.TinyDB, main.Query, main.Table, main.Console)
        if not self.players_table.all() == []:
            comePlayer.display_style_players_database(self.players_table.all())
            self.viewPlayer.phrasing_len_players(self.players_table.all)
        else:
            self.viewPlayer.phrasing_none_players()

    def rapports(self):
        self.viewTournament.phrasingRapport(self.tournaments_table)
        try:
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
        except IndexError:
            self.viewTournament.phrasing_error2()
            self.viewTournament.return_menu(self.menu_tournament, self.rapports)

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
                self.viewTournament.return_menu(self.menu_tournament, self.get_tournaments_database)
        else:
            self.viewTournament.phrasing_none_tournaments()
            self.viewTournament.return_menu(self.menu_tournament, self.get_tournaments_database)

    def menu_tournament(self):
        import main
        from controllers.round import Round
        comeRound = Round(main.Rounds, main.Matchs, main.PromptPlayer, main.PromptTournament, main.PromptRound,
                          main.TinyDB, main.Query, main.Console, main.Table, main.print, main.Prompt)

        self.viewTournament.menu_tournament(self.create_tournament, comeRound.create_round,
                                            self.get_tournaments_database, self.menu)

    def menu(self):
        import main
        from controllers.player import Player
        comePlayer = Player(main.Players, main.PromptPlayer, main.TinyDB, main.Query, main.Table, main.Console)
        comePlayer.menu()


