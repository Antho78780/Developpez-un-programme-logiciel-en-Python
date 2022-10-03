import re
from rich import print
from rich.prompt import Prompt
from rich.console import Console
from rich import print
from rich.prompt import Prompt
from rich.table import Table

verif_first_name = "^[A-Za-z]+$"
verif_date = "^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$"


class PromptPlayer:
    @staticmethod
    def prompt_userName_player(reset_first_name):
        first_name = Prompt.ask("[bold blue]Saisisez le prenom du joueur")
        if re.match(verif_first_name, first_name):
            return first_name
        else:
            print("[bold red]Information incorrect")
            return reset_first_name(reset_first_name)

    @staticmethod
    def prompt_name_player(reset_name):
        name = Prompt.ask("[bold blue]Saisisez le nom du joueur")
        if re.match(verif_first_name, name):
            return name
        else:
            print("[bold red]Information incorrect")
            return reset_name(reset_name)

    @staticmethod
    def prompt_dateBirth_player(reset_date_birth):
        date_birth = Prompt.ask("[bold blue]Saisisez la date de naissance du joueur")
        if re.match(verif_date, date_birth):
            return date_birth
        else:
            print("[bold red]Information incorrect")
            return reset_date_birth(reset_date_birth)

    @staticmethod
    def prompt_sex_player(reset_sex):
        sex = Prompt.ask("[bold blue]Saisisez la civilité du joueur")
        verif_genre = "^[e-oE-O]+$"
        if re.match(verif_genre, sex):
            return sex
        else:
            print("[bold red]Information incorrect")
            return reset_sex(reset_sex)

    @staticmethod
    def prompt_ranking_player():
        ranking = int(Prompt.ask("[bold blue]Saisisez le classement du joueur"))
        if ranking == 0:
            return ranking
        else:
            return ranking

    @staticmethod
    def phrasing_create_player():
        print("[bold green]Joueur créer")

    @staticmethod
    def phrasing_none_players():
        print("[bold red]Aucun joueurs enregistrés")

    @staticmethod
    def prompt_add_player(query, players, add_player, return_menu, menu, cr_tr):
        player = query()
        if len(players.all()) < 8:
            return_menu(menu, cr_tr)
        else:
            while len(add_player) < 8:
                first_name = Prompt.ask(f"[bold blue]Entrez le prenom du joueur{len(add_player) + 1}")
                name = Prompt.ask(f"[bold blue]Entrez le nom du joueur{len(add_player) + 1}")
                recupFirst_name = players.search(player.prenom == first_name)
                recup_name = players.search(player.nom == name)
                if recupFirst_name and recup_name:
                    add_player.append(recupFirst_name[0])
                else:
                    print("[bold red]Joueur introuvable")

    @staticmethod
    def promptEditRank(query, players):
        verif = query()
        print(players.all())
        first_name = Prompt.ask("[bold blue]Saissisez le prenom du joueur")
        name = Prompt.ask("[bold blue]Saissisez le nom du joueur")
        if players.search(verif.prenom == first_name) and players.search(verif.nom == name):
            rank = int(Prompt.ask(f"[bold blue]Rentrer le nouveau classement de {first_name} {name}"))
            players.update({"classement": rank}, verif.prenom == first_name)
            print("[bold green]Classement mis à jour")

        else:
            print("[bold red]Joueur introuvable")

    @staticmethod
    def menu_player(menu1, menu2, menu3, menu4):

        table = Table()
        table.add_column("MENU JOUEURS", justify="center", style="cyan", no_wrap=True)
        table.add_row("1: Ajout de joueur")
        table.add_row("2: Joueurs enregistrés")
        table.add_row("3: Modifier le classement d'un joueur")
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
            print("[bold red]Information incorrect")
            PromptPlayer.menu_player(menu1, menu2, menu3, menu4)

    @staticmethod
    def phrasing_len_players(players_table_all):
        if len(players_table_all()) == 8:
            print(f"[bold green]Il y a {len(players_table_all())} joueurs qui peuvent participer au tournoi")

        elif len(players_table_all()) < 8:
            print(f"[bold red]Il n'y a que {len(players_table_all())} joueurs")
            print("[bold red]Il n'y a pas assez de joueurs pour participer a un tournoi")

        else:
            print("[bold red]Il y a que 8 joueurs maximums qui peuvent participer à un tournoi")
            print(f"[bold red]Il y a {len(players_table_all())} deja enregistrés")

    @staticmethod
    def menu(menu1, menu2, menu3):

        table = Table()
        table.add_column("MENU PRINCIPAL", justify="center", style="cyan", no_wrap=True)
        table.add_row("1: Joueurs")
        table.add_row("2: Tournois")
        table.add_row("3: Rapports")
        table.add_row("4: Quitter")
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
            exit()
        else:
            print("[bold red]Information incorrect")
            PromptPlayer.menu(menu1, menu2, menu3)

    @staticmethod
    def return_menu(menu, choice_menu):
        question = Prompt.ask("[bold blue]Retourner au menu: y/n ")
        if question == "y" or question == "Y":
            menu()
        elif question == "n" or question == "N":
            choice_menu()
        else:
            print("[bold red]Informations incorrect")
            PromptPlayer.return_menu(menu, choice_menu)

    @staticmethod
    def phrasing_error():
        print("Il n'y a rien dans la base de donnée")
