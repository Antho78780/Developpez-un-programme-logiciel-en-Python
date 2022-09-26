from controller import ControllerGen
from models import Players, Tournaments, Rounds, Matchs
from view import Views, ViewPromptPlayer, ViewPromptTournament, ViewPromptRound, ViewPhrasing
from rich.console import Console
from rich.table import Table
from rich import print
from rich.tree import Tree
from rich.prompt import Prompt
from tinydb import TinyDB, Query

views = Views(ViewPromptPlayer, ViewPromptTournament, ViewPromptRound, ViewPhrasing)
controller = ControllerGen(Players, Tournaments, Rounds, Matchs, views, Console, Table, print, Tree, Prompt, TinyDB, Query)
controller.run()
