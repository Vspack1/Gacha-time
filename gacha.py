import random
import tkinter as tk
from tkinter import messagebox

# Define the items and their rarities
items = {
    "food": {"rarity": "common", "effect": "+10 HP"},
    "drink": {"rarity": "common", "effect": "+10 Mana"},
    "buff": {"rarity": "rare", "effect": "+20 HP"},
    "debuff": {"rarity": "rare", "effect": "+20 Mana"}
}

# Define the weapons and their rarities
weapons = {
    "dagger": {"rarity": "common", "effect": "deal phys dmg have 50% lifesteal"},
    "sword": {"rarity": "uncommon", "effect": "deal phys dmg and increase next atk"},
    "shield": {"rarity": "rare", "effect": "absorb dmg except true dmg"},
    "bow": {"rarity": "epic", "effect": "70% deal crit phys dmg"},
    "wand": {"rarity": "mythical", "effect": "deal magic dmg"},
    "medic staff": {"rarity": "legendary", "effect": "healing"}
}

# Define the pets and their rarities
pets = {
    "common": ["Pet1", "Pet2"],
    "uncommon": ["Pet3", "Pet4"],
    "rare": ["Pet5"],
    "epic": ["Pet6"],
    "mythical": ["Pet7"],
    "legendary": ["Pet8"]
}

# Define the probabilities for each rarity
probabilities = {
    "common": 0.5,
    "uncommon": 0.3,
    "rare": 0.1,
    "epic": 0.05,
    "mythical": 0.04,
    "legendary": 0.01
}

class Character:
    def __init__(self, name, health, attack, defense, magic_defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.magic_defense = magic_defense
        self.weapons = []
        self.items = []
        self.pet = None

    def add_weapon(self, weapon):
        if len(self.weapons) < 2:
            self.weapons.append(weapon)
        else:
            messagebox.showinfo("Info", "You can only carry 2 weapons.")

    def add_item(self, item):
        self.items.append(item)

    def add_pet(self, pet):
        self.pet = pet

    def show_stats(self):
        stats = f"{self.name} - Health: {self.health}, Attack: {self.attack}, Defense: {self.defense}, Magic Defense: {self.magic_defense}\n"
        for weapon in self.weapons:
            stats += f"Weapon: {weapon}, Effect: {weapons[weapon]['effect']}\n"
        for item in self.items:
            stats += f"Item: {item}, Effect: {items[item]['effect']}\n"
        if self.pet:
            stats += f"Pet: {self.pet}\n"
        return stats

def pull_item():
    rarity = random.choices(list(probabilities.keys()), list(probabilities.values()))[0]
    item = random.choice(list(items.keys()))
    return rarity, item

def pull_weapon():
    rarity = random.choices(list(probabilities.keys()), list(probabilities.values()))[0]
    weapon = random.choice(list(weapons.keys()))
    return rarity, weapon

def pull_pet():
    rarity = random.choices(list(probabilities.keys()), list(probabilities.values()))[0]
    pet = random.choice(pets[rarity])
    return rarity, pet

def update_stats(player, enemy, player_label, enemy_label):
    player_label.config(text=player.show_stats())
    enemy_label.config(text=enemy.show_stats())

def battle(player, enemy, player_label, enemy_label, result_label, play_again_button, quit_button):
    result_label.config(text="Battle Start! Player vs Boss")
    root.update()
    while player.health > 0 and enemy.health > 0:
        root.after(2000)
        player_attack = max(0, player.attack - enemy.defense)
        enemy.health -= player_attack
        result_label.config(text=f"Player attacks Boss for {player_attack} damage. Boss health: {enemy.health}")
        update_stats(player, enemy, player_label, enemy_label)
        root.update()

        if enemy.health <= 0:
            result_label.config(text="Boss is defeated! You win!")
            play_again_button.pack()
            quit_button.pack()
            return

        root.after(2000)
        enemy_attack = max(0, enemy.attack - player.defense)
        player.health -= enemy_attack
        result_label.config(text=f"Boss attacks Player for {enemy_attack} damage. Player health: {player.health}")
        update_stats(player, enemy, player_label, enemy_label)
        root.update()

        if player.health <= 0:
            result_label.config(text="You lose and lost everything, try again.")
            play_again_button.pack()
            quit_button.pack()
            return

def choose_weapon(player):
    sorted_weapons = sorted(weapons.items(), key=lambda x: probabilities[x[1]['rarity']], reverse=True)
    weapon_choices = tk.Toplevel(root)
    weapon_choices.title("Choose Weapons")
    tk.Label(weapon_choices, text="Choose your weapons:").pack()
    for i, (weapon, details) in enumerate(sorted_weapons):
        tk.Button(weapon_choices, text=f"{weapon} (Rarity: {details['rarity']}, Effect: {details['effect']})",
                  command=lambda w=weapon: [player.add_weapon(w), weapon_choices.destroy(), choose_food(player)]).pack()

def choose_food(player):
    sorted_items = sorted([(item, details) for item, details in items.items() if "food" in item], key=lambda x: probabilities[x[1]['rarity']], reverse=True)
    food_choices = tk.Toplevel(root)
    food_choices.title("Choose Food")
    tk.Label(food_choices, text="Choose your food:").pack()
    for i, (item, details) in enumerate(sorted_items):
        tk.Button(food_choices, text=f"{item} (Rarity: {details['rarity']}, Effect: {details['effect']})",
                  command=lambda it=item: [player.add_item(it), food_choices.destroy(), choose_drink(player)]).pack()

def choose_drink(player):
    sorted_items = sorted([(item, details) for item, details in items.items() if "drink" in item], key=lambda x: probabilities[x[1]['rarity']], reverse=True)
    drink_choices = tk.Toplevel(root)
    drink_choices.title("Choose Drink")
    tk.Label(drink_choices, text="Choose your drink:").pack()
    for i, (item, details) in enumerate(sorted_items):
        tk.Button(drink_choices, text=f"{item} (Rarity: {details['rarity']}, Effect: {details['effect']})",
                  command=lambda it=item: [player.add_item(it), drink_choices.destroy(), choose_pet(player)]).pack()

def choose_pet(player):
    sorted_pets = sorted([(pet, rarity) for rarity, pets_list in pets.items() for pet in pets_list], key=lambda x: probabilities[x[1]], reverse=True)
    pet_choices = tk.Toplevel(root)
    pet_choices.title("Choose Pet")
    tk.Label(pet_choices, text="Choose your pet:").pack()
    for i, (pet, rarity) in enumerate(sorted_pets):
        tk.Button(pet_choices, text=f"{pet} (Rarity: {rarity})",
                  command=lambda p=pet: [player.add_pet(p), pet_choices.destroy(), start_battle()]).pack()

def start_battle():
    player.show_stats()
    enemy.show_stats()
    update_stats(player, enemy, player_label, enemy_label)
    battle(player, enemy, player_label, enemy_label, result_label, play_again_button, quit_button)

def start_game():
    global player, enemy
    player = Character("Player", 100, 20, 10, 5)
    enemy = Character("Boss", 150, 15, 5, 5)

    try:
        pulls = int(pulls_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number of pulls.")
        return

    for _ in range(pulls):
        rarity, item = pull_item()
        messagebox.showinfo("Item Pulled", f"You pulled a {rarity} item: {item}")

    for _ in range(2):
        rarity, weapon = pull_weapon()
        messagebox.showinfo("Weapon Pulled", f"You pulled a {rarity} weapon: {weapon}")

    rarity, pet = pull_pet()
    messagebox.showinfo("Pet Pulled", f"You pulled a {rarity} pet: {pet}")

    choose_weapon(player)

def play_again():
    play_again_button.pack_forget()
    quit_button.pack_forget()
    start_game()

def quit_game():
    root.destroy()

root = tk.Tk()
root.title("Gacha Game")

player_label = tk.Label(root, text="")
player_label.pack()

enemy_label = tk.Label(root, text="")
enemy_label.pack()

result_label = tk.Label(root, text="")
result_label.pack()

pulls_label = tk.Label(root, text="How many pulls would you like to make?")
pulls_label.pack()

pulls_entry = tk.Entry(root)
pulls_entry.pack()

start_button = tk.Button(root, text="Start Game", command=start_game)
start_button.pack()

play_again_button = tk.Button(root, text="Play Again", command=play_again)
quit_button = tk.Button(root, text="Quit Game", command=quit_game)

quit_button.pack()

root.mainloop()