import questionary
from tracker import Database, Encounter, Combatant
import subprocess
import os


def clear_screen():
    subprocess.run(
        ["cmd", "/c", "cls"] if os.name == "nt" else ["clear"], check=False)

def sub_menu_questions():
    clear_screen()

    return questionary.select(
        "Please choose an action to do:",
        choices=[
            "Add combatant",
            "Remove combatant",
            "View turn order",
            "Roll initiative",
            "Start encounter",
            "Save encounter",
            "Exit"
        ], qmark="", instruction="").ask() or "do nothing"

def choice_menu(choice, encounter):
        clear_screen()
        
        match choice:
            case "Add combatant":
                name = questionary.text("Name: ", qmark="", instruction="").ask()
                health = int(questionary.text("Health: ", qmark="", instruction="").ask())
                init_mod = int(questionary.text("Initiative modifier: ", qmark="", instruction="").ask())
                type = questionary.select(
                    "Select combatant tupe: ",
                    choices=["player", "enemy", "ally"], qmark="", instruction="").ask()

                encounter.add_combatant(Combatant(name, health, init_mod, type))
                print(f"Combatant: {name} added succesfully")
                return None
            case "Remove combatant":
                name = questionary.text("Name of combatant you would like to remove: ", qmark="", instruction="").ask()
                encounter.remove_combatant(name)
                print(f"Succesfully removed {name}")
                return None
            case "View turn order":
                encounter.sort_list()
                encounter.print_turn_order()
                return None
            case "Roll initiative":
                encounter.roll_all_initiative()
                return None
            case "Start encounter":
                return "Start"
            case "Save encounter":
                return "Save"
            case "Exit":
                return "Exit"

def active_encounter(encounter):
    while True:
        clear_screen()
        choices = []

        for i, combatant in enumerate(encounter.combatant_list):
            name = f"▶ {combatant}" if i == encounter.active_combatant_index else f"  {combatant}"

            choices.append(questionary.Choice(
                title=name,
                value=combatant
            ))
        choices.append("  End Turn")
        choices.append("  Exit")

        choice = questionary.select("Turn Order:", choices=choices, qmark="", instruction="").ask() or "do nothing"

        if choice == "  End Turn":
            encounter.advance_turn()
            continue
        elif choice == "  Exit":
            break
        else:
            action, value = input(choice).split()
            if action.lower() == "damage":
                encounter.combatant_list[encounter.combatant_list.index(choice)].damage(int(value))
            elif action.lower() == "heal":
                encounter.combatant_list[encounter.combatant_list.index(choice)].heal(int(value))




if __name__ == "__main__":
    database = Database("test.db")
    database.create_tables()
    clear_screen()

    while True:

        action = (questionary.select("Welcome to tracker, please select from the options below:", 
            choices=[
                "Start new encounter",
                "Load encounter",
                "Exit"], qmark="", instruction="").ask() or "do nothing")

        match action:
            case "Start new encounter":
                encounter = Encounter()

                while True:
                    choice = sub_menu_questions()
                    check = choice_menu(choice, encounter)
                    if check == None:
                        continue
                    elif check == "Exit":
                        break
                    elif check == "Save": 
                        database.save_encounter(encounter)
                    elif check == "Start":
                        active_encounter(encounter)
            case "Load encounter":
                encounter  = database.load_encounter()

                while True:
                    choice = sub_menu_questions()
                    check = choice_menu(choice, encounter)
                    if check == None:
                        continue
                    elif check == "Exit":
                        break
                    elif check == "Save": 
                        database.save_encounter(encounter)
                    elif check == "Start":
                        active_encounter(encounter)
            case "Exit":
                break
            case _:
                print("No option chosen")