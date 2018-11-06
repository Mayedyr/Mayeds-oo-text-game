from random import randint
from os import system
from winsound import *
from time import sleep

class Character():
    def __init__(self, race, school):
        self.race = race
        self.school = school

        self.MAXHEALTH = race.gethealth()
        self.health = race.gethealth()
        self.accuracy = race.getaccuracy()
        self.strength = race.getstrength()
        self.mana = race.getmana()
        self.armor = school.getarmor()
        self.skills = school.getskills()

    def changehealth(self, amount):
        self.health += amount

    def changemana(self, amount):
        self.mana += amount


class Player(Character):
    pass


class Enemy(Character):
    pass


class Race():
    def __init__(self):
        self._health = 0
        self._accuracy = 0
        self._strength = 0
        self._mana = 0

    def gethealth(self):
        return (self.health)

    def getaccuracy(self):
        return (self.accuracy)

    def getstrength(self):
        return (self.strength)

    def getmana(self):
        return (self.mana)


class School():
    def __init__(self):
        self._armor = 0
        self._skills = {}

    def getarmor(self):
        return(self.armor)

    def getskills(self):
        return(self.skills)

    def basicattack(self, cast, targ):
        attackroll = cast.accuracy + randint(-2, 3)
        damage = cast.strength + randint(-2, 3)

        if(isinstance(cast, Player)):
            noun1 = "Your"
            noun2 = "You"
        else:
            noun1 = "Their"
            noun2 = "They"

        if(attackroll > targ.armor):
            targ.changehealth(-1 * damage)
            system("cls")
            print("")

            text(noun1, " attack...  hit! ", noun2, " dealt ", str(damage), " damage!")
            text("-------------------------------")
        else:
            system("cls")
            print("")
            text(noun1, " attack...  missed!")
            text("-------------------------------")


class Orc(Race):
    health = 80
    accuracy = 10
    strength = 14
    mana = 0
    def __init__(self):
        self.health = 80
        self.accuracy = 10
        self.strength = 14
        self.mana = 0


class Elf(Race):
    health = 60
    accuracy = 14
    strength = 6
    mana = 100
    def __init__(self):
        self.health = 60
        self.accuracy = 14
        self.strength = 6
        self.mana = 100


class Dwarf(Race):
    health = 70
    accuracy = 12
    strength = 10
    mana = 40
    def __init__(self):
        self.health = 70
        self.accuracy = 12
        self.strength = 10
        self.mana = 40


class Tuskrider(School):
    armor = 11
    def __init__(self):
        self.armor = 11
        self.skills = {1: "basicattack (0)"}


class Warrior(School):
    armor = 11
    def __init__(self):
        self.armor = 11
        self.skills = {1: "basicattack (0)", 2: "heal (20)"}

    def heal(self, cast):
        heal = cast.MAXHEALTH - cast.health
        if(heal > 20):
            heal = 20
        if(cast.mana >= 20):
            cast.changehealth(heal)
            cast.changemana(-20)
            system("cls")
            print("")
            text("You healed ", str(heal), " health points!")
            text("-------------------------------")
        else:
            system("cls")
            print("")
            text("You did not have enough mana to heal!")
            text("-------------------------------")


class Wizard(School):
    armor = 9
    def __init__(self):
        self.armor = 9
        self.skills = {1: "basicattack (0)", 2: "heal (10)", 3: "lightning (30)"}

    def heal(self, cast):
        heal = cast.MAXHEALTH - cast.health
        if(heal > 20):
            heal = 20
        if(cast.mana >= 10):
            cast.changehealth(heal)
            cast.changemana(-10)
            system("cls")
            print("")
            text("You healed ", str(heal), " health points!")
            text("-------------------------------")
        else:
            system("cls")
            print("")
            text("You did not have enough mana to heal!")
            text("-------------------------------")

    def lightning(self, cast, targ):
        damage = 22 + randint(-4, 5)

        if(cast.mana >= 30):
            targ.changehealth(-1 * damage)
            cast.changemana(-30)
            system("cls")
            print("")
            text("Your attack...  hit! You dealt ", str(damage), " damage!")
            text("-------------------------------")
        else:
            system("cls")
            print("")
            text("Your attack...  failed! You did not have enough mana!")
            text("-------------------------------")


def text(*sentence):
    sleep(0.5)
    for seg in sentence:
        for char in seg:
            print(char, end = "", flush = True)
            if(char != " "):
                Beep(600, 40)
                sleep(0.01)
    print("")

def fightstats(player, opponent):
    system("cls")
    print("Your health: ", player.health)
    print("Your mana: ", player.mana)
    print("")
    print("Opponents health: ", opponent.health)
    print("\n")

def fightintro(player, opponent):
    system("cls")
    opponentrace = opponent.race.__class__.__name__
    opponentschool = opponent.school.__class__.__name__
    print("")
    text("     PREPARE TO FIGHT!")
    text("An ", opponentrace, " ", opponentschool, " has appeared!")
    text("-------------------------------")

def skillselect(player, opponent):
    while(True):
        fightstats(player, opponent)
        print(player.skills)
        text("Input number to select skill")
        skill = input(" > ")
        try:
            if(skill == "1"):
                player.school.basicattack(player, opponent)
                break
            elif(skill == "2"):
                player.school.heal(player)
                break
            elif(skill == "3"):
                player.school.lightning(player, opponent)
                break
            else:
                system("cls")
                print("")
                print("        invalid input")
                text("-------------------------------")
        except:
            system("cls")
            print("")
            print("        invalid input")
            text("-------------------------------")

def fight(player, opponent):
    fightintro(player, opponent)
    while(player.health > 0 and opponent.health > 0):
        skillselect(player, opponent)
        if(opponent.health <= 0):
            system("cls")
            print("")
            text("YES BOI U WIN")
            text("!!!!!!!!!!!!!")
            break
        opponent.school.basicattack(opponent, player)
    if(opponent.health > 0):
        system("cls")
        text("...")
        text("...")
        text("im dissapointed...")
        text("...")

def charactercreate():
    system("cls")
    while(True):
        text("\n 1 - Elf:\n   health: ", str(Elf.health), "\n   accuracy: ", str(Elf.accuracy),
        "\n   strength: ", str(Elf.strength),"\n   mana: ", str(Elf.mana),
        "\n 2 - Dwarf:\n   health: ", str(Dwarf.health), "\n   accuracy: ", str(Dwarf.accuracy),
        "\n   strength: ", str(Dwarf.strength),"\n   mana: ", str(Dwarf.mana),
        "\n\n Input number to select race")
        race = input(" > ")
        if(race == "1" or race.upper() == "ELF"):
            race = Elf()
            break
        elif(race == "2" or race.upper() == "DWARF"):
            race = Dwarf()
            break
        else:
            system("cls")
            print("Invalid input")

    system("cls")
    while(True):
        text("\n 1 - Warrior:\n   armor: ", str(Warrior.armor), "\n   skills: heal"
             "\n 2 - Wizard:\n   armor: ", str(Wizard.armor), "\n   skills: heal, lightning"
             "\n\n Input number to select school")
        school = input(" > ")
        if(school == "1"):
            school = Warrior()
            break
        elif(school == "2"):
            school = Wizard()
            break
        else:
            system("cls")
            print("Invalid input")

    character = {"race": race, "school": school}
    return(character)

PlaySound("C:\Projects\OOGame\Bonetrousle.wav",SND_ASYNC)

character = charactercreate()
pc = Player(character["race"], character["school"])
npc = Enemy(Orc(), Tuskrider())

fight(pc, npc)
