from controller import Controller
from controllers.player import Player
from controllers.tournament import Tournament

from models.player import Players
from models.tournament import Tournaments
from models.round import Rounds
from models.match import Matchs

from views.player import PromptPlayer
from views.tournament import PromptTournament
from views.round import PromptRound

from rich.console import Console
from rich.table import Table
from rich import print
from rich.tree import Tree
from rich.prompt import Prompt

from tinydb import TinyDB, Query

controller = Controller(Players, Tournaments, Rounds, Matchs, PromptPlayer, PromptTournament,
                        PromptRound, Console, Table, print, Tree, Prompt, TinyDB, Query)
controller.run()

