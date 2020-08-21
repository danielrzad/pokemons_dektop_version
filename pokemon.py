from collections import namedtuple
from dataclasses import make_dataclass


class Pokemon:
    # List of available pokemons and their types
    PokemonAttributes = make_dataclass(
        "PokemonAttributes", ["type", "level", "cost"]
    )
    available_pokemons = {
        "Bulbasaur": PokemonAttributes(
            type="Grass", level=10, cost=15
        ),
        "Charmander": PokemonAttributes(
            type="Fire", level=10, cost=15
        ),
        "Squirtle": PokemonAttributes(
            type="Water", level=10, cost=15
        ),
        "Butterfree": PokemonAttributes(
            type="Bug", level=10, cost=15
        ),
        "Pidgey": PokemonAttributes(
            type="Flying", level=10, cost=15
        ),
        "Rattata": PokemonAttributes(
            type="Normal", level=10, cost=15
        ),
        "Ekans": PokemonAttributes(
            type="Poison", level=10, cost=15
        ),
        "Pikachu": PokemonAttributes(
            type="Electric", level=10, cost=15
        ),
        "Jigglypuff": PokemonAttributes(
            type="Fairy", level=10, cost=15
        ),
        "Diglett": PokemonAttributes(
            type="Ground", level=10, cost=15
        ),
    }
    # List of types conters when attacking other type
    counters = {
            "Fire": {
                ("Grass", "Bug"): 2,
                ("Fire", "Grass", "Poison", "Flying", "Bug"): 0.5,
            },
            "Grass": {
                ("Water", "Ground"): 2,
                ("Fire", "Grass", "Poison", "Flying", "Bug"): 0.5,
            },
            "Water": {
                ("Fire", "Ground"): 2,
                ("Water", "Grass"): 0.5,
            },
            "Bug": {
                ("Grass", "Ground"): 2,
                ("Fire", "Poison", "Flying", "Fairy"): 0.5,
            },
            "Flying": {
                ("Grass", "Bug"): 2,
                ("Electric"): 0.5,
            },
            "Poison": {
                ("Grass", "Fairy"): 2,
                ("Poison", "Ground"): 0.5,
            },
            "Electric": {
                ("Water", "Flying"): 2,
                ("Electric", "Grass"): 0.5,
            },
            "Fairy": {
                ("Fire"): 0.5,
            },
            "Ground": {
                ("Fire", "Electric", "Poison", ): 2,
                ("Grass", "Bug"): 0.5,
            },
    }    
    """Pocemon base class"""
    def __init__(
        self, 
        name,
    ):
        self.name = name
        self.level = self.available_pokemons[self.name].level
        self.p_type = self.available_pokemons[self.name].type
        self.max_health = self.level * 5
        self.current_health = self.max_health
        self.ko_status = False
        self.experience = 0
    
    def lose_health(self, amount):
        print(f"Ouchh I've lost {amount} health points.")
        print(f"{self.name} now has {self.current_health} health.")
        self.current_health -= amount

    def regenerate_health(self, amount):
        print(f"Mmmm I'm regenerating {amount} health points.")
        print(f"{self.name} now has {self.current_health} health.")
        self.current_health += amount

    def is_knocked_out(self):
        self.ko_status = self.current_health <= 0
        if self.ko_status == True:
            print(f"Oh fuck I'm knocked out. Upss")

    def revival(self):
        print(f"Thanks for reviving me. I fell much better now")
        self.ko_status = False

    def attack(self, target):
        damage = self.level * 2
        if self.p_type in counters.keys():
            if self.target.p_type in counters[self.p_type].keys():
                for key, val in counters[self.p_type].items():
                    if self.target.p_type in key:
                        damage *= val
        if damage > target.current_health:
            target.current_health = 0
        else:
            target.current_health -= damage
        print(
            f"==========================================\n"
            f"{self.name} is dealing {damage} damage to {target.name}.\n"
            f"==========================================\n"
            f"{self.name} current health is {self.current_health}\n"
            f"==========================================\n"
            f"{target.name} current health is {target.current_health}\n"
            f"==========================================\n"
        )
        target.is_knocked_out()
        self.experience += 10
        self.level_up_check()

    def check_experience(self):
        print("EXP BAR")
        print("== " * int((self.experience / 10)))
        print("== == == == == == == == == ==")
        print(
            f"{self.name} got {self.experience}% experience towards "
            f"{self.level + 1}."
        )

    def level_up_check(self):
        if self.experience == 100:
            self.level += 1
            print(f"{self.name} reached {self.level} level.")

    def __repr__(self):
        return (
            f"Pokemon({self.name!r}, {self.level!r}, {self.p_type!r}, "
            f"{self.current_health!r}, {self.ko_status!r})"
        )

    def __str__(self):
        return f"I'm {self.name} a Pokemon of a {self.p_type} type."
