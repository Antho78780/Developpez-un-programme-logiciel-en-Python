from models.tournament import Tournaments
from models.round import Rounds
from models.match import Matchs

from views.tournament import PromptTournament
from views.player import PromptPlayer
from views.round import PromptRound

from tinydb import TinyDB, Query

from rich.table import Table
from rich.console import Console
from rich.tree import Tree
from rich import print
from rich.prompt import Prompt

from controllers import tournament

comeTournament = tournament.Tournament(Tournaments, Rounds, Matchs, PromptTournament, PromptPlayer,
                                       PromptRound, TinyDB, Query, Table, Console, Tree, print, Prompt)


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

    def editRankPlayer(self):
        self.viewPlayer.promptEditRank(self.query, self.players_table)
        self.viewPlayer.return_menu(self.menu_player, self.editRankPlayer)

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

    def print_players_score_ranking(self, search_tournament):
        search_tournament[0]["joueurs"].sort(key=lambda x: (x.get("score"), x.get("classement")))
        self.display_style_players_database(search_tournament[0]["joueurs"])

    def menu_player(self):
        self.viewPlayer.menu_player(self.create_player, self.get_players_database, self.editRankPlayer, self.menu)

    def menu(self):
        self.viewPlayer.menu(self.menu_player, comeTournament.menu_tournament, comeTournament.rapports)
