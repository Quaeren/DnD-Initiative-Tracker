import sqlite3

DB_NAME = "tracker.db"

def create_database():
    with sqlite3.connect(DB_NAME) as conn: 
        conn.execute("""
            CREATE TABLE IF NOT EXISTS encouters (
                id INTERGER PRIMARY KEY,
                round_number INTERGER NOT NULL DEFAULT 1,
                active_index INTERGER
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS combatants (
                id INTERGER PRIMARY KEY,
                encounter_id INTERGER NOT NULL,
                position INTERGER NOT NULL,
                name TEXT NOT NULL,
                max_hp INTERGER NOT NULL,
                hp INTERGER NOT NULL,
                init_mod INTERGER NOT NULL,
                init INTERGER NOT NULL,
                type TEXT NOT NULL

                FOREIGN KEY (encounter_id)
                    REFERENCES encounters(id)
                    ON DELETE CASCADE
            )    
        """)

        conn.execute("""
            INSERT OR IGNORE INTO encounters (id, round_number)
            VALUES (1, 0)
        """)

def save_database(encounter):
    with sqlite3.connect(DB_NAME) as conn:
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
                position,
                name,
                max_hp,
                hp,
                init_mod,
                init,
                type    
            )
            VALUES (1, ?, ?, ?, ?, ?, ?, ?)
        """, (encounter.combatant_list.index(combatant), combatant.name, combatant.max_hp, combatant.hp, combatant.init_mod, combatant.init, combatant.type))