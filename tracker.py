import random

class Combatant:

    def __init__(self, name, hp, init_mod):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.init_mod = init_mod # initiative modifer
        self.init = 0 # set default initiative to zero

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
                  
class Player(Combatant):
    pass

class Enemy(Combatant):
    pass

class Ally(Combatant):
    def __init__(self, name, hp, init_mod, owner):
        super().__init__(name, hp, init_mod)
        self.owner = owner

class Encounter:
    def __init__(self):
        self.combatant_list = []
        self.active_combatant 
        self.round_number = 0

    def add_combatant(combatant):
        combatant_list += combatant


