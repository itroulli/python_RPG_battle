import random


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, atk, magic, items):
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.atkh = atk + 10
        self.atkl = atk - 10
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]
        self.name = name

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.max_mp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i=1
        print("\n" + "    " + bcolors.BOLD + self.name + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD + "    ACTIONS:" + bcolors.ENDC)
        for action in self.actions:
            print("        " + str(i) + ".", action)
            i += 1

    def choose_magic(self):
        i=1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "    MAGIC:" + bcolors.ENDC)
        for spell in self.magic:
            print("        " + str(i) + ".", spell.name, "(cost:", str(spell.cost) +")")
            i += 1

    def choose_item(self):
        i=1
        print("\n" + bcolors.OKGREEN + bcolors.BOLD + "    ITEMS:" + bcolors.ENDC)
        for item in self.items:
            print("        " + str(i) + ".", item["item"].name, ":", item["item"].description, "(x" + str(item["quantity"]) + ")")
            i += 1

    def choose_target(self,enemies):
        print("\n" + bcolors.FAIL + bcolors.BOLD + "    TARGET:" + bcolors.ENDC)
        for i, enemy in enumerate(enemies):
            if enemy.get_hp() != 0:
                print("        " + str(i+1) + ".", enemy.name)
        choice = int(input("    Choose Target:")) -1
        return choice



    def get_enemy_stats(self):
        hp_bar = ""
        hp_cells = (self.hp / self.max_hp) * 100 / 2

        while hp_cells > 0:
            hp_bar += "█"
            hp_cells -= 1

        while len(hp_bar) < 50:
            hp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.max_hp)
        if len(hp_string) < 11:
            chp = (11 - len(hp_string)) * " " + hp_string
        else:
            chp = hp_string

        print("                     __________________________________________________ ")
        print(bcolors.BOLD + self.name + ":  " + chp + "|" + bcolors.FAIL
              + hp_bar + bcolors.ENDC + "|")


    def get_stats(self):

        hp_bar = ""
        hp_cells = (self.hp/self.max_hp) * 100 / 4

        mp_bar = ""
        mp_cells = (self.mp/self.max_mp) * 100 / 10

        while hp_cells > 0:
            hp_bar += "█"
            hp_cells -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        while mp_cells > 0:
            mp_bar += "█"
            mp_cells -= 1

        while len(mp_bar) < 10:
            mp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.max_hp)
        if len(hp_string) < 9:
            chp = (9 - len(hp_string))*" " + hp_string
        else:
            chp = hp_string

        mp_string = str(self.mp) + "/" + str(self.max_mp)
        if len(mp_string) < 7:
            cmp = (7 - len(mp_string))*" " + mp_string
        else:
            cmp = mp_string

        print("                     _________________________               __________ ")
        print(bcolors.BOLD + self.name +":     " + chp  +  "|" + bcolors.OKGREEN
              + hp_bar + bcolors.ENDC + bcolors.BOLD + "|      " + cmp
              + "|" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + "|")

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        #print(type(spell))
        #magic_dmg = spell.generate_damage()
        pct = (self.hp / self.max_hp) * 100
        # The following if statement can lead to an infinite loop
        # I have to fix it
        if self.mp < spell.cost or spell.type == "white" and pct>50:
            return self.choose_enemy_spell()
        else:
            return spell
            #return spell, magic_dmg
