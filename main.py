from controllers.player import Player

from models.player import Players

from views.player import PromptPlayer

from rich.console import Console
from rich.table import Table

from tinydb import TinyDB, Query

controllerPlayer = Player(Players, PromptPlayer, TinyDB, Query, Table, Console)
controllerPlayer.menu()
"""
controller = Controller(Players, Tournaments, Rounds, Matchs, PromptPlayer, PromptTournament,
                        PromptRound, Console, Table, print, Tree, Prompt, TinyDB, Query)
controller.run()
"""

