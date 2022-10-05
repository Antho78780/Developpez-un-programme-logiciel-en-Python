from controllers.player import Player

from models.player import Players

from views.player import PromptPlayer

from rich.console import Console
from rich.table import Table

from tinydb import TinyDB, Query

controllerPlayer = Player(Players, PromptPlayer, TinyDB, Query, Table, Console)
controllerPlayer.menu()
