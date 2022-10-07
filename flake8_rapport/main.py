from models.player import Players

from views.player import PromptPlayer

from tinydb import TinyDB, Query

from rich.table import Table
from rich.console import Console


from controllers.player import Player
controllerPlayer = Player(Players, PromptPlayer, TinyDB, Query, Table, Console)
controllerPlayer.menu()
