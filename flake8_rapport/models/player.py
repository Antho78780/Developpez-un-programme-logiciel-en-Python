class Players:
    def __init__(self, first_name, name, date_birth, sex, ranking):
        self.first_name = first_name
        self.name = name
        self.date_birth = date_birth
        self.sex = sex
        self.ranking = ranking
        self.score = 0.0

    def __str__(self):
        player_presentation = f"prenom: {self.first_name}, nom: {self.name}, date_de_naissance: {self.date_birth}"\
            f"sexe: {self.sex}, classement: {self.ranking}, score: {self.score}"
        return player_presentation
