from controller import Controller
from models import Players
from models import Tournaments
from models import Rounds
from models import Matchs
from view import View

controller = Controller(Players, Tournaments, Rounds, Matchs, View)
controller.run()
