from controller import Controller
from view import View
from models import Players, Tournaments, Rounds, Matchs
from rich.console import Console
from rich.table import Table
from rich import print
from rich.tree import Tree
from rich.prompt import Prompt
from tinydb import TinyDB, Query

controller = Controller(View, Players, Tournaments, Rounds, Matchs, Console, Table, print, Tree, Prompt, TinyDB, Query)
controller.run()
