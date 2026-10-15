import random
import sqlite3
from pathlib import Path

class Combatant:
    def __init__(self, name, hp, init_mod, type):
        self.name = name.strip()
        self.max_hp = hp
        self.hp = hp
        self.init_mod = init_mod # initiative modifer
        self.init = 0 # set default initiative to zero
        self.type = type

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
        if init <= 0:
            init = 1
        self.init = init
        return init
    
    def change_name(self, name):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        
        if not name.strip():
            raise ValueError("Name cannnot be empty")
        
        self.name = name.strip()

    def __str__(self):
        return f"{self.name} ({self.hp}/{self.max_hp}) HP, ({self.init})"

    def __lt__(self, other):
        return self.init > other.init

class Encounter:
    def __init__(self):
        self.combatant_list = []
        self.active_combatant_index = 0
        self.round_number = 0


    def add_combatant(self, combatant):
        self.combatant_list.append(combatant)

    def remove_combatant(self, combatant):
        for i in range(len(self.combatant_list)):
            if self.combatant_list[i] == combatant:
                del self.combatant_list[i]

    def sort_list(self):
        self.combatant_list.sort() # Later add way to check if creature health is 0 and don't sort them

    def print_turn_order(self):
        for mem in self.combatant_list:
            print(mem)

    def roll_all_initiative(self):
        for mem in self.combatant_list:
            mem.roll_init()

    def advance_turn(self):
        self.active_combatant_index += 1

class Database:
    def __init__(self, db_name="tracker.db"):
        self.db_name = db_name

    def check(self):
        return Path(self.db_name).exists()

    def connect(self):
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def create_tables(self):
        with self.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS encounters (
                    id INTEGER PRIMARY KEY,
                    round_number INTEGER NOT NULL DEFAULT 0,
                    active_index INTEGER
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS combatants (
                    id INTEGER PRIMARY KEY,
                    encounter_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    max_hp INTEGER NOT NULL,
                    hp INTEGER NOT NULL,
                    init_mod INTEGER NOT NULL,
                    init INTEGER NOT NULL,
                    type TEXT NOT NULL,

                    FOREIGN KEY (encounter_id)
                        REFERENCES encounters(id)
                        ON DELETE CASCADE
                )    
            """)

            conn.execute("""
                INSERT OR IGNORE INTO encounters (id, round_number)
                VALUES (1, 0)
            """)

    def save_encounter(self, encounter):
        with self.connect() as conn:
            conn.execute("PRAGMA foreign_keys = ON")

            conn.execute("""
                UPDATE encounters
                SET round_number = ?, active_index = ?
                WHERE id = 1
            """, (encounter.round_number, encounter.active_combatant_index))

            conn.execute("""
                DELETE FROM combatants
                WHERE encounter_id = 1
            """)

            for combatant in encounter.combatant_list:
                conn.execute("""
                    INSERT INTO combatants (
                        encounter_id,
                        name,
                        max_hp,
                        hp,
                        init_mod,
                        init,
                        type    
                    )
                    VALUES (1, ?, ?, ?, ?, ?, ?)
                """, (combatant.name, combatant.max_hp, combatant.hp, combatant.init_mod, combatant.init, combatant.type))

    def load_encounter(self):
        with self.connect() as conn:
            conn.row_factory = sqlite3.Row

            encounter_row = conn.execute("""
                SELECT round_number, active_index
                FROM encounters
                WHERE id = 1
            """).fetchone()

            if encounter_row is None:
                return None

            encounter = Encounter()
            encounter.round_number = encounter_row["round_number"]

            rows = conn.execute("""
                SELECT name, max_hp, hp, init_mod, init, type
                FROM combatants
                WHERE encounter_id = 1
                ORDER BY id
            """).fetchall()

            for row in rows:
                combatant = Combatant(
                    row["name"],
                    row["max_hp"],
                    row["init_mod"],
                    row["type"]
                )

                combatant.hp = row["hp"]
                combatant.init = row["init"]

                encounter.add_combatant(combatant)

            active_index = encounter_row["active_index"]

            if active_index is not None:
                if 0 <= active_index < len(encounter.combatant_list):
                    encounter.active_combatant_index = active_index

            return encounter
