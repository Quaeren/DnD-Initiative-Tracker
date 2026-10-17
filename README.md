# Initiative Tracker for TTRPGS
A simple command line interface for running a initiative tracker in the terminal. You can create an encounter, add combatants, roll initiative, track health and save encounters for later use.

## Features
- **Combatant Mangement** Add or remove players, enemies or allies in an encounter
- **Automatic Turn Tracking** After letting the program roll the initiative it autmatically tracks whoose turn it is
- **Health Management** Add or remove health via the damage and heal funcitons
- **Save and Load** Save and load encounters between sessions for quick and easy playthroughs

## How to Use
### Main menu
When the application starts, you can choose to:
- **Start new encounter:** Create an empty encounter.
- **Load** encounter:** Load the saved encounter.
- **Exit:** Close the application.

### Managing an encounter
Once an encounter has been created or loaded, the encounter menu provides the following options:
- **Add combatant:** Enter a name, maximum hit points, initiative modifier, and combatant type.
- **Remove combatant:** Select combatants to remove from the encounter.
- **View turn order:** Sort combatants by initiative and display their current health and initiative.
- **Roll initiative:** Roll initiative for every combatant.
- **Start encounter:** Open the turn-order menu and begin managing combat.
- **Save encounter:** Save the encounter's current state to the database.
- **Exit:** Return to the main menu.

During an encounter, the currently active combatant is marked with an arrow. You can advance to the next turn, reset the round counter, or select a combatant to perform a health-related action.

### Actions on a combatant
Once you select a combatant you are presented with the option to input a command, the following commands are allowed:
- **damage** after inputting enter a value and the corresponding health will be removed
- **heal** after inputting enter a value and the corresponding health will be healed
- **set** after inputting manually set and initiative value for the combatant
- **exit** after inputting press enter again and exit this menu

## License
MIT