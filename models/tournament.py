class Tournaments:
    def __init__(self, name, lieu, date, time, number_round=4, description=""):
        self.name = name
        self.lieu = lieu
        self.date = date
        self.time = time
        self.number_round = number_round
        self.rounds = []
        self.add_player = []
        self.description = description