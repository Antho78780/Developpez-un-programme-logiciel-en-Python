import re
from rich.console import Console
from rich.table import Table

verif_first_name = "^[A-Za-z]+$"
verif_date = "^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$"

class View:
    @staticmethod
    def prompt_userName_player(reset_first_name):
        first_name = input("Saisisez le prenom du joueur: ")
        if re.match(verif_first_name, first_name):
            return first_name
        else:
            print("Information incorrect")
            return reset_first_name(reset_first_name)

    @staticmethod
    def prompt_name_player(reset_name):
        name = input("Saisisez le nom du joueur: ")
        if re.match(verif_first_name, name):
            return name
        else:
            print("Information incorrect")
            return reset_name(reset_name)

    @staticmethod
    def prompt_dateBirth_player(reset_date_birth):
        date_birth = input("Saisisez la date de naissance du joueur: ")
        if re.match(verif_date, date_birth):
            return date_birth
        else:
            print("Information incorrect")
            return reset_date_birth(reset_date_birth)

    @staticmethod
    def prompt_sex_player(reset_sex):
        sex = input("Saisisez la civilité du joueur: ")
        verif_genre = "^[e-oE-O]+$"
        if re.match(verif_genre, sex):
            return sex
        else:
            print("Information incorrect")
            return reset_sex(reset_sex)

    @staticmethod
    def prompt_ranking_player():
        ranking = int(input("Saisisez le classement du joueur: "))
        if ranking == 0:
            return ranking
        else:
            return ranking

    @staticmethod
    def prompt_name_tournament(reset_name):
        name = input("Saisisez le nom du tournoi: ")
        if re.match(verif_first_name, name):
            return name
        else:
            print("Information incorrect")
            return reset_name(reset_name)

    @staticmethod
    def prompt_lieu_tournament(reset_lieu):
        lieu = input("Saisisez le lieu du tournoi: ")
        if re.match(verif_first_name, lieu):
            return lieu
        else:
            print("Information incorrect")
            return reset_lieu(reset_lieu)

    @staticmethod
    def prompt_date_tournament(reset_date):
        date = input("Saisisez la date du tournoi: ")
        if re.match(verif_date, date):
            return date
        else:
            print("Information incorrect")
            return reset_date(reset_date)

    @staticmethod
    def prompt_add_player(query, players, add_player):
        player = query()
        while len(add_player) < 8:
            first_name = input(
                f"Entrez le prenom du joueur{len(add_player) +1}: ")
            name = input(f"Entrez le nom du joueur{len(add_player) +1}: ")
            recupFirst_name = players.search(player.prenom == first_name)
            recup_name = players.search(player.nom == name)
            if recupFirst_name and recup_name:
                add_player.append(recupFirst_name[0])
            else:
                print("Joueur introuvable")

    @staticmethod
    def prompt_time_tournament(reset_time):
        time = input("Saisisez le temps du tournoi(bullet,blitz,coup-rapide):")
        if time == "bullet" or time == "Bullet" or time == "BULLET":
            return time
        elif time == "blitz" or time == "Blitz" or time == "BLITZ":
            return time
        elif time == "coup-rapide" or time == "Coup-rapide" or time == "COUP-RAPIDE":
            return time
        else:
            print("Information incorrect")
            return reset_time(reset_time)

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

        question = int(input("Saisisez 1, 2, 3, 4: "))
        if question == 1:
            menu1()
        elif question == 2:
            menu2()
        elif question == 3:
            menu3()
        elif question == 4:
            exit()
        else:
            print("Information incorrect")
            View.menu(menu1, menu2, menu3)

    @staticmethod
    def menu_player(menu1, menu2, menu3):

        table = Table()
        table.add_column("MENU JOUEURS", justify="center", style="cyan", no_wrap=True)
        table.add_row("1: Ajout de joueur")
        table.add_row("2: Joueurs enregistrés")
        table.add_row("3: Retour")
        console = Console()
        console.print(table)

        question = int(input("Saisisez 1, 2, 3: "))
        if question == 1:
            menu1()
        elif question == 2:
            menu2()
        elif question == 3:
            menu3()
        else:
            print("Information incorrect")
            View.menu_player(menu1, menu2, menu3)

    @staticmethod
    def menu_tournament(menu1, menu2, menu3, menu4, ):

        table = Table()
        table.add_column("MENU TOURNOI", justify="center", style="cyan", no_wrap=True)
        table.add_row("1: Créer un tournoi")
        table.add_row("2: Accéder au tournoi")
        table.add_row("3: Voir les tournois")
        table.add_row("4: Retour")
        console = Console()
        console.print(table)

        question = int(input("Saisisez 1, 2, 3, 4: "))
        if question == 1:
            menu1()
        elif question == 2:
            menu2()
        elif question == 3:
            menu3()
        elif question == 4:
            menu4()
        else:
            print("Informations incorrect")
            View.menu_tournament(menu1, menu2, menu3, menu4)

    @staticmethod
    def get_players_tournaments_database(get_players_tournament_database):
        print("Joueurs enregistré: ")
        get_players_tournament_database()
        print("Ajouter 8 joueurs: ")

    @staticmethod
    def phrasing_create_tournament():
        print("Tournoi créer")

    @staticmethod
    def phrasing_create_player():
        print("Joueur créer")

    @staticmethod
    def phrasing_none_players():
        print("Aucun joueurs enregistrés")

    @staticmethod
    def phrasing_none_tournaments():
        print("Il n'y a pas de tournois dans la base de donnée")

    @staticmethod
    def return_menu(menu, choice_menu):
        question = input("Retourner au menu: y/n ")
        if question == "y" or question == "Y":
            menu()
        elif question == "n" or question == "N":
            choice_menu()
        else:
            print("Informations incorrect")
            View.return_menu(menu, choice_menu)

    @staticmethod
    def phrasing_len_players(players_table_all):
        if len(players_table_all()) == 8:
            print(f"Il y a {len(players_table_all())} joueurs qui peuvent participer au tournoi")

        elif len(players_table_all()) < 8:
            print(f"Il n'y a que {len(players_table_all())} joueurs")
            print("Il n'y a pas assez de joueurs pour participer a un tournoi")

        else:
            print("Il y a que 8 joueurs maximums qui peuvent participer à un tournoi")
            print(f"Il y a {len(players_table_all())} deja enregistrés")

    @staticmethod
    def prompt_round():
        round = input("Entrez le nom du round: ")
        return round

    @staticmethod
    def prompt_phrasing_name_tournament():
        tournament = input("Tapez le nom du tournoi: ")
        return tournament

    @staticmethod
    def prompt_heure_start_round():
        heure_start = input("Entrez l'heure du début du round: ")
        return heure_start

    @staticmethod
    def prompt_date_start_round(reset_date):
        date_start = input("Entrez la date de début du round: ")
        if re.match(verif_date, date_start):
            return date_start
        else:
            print("Information incorrect")
            return reset_date(reset_date)

    @staticmethod
    def prompt_heure_end_round():
        heure_end = input("Entrez l'heure de fin du round: ")
        return heure_end

    @staticmethod
    def prompt_date_end_round(reset_date):
        date_end = input("Entrez la date de fin du round: ")
        if re.match(verif_date, date_end):
            return date_end
        else:
            print("Information incorrect")
            return reset_date(reset_date)

    @staticmethod
    def prompt_nRound():
        print("Créer le round")
        nRound = int(input("Tapez le n° du round: "))
        return nRound

    @staticmethod
    def printNRound(number_round):
        if number_round == 0:
            print("Il n'y a pas de round créer")

        elif number_round == 1:
            print("Il y a deja un round qui a été créer")

        else:
            print("Il y a deja plusieurs rounds qui ont été créer")

    @staticmethod
    def phrasing_tournament():
        print("Tournoi introuvable")
