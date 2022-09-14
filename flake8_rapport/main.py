from controller import Controller
from models import Players, Tournaments, Rounds, Matchs
from view import View
from rich.console import Console
from rich.table import Table
from rich import print
from rich.tree import Tree
from rich.prompt import Prompt
from tinydb import TinyDB, Query

controller = Controller(Players, Tournaments, Rounds, Matchs, View, Console, Table, print, Tree, Prompt, TinyDB, Query)
controller.run()
