from wsgiref import validate

import questionary
from tracker import Database, Encounter, Combatant

def sub_menu_questions():
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
        ],).ask() or "do nothing"

def choice_menu(choice, encounter):
        match choice:
            case "Add combatant":
                name = questionary.text("Name: ").ask()
                health = int(questionary.text("Health: ").ask())
                init_mod = int(questionary.text("Initiative modifier: ").ask())
                type = questionary.select(
                    "Select combatant tupe: ",
                    choices=["player", "enemy", "ally"],
                ).ask()

                encounter.add_combatant(Combatant(name, health, init_mod, type))
                print(f"Combatant: {name} added succesfully")
                return "None"
            case "Remove combatant":
                name = questionary.text("Name of combatant you would like to remove: ").ask()
                encounter.remove_combatant(name)
                print(f"Succesfully removed {name}")
                return "None"
            case "View turn order":
                encounter.sort_list()
                encounter.print_turn_order()
                return "None"
            case "Roll initiative":
                encounter.roll_all_initiative()
                return "None"
            case "Start encounter":
                return "Start"
            case "Save encounter":
                return "Save"
            case "Exit":
                return "Exit"


if __name__ == "__main__":
    database = Database("test.db")

    if not database.check():
        database.create_tables()

    while True:

        action = (questionary.select("Welcome to tracker, please select from the options below:", 
            choices=[
                "Start new encounter",
                "Load encounter",
                "Exit"],).ask() or "do nothing")

        match action:
            case "Start new encounter":
                encounter = Encounter()

                while True:
                    choice = sub_menu_questions()
                    check = choice_menu(choice, encounter)
                    if check == "None":
                        continue
                    elif check == "Exit":
                        break
                    elif check == "Save": 
                        pass
            case "Load encounter":
                pass
            case "Exit":
                break
            case _:
                print("No option chosen")