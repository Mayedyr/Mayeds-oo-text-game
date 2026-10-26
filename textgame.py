from __future__ import annotations

import random
import sys
import time
from dataclasses import dataclass, field
from typing import Callable, Mapping, TypeVar


HEAL_AMOUNT = 20
LIGHTNING_DAMAGE = 22
SEPARATOR = "-------------------------------"


@dataclass(frozen=True)
class Race:
    name: str
    health: int
    accuracy: int
    strength: int
    mana: int


@dataclass(frozen=True)
class Skill:
    name: str
    mana_cost: int
    effect: Callable[[Character, Character], str]

    def use(self, caster: Character, target: Character) -> str:
        """Apply the effect when the caster can pay its mana cost."""
        if caster.mana < self.mana_cost:
            return f"Not enough mana to use {self.name.lower()}!"

        caster.change_mana(-self.mana_cost)
        return self.effect(caster, target)


@dataclass(frozen=True)
class School:
    name: str
    armor: int
    skills: tuple[Skill, ...]


@dataclass
class Character:
    race: Race
    school: School
    health: int = field(init=False)
    mana: int = field(init=False)

    def __post_init__(self) -> None:
        self.health = self.max_health
        self.mana = self.max_mana

    @property
    def max_health(self) -> int:
        return self.race.health

    @property
    def max_mana(self) -> int:
        return self.race.mana

    def change_health(self, amount: int) -> int:
        """Keep health within its limits and return the applied change."""
        previous_health = self.health
        self.health = max(0, min(self.max_health, self.health + amount))
        return self.health - previous_health

    def change_mana(self, amount: int) -> None:
        self.mana = max(0, min(self.max_mana, self.mana + amount))


class Player(Character):
    """The character controlled by the player."""


class Enemy(Character):
    """A computer-controlled opponent."""


def basic_attack(caster: Character, target: Character) -> str:
    attack_roll = caster.race.accuracy + random.randint(-2, 3)
    damage = caster.race.strength + random.randint(-2, 3)
    possessive, subject = (
        ("Your", "You") if isinstance(caster, Player) else ("Their", "They")
    )

    if attack_roll <= target.school.armor:
        return f"{possessive} attack missed!"

    target.change_health(-damage)
    return f"{possessive} attack hit! {subject} dealt {damage} damage!"


def heal(caster: Character, _target: Character) -> str:
    healed = caster.change_health(HEAL_AMOUNT)
    subject = "You" if isinstance(caster, Player) else "They"
    return f"{subject} healed {healed} health points!"


def lightning(caster: Character, target: Character) -> str:
    damage = LIGHTNING_DAMAGE + random.randint(-4, 5)
    target.change_health(-damage)
    subject = "You" if isinstance(caster, Player) else "They"
    return f"{subject} dealt {damage} lightning damage!"


# Immutable configuration is shared; health and mana belong to each character.
ELF = Race(name="Elf", health=60, accuracy=14, strength=6, mana=100)
DWARF = Race(name="Dwarf", health=70, accuracy=12, strength=10, mana=40)
ORC = Race(name="Orc", health=80, accuracy=10, strength=14, mana=0)

BASIC_ATTACK = Skill(name="Basic attack", mana_cost=0, effect=basic_attack)
WARRIOR_HEAL = Skill(name="Heal", mana_cost=20, effect=heal)
WIZARD_HEAL = Skill(name="Heal", mana_cost=10, effect=heal)
LIGHTNING = Skill(name="Lightning", mana_cost=30, effect=lightning)

TUSKRIDER = School(name="Tuskrider", armor=11, skills=(BASIC_ATTACK,))
WARRIOR = School(
    name="Warrior", armor=11, skills=(BASIC_ATTACK, WARRIOR_HEAL)
)
WIZARD = School(
    name="Wizard", armor=9, skills=(BASIC_ATTACK, WIZARD_HEAL, LIGHTNING)
)

RACES = {race.name: race for race in (ELF, DWARF)}
SCHOOLS = {school.name: school for school in (WARRIOR, WIZARD)}


def clear_screen() -> None:
    """Clear interactive terminals without starting a shell command."""
    if sys.stdout.isatty():
        print("\033[2J\033[H", end="", flush=True)


def display_text(message: str) -> None:
    """Animate text in terminals; print immediately for redirected output."""
    if not sys.stdout.isatty():
        print(message)
        return

    time.sleep(0.5)
    for character in message:
        print(character, end="", flush=True)
        time.sleep(0.01)
    print()


def show_message(message: str) -> None:
    clear_screen()
    print()
    display_text(message)
    display_text(SEPARATOR)


Option = TypeVar("Option")


def choose_option(
    prompt: str,
    options: Mapping[str, Option],
    describe: Callable[[Option], str],
) -> Option:
    """Select an available option by its number or name."""
    while True:
        clear_screen()
        for number, (name, option) in enumerate(options.items(), start=1):
            print(f"{number} - {name}\n{describe(option)}\n")

        choice = input(f"{prompt}\n > ").strip().casefold()
        for number, (name, option) in enumerate(options.items(), start=1):
            if choice in (str(number), name.casefold()):
                return option

        display_text("Invalid selection. Enter an available number or name.")


def describe_race(race: Race) -> str:
    return (
        f"  Health: {race.health}\n"
        f"  Accuracy: {race.accuracy}\n"
        f"  Strength: {race.strength}\n"
        f"  Mana: {race.mana}"
    )


def describe_school(school: School) -> str:
    skills = ", ".join(
        f"{skill.name} ({skill.mana_cost} mana)" for skill in school.skills
    )
    return f"  Armor: {school.armor}\n  Skills: {skills}"


def create_character() -> Player:
    race = choose_option("Select your race:", RACES, describe_race)
    school = choose_option("Select your school:", SCHOOLS, describe_school)
    return Player(race, school)


def show_fight_stats(player: Player, opponent: Enemy) -> None:
    clear_screen()
    print(f"Your health: {player.health}/{player.max_health}")
    print(f"Your mana: {player.mana}/{player.max_mana}\n")
    print(f"Opponent's health: {opponent.health}/{opponent.max_health}\n")


def select_skill(player: Player, opponent: Enemy) -> None:
    """Take one turn; insufficient mana still consumes the turn."""
    while True:
        show_fight_stats(player, opponent)
        skills = player.school.skills
        for number, skill in enumerate(skills, start=1):
            print(f"{number} - {skill.name} ({skill.mana_cost} mana)")

        choice = input("\nSelect a skill:\n > ").strip()
        available_skills = {
            str(number): skill
            for number, skill in enumerate(skills, start=1)
        }
        skill = available_skills.get(choice)
        if skill is None:
            display_text("Invalid selection. Enter an available skill number.")
            continue

        show_message(skill.use(player, opponent))
        return


def fight(player: Player, opponent: Enemy) -> None:
    show_message(
        f"PREPARE TO FIGHT!\n"
        f"An {opponent.race.name} {opponent.school.name} has appeared!"
    )

    while player.health > 0 and opponent.health > 0:
        select_skill(player, opponent)
        if opponent.health == 0:
            break

        show_message(BASIC_ATTACK.use(opponent, player))

    if player.health > 0:
        show_message("You win!")
    else:
        show_message("You were defeated.")


def main() -> None:
    player = create_character()
    opponent = Enemy(ORC, TUSKRIDER)
    fight(player, opponent)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nGame closed.")
