class Player:
    def __init__(self, modelPlayer, viewPlayer, tinyDB, query, table, console):
        # Model
        self.modelPlayer = modelPlayer
        # View
        self.viewPlayer = viewPlayer
        # Rich
        self.table = table
        self.console = console
        # Database
        self.tinyDB = tinyDB
        self.query = query
        self.db = self.tinyDB("db.json")
        self.players_table = self.db.table("players")

    # Créer un joueur
    def create_player(self):
        players = self.modelPlayer(
            self.viewPlayer.prompt_userName_player(self.viewPlayer.prompt_userName_player),
            self.viewPlayer.prompt_name_player(self.viewPlayer.prompt_name_player),
            self.viewPlayer.prompt_dateBirth_player(self.viewPlayer.prompt_dateBirth_player),
            self.viewPlayer.prompt_sex_player(self.viewPlayer.prompt_sex_player),
            self.viewPlayer.prompt_ranking_player()
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
        self.viewPlayer.phrasing_create_player()
        self.viewPlayer.return_menu(self.menu_player, self.create_player)

    # Afficher les joueurs
    def get_players_database(self):
        if not self.players_table.all() == []:
            trie_first_name = self.players_table.all()
            trie_first_name.sort(key=lambda x: x.get("classement"))

            self.display_style_players_database(trie_first_name)
            self.viewPlayer.phrasing_len_players(self.players_table.all)
            self.viewPlayer.return_menu(self.menu, self.get_players_database)
        else:
            self.viewPlayer.phrasing_none_players()
            self.viewPlayer.return_menu(self.menu, self.get_players_database)

    # Modifier le classement d'un joueur
    def editRankPlayer(self):
        self.viewPlayer.promptEditRank(self.query, self.players_table)
        self.viewPlayer.return_menu(self.menu_player, self.editRankPlayer)

    # Afficher avec un meilleur design les joueurs
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

    # Afficher le score et le classement des joueurs dans l'ordre
    def print_players_score_ranking(self, search_tournament):
        search_tournament[0]["joueurs"].sort(key=lambda x: (x.get("score"), x.get("classement")))
        self.display_style_players_database(search_tournament[0]["joueurs"])

    # Affichage du menu des joueurs
    def menu_player(self):
        self.viewPlayer.menu_player(self.create_player, self.get_players_database, self.editRankPlayer, self.menu)

    # Affichage du menu général
    def menu(self):
        import main
        self.viewPlayer.menu(self.menu_player, main.comeTournament.menu_tournament, main.comeTournament.rapports)
