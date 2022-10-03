import re
from rich.console import Console
from rich import print
from rich.prompt import Prompt
from rich.table import Table

verif_first_name = "^[A-Za-z]+$"
verif_date = "^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$"


class PromptTournament:
    @staticmethod
    def prompt_name_tournament(reset_name):
        name = Prompt.ask("[bold blue]Saisisez le nom du tournoi")
        if re.match(verif_first_name, name):
            return name
        else:
            print("[bold red]Information incorrect")
            return reset_name(reset_name)

    @staticmethod
    def prompt_lieu_tournament(reset_lieu):
        lieu = Prompt.ask("[bold blue]Saisisez le lieu du tournoi")
        if re.match(verif_first_name, lieu):
            return lieu
        else:
            print("[bold red]Information incorrect")
            return reset_lieu(reset_lieu)

    @staticmethod
    def prompt_date_tournament(reset_date):
        date = Prompt.ask("[bold blue]Saisisez la date du tournoi")
        if re.match(verif_date, date):
            return date
        else:
            print("[bold red]Information incorrect")
            return reset_date(reset_date)

    @staticmethod
    def prompt_time_tournament(reset_time):
        time = Prompt.ask("[bold blue]Saisisez le temps du tournoi(bullet,blitz,coup-rapide)")
        if time == "bullet" or time == "Bullet" or time == "BULLET":
            return time
        elif time == "blitz" or time == "Blitz" or time == "BLITZ":
            return time
        elif time == "coup-rapide" or time == "Coup-rapide" or time == "COUP-RAPIDE":
            return time
        else:
            print("[bold red]Information incorrect")
            return reset_time(reset_time)

    @staticmethod
    def phrasing_create_tournament():
        print("[bold green]Tournoi créer")

    @staticmethod
    def phrasing_none_tournaments():
        print("[bold red]Il n'y a pas de tournois dans la base de donnée")

    @staticmethod
    def prompt_phrasing_name_tournament():
        tournament = Prompt.ask("[bold blue]Tapez le nom du tournoi: ")
        return tournament

    @staticmethod
    def phrasing_tournament(search_tournament):
        if search_tournament:
            print("[bold green]Vous avez accés au tournoi")
        else:
            print("[bold red]Tournoi introuvable")

    @staticmethod
    def phrasing_prompt_description():
        question_description = Prompt.ask("[bold blue] Ajouter une description")
        return question_description

    @staticmethod
    def menu_tournament(menu1, menu2, menu3, menu4):

        table = Table()
        table.add_column("MENU TOURNOI", justify="center", style="cyan", no_wrap=True)
        table.add_row("1: Créer un tournoi")
        table.add_row("2: Accéder au tournoi")
        table.add_row("3: Voir les tournois")
        table.add_row("4: Retour")
        console = Console()
        console.print(table)

        question = int(Prompt.ask("[bold blue]Saisisez 1, 2, 3, 4: "))
        if question == 1:
            menu1()
        elif question == 2:
            menu2()
        elif question == 3:
            menu3()
        elif question == 4:
            menu4()
        else:
            print("[bold red]Informations incorrect")
            PromptTournament.menu_tournament(menu1, menu2, menu3, menu4)

    @staticmethod
    def phrasingRapport(tournament):
        if len(tournament.all()) > 1:
            print(f"Il y a {len(tournament.all())} tournois enregistrés")
        else:
            print(f"[bold green]Il y a {len(tournament.all())} tournoi enregistré")

    @staticmethod
    def phrasing_end_ranking():
        print("-------Classement des joueurs de fin de tournoi--------")

    @staticmethod
    def print_match():
        print("-------------Match------------>")

    @staticmethod
    def print_result_match():
        print("-------------Résultat du Match------------")

    @staticmethod
    def return_menu(menu, choice_menu):
        question = Prompt.ask("[bold blue]Retourner au menu: y/n ")
        if question == "y" or question == "Y":
            menu()
        elif question == "n" or question == "N":
            choice_menu()
        else:
            print("[bold red]Informations incorrect")
            PromptTournament.return_menu(menu, choice_menu)

    @staticmethod
    def phrasing_error():
        print("[bold red]Il n'y a rien dans la base de donnée")





