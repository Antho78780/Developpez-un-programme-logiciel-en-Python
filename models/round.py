class Rounds:
    def __init__(self, name, heure_start, date_start):
        self.name = name
        self.heure_start = heure_start
        self.date_start = date_start
        self.date_end = ""
        self.heure_end = ""
        self.matchs = []

    def __str__(self):
        round_presentation = f"nom: {self.name}, heure_debut: {self.heure_start}, date_debut: {self.date_start},"\
                             f"heure_fin:{self.heure_end}, date_fin: {self.date_end}, matchs: {self.matchs}"
        return round_presentation
