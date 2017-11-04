import random

from classes.game import Person, bcolors
from classes.inventory import Item
from classes.magic import Spell


# Create black magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 350, "black")


# Create white magic
cure = Spell("Cure", 12, 620, "white")
cura = Spell("Cura", 18, 1500, "white")


# Create some items
potion = Item("Potion", "potion", "Heals 50 HP", 200)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 500)
superpotion = Item("Super-Potion", "potion", "Heals 500 HP", 1000)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999)
megaelixir = Item("MegaElixir", "elixir", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)


player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, cure]
player_items = [{"item": potion, "quantity": 15},{"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 3}, {"item": elixir, "quantity": 4},
                {"item": megaelixir, "quantity": 1}, {"item": grenade, "quantity": 2}]


# Instatiate People
player1 = Person("Ilias", 3850, 132, 300, player_spells, player_items)
player2 = Person("Billy", 4100, 188, 311, player_spells, player_items)
player3 = Person("Napo ", 3090, 174, 288, player_spells, player_items)

enemy1 = Person("Bored ", 1250, 130, 560, enemy_spells, [])
enemy2 = Person("Ptyxio", 11500, 700, 525, enemy_spells, [])
enemy3 = Person("Procr ", 1250, 130, 560, enemy_spells, [])


players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

defeated_enemies = 0
defeated_players = 0

running = True

print(35*"=")
print(bcolors.FAIL + bcolors.BOLD + "BATTLE IS INITIATED! THE END IS NEAR!" + bcolors.ENDC)
while running:
    print(35*"=")
    print("\n")
    print(bcolors.BOLD + "NAME:" + 16*" " + "HP" + 37*" " + "MP" + bcolors.ENDC)
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        if defeated_enemies == 3:
            print(bcolors.BOLD + bcolors.OKGREEN + "YOU WIN!" + bcolors.ENDC)
            running = False
            break
        player.choose_action()
        choice = int(input("    Choose action: ")) -1

        if choice == 0:
            dmg = player.generate_damage()
            enemy_target = player.choose_target(enemies)
            enemies[enemy_target].take_damage(dmg)
            print("\n", player.name.replace(" ", ""), "attacked", enemies[enemy_target].name.replace(" ", ""),
                  "for", dmg, "points of damage.")
            if enemies[enemy_target].get_hp()==0:
                defeated_enemies += 1
                print(bcolors.BOLD + "\n", enemies[enemy_target].name.replace(" ", ""),
                      "has been defeated!" + bcolors.ENDC)
                del enemies[enemy_target]
        elif choice == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic: ")) -1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            # Sometimes here occurs the following error:
            # magic_dmg = spell.generate_damage()
            #    AttributeError: 'NoneType' object has no attribute 'generate_damage'
            # Haven't figured out why spell is 'NoneType' some of the times it runs

            current_mp = player.get_mp()
            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for " + str(magic_dmg) + " HP" + bcolors.ENDC)
            elif spell.type == "black":
                enemy_target = player.choose_target(enemies)
                enemies[enemy_target].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg),
                      "points of damage to", enemies[enemy_target].name.replace(" ", "") + bcolors.ENDC)
                if enemies[enemy_target].get_hp() == 0:
                    defeated_enemies += 1
                    print(bcolors.BOLD + "\n", enemies[enemy_target].name.replace(" ", ""),
                          "has been defeated!" + bcolors.ENDC)
                    del enemies[enemy_target]
        elif choice == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) -1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop) + " HP" + bcolors.ENDC)
            elif item.type == "elixir":
                if item.name =="MegaElixir":
                    for i in players:
                        i.hp = i.max_hp
                        i.mp = i.max_mp
                        print(bcolors.OKGREEN + "\n" + item.name
                              + " fully restores HP/MP for all players!" + bcolors.ENDC)
                else:
                    player.hp = player.max_hp
                    player.mp = player.max_mp
                    print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP!" + bcolors.ENDC)
            elif item.type == "attack":
                enemy_target = player.choose_target(enemies)
                enemies[enemy_target].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop),
                      "points of damage to", enemies[enemy_target].name.replace(" ", "") + bcolors.ENDC)
                if enemies[enemy_target].get_hp() == 0:
                    defeated_enemies += 1
                    print(enemies[enemy_target].name.replace(" ", ""), "has been defeated!")
                    del enemies[enemy_target]

    print(35 * "=")
    # Enemy attack phase
    for enemy in enemies:
        # Check if Enemies won
        if defeated_players == 3:
            print(bcolors.BOLD + bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
            running = False
            break
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            # Enemy chose Attack
            target = random.randrange(0, len(players))
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print("\n", enemy.name.replace(" ", ""), "attacked",
                  players[target].name.replace(" ", ""),
                  "for", enemy_dmg, "points of damage.")
            if players[target].get_hp() == 0:
                defeated_players += 1
                print(bcolors.BOLD + "\n", players[target].name.replace(" ", ""), "has been defeated!" + bcolors.ENDC)
                del players[target]
        elif enemy_choice == 1:
            # Enemy chose to use magic
            #spell, magic_dmg = enemy.choose_enemy_spell()
            spell = enemy.choose_enemy_spell()
            #print(type(spell))
            magic_dmg = spell.generate_damage()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals " + enemy.name.replace(" ", "")
                      + " for " + str(magic_dmg) + " HP" + bcolors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, len(enemies))
                players[target].take_damage(magic_dmg)
                print("\n", enemy.name.replace(" ", "") + "'s", spell.name, "deals",magic_dmg,
                      "points of damage to",  players[target].name.replace(" ", "") + "!")
                if players[target].get_hp() == 0:
                    defeated_players += 1
                    print(bcolors.BOLD + "\n", players[target].name.replace(" ", ""), "has been defeated!" + bcolors.ENDC)
                    del players[target]

#running = False
