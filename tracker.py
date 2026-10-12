import random
from database import create_database


class Combatant:
    counter = 0

    def __init__(self, name, hp, init_mod, type):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.init_mod = init_mod # initiative modifer
        self.init = 0 # set default initiative to zero
        self.type = type
        self.encounter_id = Encounter.counter + 1

        if Combatant.counter == 0:
            self.id = 1
        else: 
            self.id = Combatant.counter + 1

        counter += 1

    def damage(self, value: int) -> None:
        if value <= 0:
            raise ValueError("Only positive numbers above zero accepted")
        else:
            if (self.hp - value) < 0:
                self.hp = 0
            else:
                self.hp -= value
            #print(f"{value} damage done to {self.name}. Current HP: {self.hp}")

    def heal(self, value:int) -> None:
        if value <= 0:
            raise ValueError("Only positive number above zero accepted")
        else:
            if (self.hp + value) > self.max_hp:
                self.hp = self.max_hp
            else:
                self.hp += value
            #print(f"{value} damage healed for {self.name}. Current HP: {self.hp}")
        
    def set_init(self, value:int) -> None:
        if value > 0 and value < 26:
            self.init = value
        else:
            raise ValueError("Value has to be between 1 and 25")
        
    def set_init_mod(self, value:int) -> None:
        if value >= -5 and value <= 5:
            self.init_mod = value
        else:
            raise ValueError("Value has to be between -5 and 5")
        
    def roll_init(self) -> int:
        init = random.randint(1,20) + self.init_mod
        self.init = init
        return init
    
    def change_name(self, name):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        
        if not name.strip():
            raise ValueError("Name cannnot be empty")
        
        self.name = name

    def __str__(self):
        return f"{self.name} ({self.hp}/{self.max_hp}) HP, ({self.init})"

    def __lt__(self, other):
        return self.init < other.init

class Encounter:
    counter = 0
    
    def __init__(self):
        self.combatant_list = []
        self.active_combatant_index = 0
        self.round_number = 0

        if Encounter.counter == 0:
            self.id = 1
        else:
            self.id = Encounter.counter + 1

        counter += 1

    def add_combatant(self, combatant):
        self.combatant_list += combatant

    def remove_combatant(self, combatant):
        for i in range(len(self.combatant_list)):
            if self.combatant_list[i] == combatant:
                del self.combatant_list[i]

    def sort_list(self):
        self.combatant_list.sort() # Later add way to check if creature health is 0 and don't sort them

    def print_turn_order(self):
        for mem in self.combatant_list:
            print(mem)



create_database()