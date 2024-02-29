class Player:
    def __init__(self, name, team):
        self.name = name
        self.team = team
        self.xp = 1500

    def introduce(self):
        print(f"Hello! I'm {self.name} and I play for {self.team}")


class Team:
    def __init__(self, team_name):
        self.name = team_name
        self.players = []

    def show_players(self):
        for player in self.players:
            player.introduce()

    def add_player(self, name):
        new_player = Player(name, self.name)
        self.players.append(new_player)


nico = Player(name="nico", team="Team X")

haribo = Player(name="haribo", team="Team Blue")

team_X = Team("Team X")

team_X.add_player("nico")

team_blue = Team("Team Blue")

team_blue.add_player("haribo")

team_blue.show_players()


class Dog:
    def __init__(self, name, breed, age):
        self.name = name
        self.breed = breed
        self.age = age

    def sleep(self):
        print("ZZZZZZ......")


class GuardDog(Dog):
    def __init__(self, name, breed):
        super().__init__(
            name,
            breed,
            5,
        )
        self.aggressive = True

    def rrrrrr(self):
        print("Stay away!")


class Puppy(Dog):
    def __init__(self, name, breed):
        super().__init__(
            name,
            breed,
            3,
        )
        self.spoiled = True

    def woof_woof(self):
        print("Woof Woof!")


ruffus = Puppy(
    name="Ruffus",
    breed="Beagle")

bibi = GuardDog(
    name="Bibi",
    breed="Dalmatian")

ruffus.sleep()

bibi.sleep()
