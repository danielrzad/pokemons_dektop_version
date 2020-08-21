from pprint import pprint
from random import random


import pokemon
import pokemon_game


class Trainer:
    """Trainer initialization"""
    def __init__(self):
        self.name = input("Please enter Your Trainer name: ")
        self.points = pokemon_game.game_config.starting_points
        self.owned_pokemons = self.choose_pokemons()
        self.currently_active_pokemon = self.set_active_pokemon()
        self.available_potions = self.choose_potions()
        self.available_pokeballs = self.choose_pokeballs()

    ### Methods for object creation###
    def choose_pokemons(self):
        print(
            f"{self.name.capitalize()} now You need to choose Yours Pokemons." 
            f"Each Pokemon cost some points. You can use up to {self.points} "
            f"points. Remember to leave some for health potions and pokeballs"
            f". You can choose Pokemons from:"
        )
        available_pokemons = pokemon.Pokemon.available_pokemons
        pokemon_costs = []
        for key, val in available_pokemons.items():
            print(
                f"{key} Pokemon of type: {val.type}, level: {val.level}, "
                f"cost: {val.cost}."
            )
            pokemon_costs.append(val.cost)
        choosen_pokemons = []
        while self.points >= sorted(pokemon_costs)[0]:
            chooice = input(
                f"Please enter Pokemon name which You want to choice. "
                f"If You dont want to choose more Pokemons hit 'Enter' "
                f"key. Points left: {self.points}.\n"
            )
            if chooice in available_pokemons.keys():
                choosen_pokemons.append(chooice)
                self.points -= available_pokemons[chooice].cost
                continue
            elif chooice == "" and len(choosen_pokemons) > 0:
                return self.create_pokemons(choosen_pokemons)
            else:
                print(
                    "Please use valid Pokemons names. You need to choose at "
                    "least one Pokemon.\n"
                )
        return self.create_pokemons(choosen_pokemons)


    def create_pokemons(self, choosen_pokemons):
        print(choosen_pokemons)
        return [pokemon.Pokemon(name=name) for name in choosen_pokemons]


    def set_active_pokemon(self):
        print(self.owned_pokemons)
        choose = input("Please choose Pokemon which do You want to be active.")
        if choose in self.get_pokemon_names():
            return choose
        print("You can choose only from Pokemons in Your possesion.")
        return self.set_active_pokemon()


    def get_pokemon_names(self):
        names = []
        for pokemon in self.owned_pokemons:
            names.append(pokemon.name)
        return names


    def choose_potions(self):
        potion_cost = pokemon_game.game_config.potion_cost
        if self.points >= potion_cost:
            print(
                f"Now it's time to choose how many potions do You want to "
                f"take into the fight. You have {self.points} points left. " 
                f"Each potion costs {potion_cost} points. If you don't want "
                f"any potions enter 0."
            )
            potions_number = int_input_check()
            if potions_number * potion_cost <= self.points:
                self.available_potions = potions_number
                print(
                    f"Now You have {potions_number} potions in Yours invetory."
                )
                return potions_number
            print("You don't have enough points to take that many potions.")
            return self.choose_potions()
        else:
            print(
                "Unfortunately you didn't leave any points for health "
                "potions. You won't be able to heal Yours Pokemons during the "
                "fight."
            )


    def choose_pokeballs(self):
        pokeball_cost = pokemon_game.game_config.pokeball_cost
        if self.points >= pokeball_cost:
            print(
                f"Now it's time to choose how many Pokeballs do You want to "
                f"take into the fight. You have {self.points} points left. " 
                f"Each Pokeball costs {pokeball_cost} points. If you don't "
                f"want any Pokeballs enter 0."
            )
            pokeball_number = int_input_check()
            if pokeball_number * pokeball_cost <= self.points:
                self.available_pokeballs = pokeball_number
                print(
                    f"Now You have {pokeball_number} potions in Yours invetory."
                )
                return pokeball_number
            print("You don't have enough points to take that many Pokeballs.")
            return self.choose_potions()
        else:
            print(
                "Unfortunately you didn't leave any points for Pokeballs."
                "You won't be able to catch you opponent Pokemons during the "
                "fight."
            )

    ### End of methods for object creation ###
    
    ### Start of action methods ###
    def ko_check(self):
        if self.currently_active_pokemon.ko_status == False:
            return True
        elif self.currently_active_pokemon.ko_status:
            print(
                f"Sorry {self.currently_active_pokemon.name} has been knocked "
                f"out and He's unable to fight. You need to switch it to "
                f"another one or heal it using health potion."
            )
            if self.available_potions > 0:
                print("Do You want to heal You Pokemon?")
                asnwer = input("Please enter 'Yes' or 'No'.:")
                while asnwer != "Yes" or asnwer != "No":
                    asnwer
                if asnwer == "Yes":
                    self.heal_pokemon()
                elif asnwer == "No":
                    print(
                        f"So if You don't like to heal "
                        f"{currently_active_pokemon.name} You need to switch "
                        f"him to another Pokemon"
                    )
            self.switch_pokemon()


    def attack(self, target):
        if self.ko_check():
            self.currently_active_pokemon.attack(
                target.currently_active_pokemon
            )           


    def catch(self, target):
        if self.ko_check():
            target_pokemon = target.currently_active_pokemon
            target_current_hp = target_pokemon.current_health
            target_max_hp = target_pokemon.max_health
            print(
                f"{self.name} trying to catch {target.name}'s "
                f"{target_pokemon.name} using one Pokeball!"
            )
            catch_chance = round(target_current_hp / target_max_hp, 2)
            defense_chance = round(1 - catch_chance, 2)
            if np.random.choice(
                ['True', 'False'], 1, False, p=[catch_chance, defense_chance]
            ) == ['True']:
                self.owned_pokemons.append(target_pokemon)
                target.owned_pokemons.remove(target_pokemon)


    def heal_pokemon(self):
        if self.available_potions >= 1:
            self.available_potions -= 1
            name = self.currently_active_pokemon.name
            max_health = self.currently_active_pokemon.max_health
            current_health = self.currently_active_pokemon.current_health
            health_restored = max_health - current_health
            print(
                f"{name} healed.\n"
                f"Health restored - {health_restored}.\n"
                f"{name} current health is {max_health}."
            )
            self.currently_active_pokemon.current_health = self.currently_active_pokemon.max_health
            return True
        else:
            print("Sorry You don't have enough potions to use")
            return False


    def switch_pokemon(self, choice):
        choices = []
        for pokemon in self.owned_pokemons:
            if not pokemon.ko_status:
            # if pokemon.ko_status == False:
                choices.append(pokemon.name)
        print(choices)
        choice = input(
            "Please choose one Pokemon from ones listed above. Enter Pokemon "
            "name.:")
        while choice not in choices:
            choice
        if choice in self.owned_pokemons:
            if not choice.ko_status:                    
                self.currently_active_pokemon = choice
                print(f"Currently active pokemon switched to {choice.name}.")
            else:
                print(
                    f"Sorry. {choice.name} has been knocked out and he's "
                    f"unable to fight."
                )
        else:
            print(f"Sorry You don't have {choice.name} in your possesion")


    def __repr__(self):
        return (
            f"Trainer(name={self.name!r}, "
            f"currently_active_pokemon={self.currently_active_pokemon!r}, "
            f"owned_pokemons={self.owned_pokemons!r}, "
            f"available_potions={self.available_potions!r})"
        )


    def __str__(self):
        return f"Hey I'm {self.name}. Nice to meet You."


def int_input_check():
    number = input("Please enter an integer only. : ")
    if number.isdigit():
        number = int(number) 
        return number
    print("You didn't enter an integer.")
    return int_input_check()

