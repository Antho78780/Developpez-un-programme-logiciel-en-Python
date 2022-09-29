import re
from rich import print
from rich.prompt import Prompt

verif_first_name = "^[A-Za-z]+$"
verif_date = "^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$"


class PromptRound:
    @staticmethod
    def prompt_heure_start_round():
        heure_start = Prompt.ask("[bold blue]Entrez l'heure du début du round: ")
        return heure_start

    @staticmethod
    def prompt_date_start_round(reset_date):
        date_start = Prompt.ask("[bold blue]Entrez la date de début du round: ")
        if re.match(verif_date, date_start):
            return date_start
        else:
            print("[bold red]Information incorrect")
            return reset_date(reset_date)

    @staticmethod
    def prompt_round():
        round = Prompt.ask("[bold blue]Entrez le nom du round: ")
        return round

    @staticmethod
    def prompt_nRound():
        print("Créer le round")
        nRound = int(Prompt.ask("[bold blue]Tapez le n° du round: "))
        return nRound

    @staticmethod
    def prompt_heure_end_round():
        heure_end = Prompt.ask("[bold blue]Entrez l'heure de fin du round: ")
        return heure_end

    @staticmethod
    def prompt_date_end_round(reset_date):
        date_end = Prompt.ask("[bold blue]Entrez la date de fin du round: ")
        if re.match(verif_date, date_end):
            return date_end
        else:
            print("[bold red]Information incorrect")
            return reset_date(reset_date)

    @staticmethod
    def printNRound(number_round):
        if number_round == 0:
            print("Il n'y a pas de round créer")

        elif number_round == 1:
            print("Il y a deja un round qui a été créer")

        else:
            print("Il y a deja plusieurs rounds qui ont été créer")