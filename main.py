from models.tournament import Tournaments
from models.round import Rounds
from models.match import Matchs
from models.player import Players

from views.tournament import PromptTournament
from views.player import PromptPlayer
from views.round import PromptRound

from tinydb import TinyDB, Query

from rich.table import Table
from rich.console import Console
from rich.tree import Tree
from rich import print
from rich.prompt import Prompt

from controllers.player import Player
from controllers.tournament import Tournament
from controllers.round import Round

comeTournament = Tournament(Tournaments, Rounds, Matchs, PromptTournament, PromptPlayer, PromptRound, TinyDB, Query,
                            Table, Console, Tree, print, Prompt)
comePlayer = Player(Players, PromptPlayer, TinyDB, Query, Table, Console)

comeRound = Round(Rounds, Matchs, PromptPlayer, PromptTournament, PromptRound, TinyDB, Query, Console, Table, print,
                  Prompt)

controllerPlayer = Player(Players, PromptPlayer, TinyDB, Query, Table, Console)
controllerPlayer.menu()
