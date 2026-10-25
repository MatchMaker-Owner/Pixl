
import random
print("◙" *76)
print("="*25,">>>>>>☆*: ｡ o≧▽≦o ｡:*☆ WELCOME TO THE ULTIMATE VERSE ☆*: ｡ o≧▽≦o ｡:*☆ <<<<<<","="*25)
print("="*36,">>>>>>>>>>      ⓿_⓿ THE GLORY VERSE ⓿_⓿        <<<<<<<<<<<","="*36)
print("◙" *76)
# --- START OF GAME SETUP AND RULES ---
while True:
    Lobby = input("Enter your own name for your character:\t")
    # This check is always True since input() returns a string, but we keep the structure.
    # We proceed as the name is entered.
    
    print()
    print("!!! 🌟 RULES FOR THIS GAME 🌟 !!!")
    print("1. There are 2 Levels for this game")
    print("2. LEVEL 1 ----> NUMBER GUESSING GAME")
    print("3. LEVEL 2 -----> GLORY VERSE ADVENTURE")
    print("-" * 30) # Separator for better readability
    
    # Standardize input check for 'YES'
    user_input = input("DO YOU WANT TO CONTINUE WITH LEVEL 1? (Yes/No): ")
    if user_input.lower() == "yes":
        print()
        print("--- INSTRUCTIONS FOR LEVEL 1 ---")
        print("GLORY", Lobby ,"is your virtual character. In this level, you set a positive number as a range.")
        print("You must now guess the number between 0 and the range you set.")
        print("During the game, Glory will instruct you if your guess is above or below the secret number.")
        print("If you guess correctly, Glory wins, congratulations will appear, and you will be teleported to the Glory Verse!")
        # Break out of the initial setup loop to start the game logic
        break 
    else:
        # If the user doesn't type 'yes', exit the program with a message.
        print("🚫 Game initialization stopped. Please restart the Game to play Level 1.")
        exit() # Use exit() or quit() to stop the script completely

import random # We need random for generating the secret number

# --- START OF LEVEL 1: NUMBER GUESSING GAME ---

# 1. Get the upper limit for the range
print()
print()
top_of_range = input("Type an upper limit number for the game range: ")

if top_of_range.isdigit():
    top_of_range = int(top_of_range)

    if top_of_range <= 0:
        print('Please type a number larger than 0 next time.')
        quit()
else:
    print('Please type a number next time.')
    quit()

# Game Setup
random_number = random.randint(0, top_of_range)
guesses = 0
MAX_GUESSES = 8 # NEW: Maximum guess limit set to 8
game_won = False

print("\n--- Game Start ---")
print(f"I'm thinking of a number between 0 and {top_of_range}. You have {MAX_GUESSES} tries!")

# 2. Main Guessing Loop
while guesses < MAX_GUESSES: # Loop condition now checks the new 8 guess limit
    guesses += 1
    
    # Display remaining attempts
    print(f"\nGuess {guesses} of {MAX_GUESSES}.")
    
    user_guess = input("Make a guess: ")
    
    # Input validation
    if user_guess.isdigit():
        user_guess = int(user_guess)
        # Check if the guess is outside the allowed range (0 to top_of_range)
        if user_guess > top_of_range or user_guess < 0:
            print(f'Please make a guess between 0 and {top_of_range}.')
            guesses -= 1 # Don't count invalid attempts against the limit
            continue
    else:
        print('Please type a valid number next time.')
        guesses -= 1 # Don't count invalid attempts against the limit
        continue

    # Check the guess
    if user_guess == random_number:
        print("☆Congratulations☆!! You got it!")
        game_won = True
        break
    elif user_guess > random_number:
        print("You were **above** the number!")
    else:
        print("You were **below** the number!")


# 3. Game Over and Scoring
# --------------------------------------------------------------------

print("\n----------------- GAME OVER -----------------")

if game_won:
    print(f"You correctly guessed the number **{random_number}**.")
    print(f"You got it in **{guesses}** guesses.")
    
    # Calculate score: Score is MAX_GUESSES for 1 guess, 1 point for 8 guesses.
    score = MAX_GUESSES - guesses + 1
    
    # Create the score bar visualization
    score_bar = "★" * score + "☆" * (MAX_GUESSES - score)
    
    print(f"\n✅ Your Score: {score}/{MAX_GUESSES}")
    print(f"Score Bar: [{score_bar}]")
    
else:
    print(f"❌ You ran out of guesses! The correct number was **{random_number}**.")
    
    # Display the empty score bar (8 empty stars)
    score_bar_empty = "☆" * MAX_GUESSES
    print(f"\nScore Bar: [{score_bar_empty}]")

print("---------------------------------------------")
#############################################################################################################################################################################################


print()
# --- Adventure Game: The Gory's Lair ---
# Standardize input check for 'YES'
while True:
    user_input = input("DO YOU WANT TO CONTINUE WITH LEVEL 2? (Yes/No): ")
    if user_input.lower() == "yes":
        print()
        print("--- INSTRUCTIONS FOR LEVEL 2 ---")
        print()
        print("Available commands:")
        print("  - **quit** / **exit**: End the game.")
        print("  - **go [direction]**: Move (e.g., 'go east'). Directions: north, south, east, west.")
        print("  - **take [item]**: Pick up an item (e.g., 'take crystal').")
        print("  - **inventory**: Check the items you are carrying.")
        print("  - **attack troll**: Engage the enemy in the Chamber.")
        print("  - **cross river**: Attempt to cross the river (requires Rope or Blade).")
        print("  - **place items**: Attempt to solve the puzzle in the Altar Room.")
        print()
        print("Type help for intractive help in between the game whenever required!")
        # Break out of the initial setup loop to start the game logic
        break 
    else:
        # If the user doesn't type 'yes', exit the program with a message.
        print("🚫 Game initialization stopped. Please restart the Game.")
        print("Kudos!! You won Level 1")
        exit() # Use exit() or quit() to stop the script completely
        

import random # We need random for combat rolls

# --- Game Helper Variables (used for combat and random chance) ---

# Player Stats
player_hp = 100 # CORRECTION 1: HP is now 100
player_location = "Entrance"
inventory = []
game_over = False
has_won = False

# Location and Item Data Structure
locations = {
    "Entrance": {
        "description": "You stand at the cold, damp entrance to the lair. A faint, glowing Crystal sits on a ledge nearby. A coiled **Rope** lies on the ground.",
        "exits": {"east": "Chamber"}
    },
    "Chamber": {
        "description": "A dark, oppressive room. A grumpy Cave Troll blocks the North path.",
        "exits": {"west": "Entrance"},
        "enemy": {
            "name": "Cave Troll",
            "hp": 30,
            "damage": 15,
            "defeated": False,
            "turn_count": 0 # Added to track combat turns
        }
    },
    "River Bank": {
        # CORRECTION 3: Added a warning about the deadly current
        "description": "A swift, dark river flows here, heading deadly South. You see something glinting on a small rock midstream. To the south is the Chamber.",
        "exits": {"south": "Chamber"}
    },
    "Altar Room": {
        "description": "A large cavern with a stone pedestal in the center, bearing three empty slots. A rusty **Shield** lies discarded in a corner.",
        "exits": {"south": "River Bank"}
    },
    "Treasure Room": {
        "description": "You stand before a dazzling hoard of gold and the Serpent's Crown!",
        "exits": {}
    }
}

# --- Game Loop ---
print()
print()
print("--- The Glory's Lair Adventure ---")
print("You seek the Glory's Crown. Be wary of dangers!")
print("Type 'help' for commands.")
print("-------------------------------------")

# Main loop
while not game_over:
    # Check if the player is alive
    if player_hp <= 0:
        game_over = True
        print("\n*** YOUR HEALTH REACHED ZERO. YOU HAVE PERISHED. ***")
        break

    # Check for win condition (Player is in the Treasure Room)
    if player_location == "Treasure Room":
        has_won = True
        game_over = True
        break

    # 1. Display Status and Location
    print("\n")
    print("--- Location: " + player_location + " | HP: " + str(player_hp) + " ---")
    print(locations[player_location]["description"])

    # 2. Check for Enemy (Troll) and initiate combat dialogue
    if player_location == "Chamber" and "enemy" in locations["Chamber"] and not locations["Chamber"]["enemy"]["defeated"]:
        print("!! WARNING: The **Cave Troll** is hostile and ready to attack! !!")
        
    # 3. Get user input
    user_input = input("What do you do? ").lower().strip()
    
    # 4. Process Commands
    
    # Basic Commands (Quit, Help, Inventory)
    if user_input == "quit" or user_input == "exit":
        game_over = True
        print("Thanks for escaping! Goodbye.")
        
    elif user_input == "help":
        print("Available commands:")
        print("  - **quit** / **exit**: End the game.")
        print("  - **go [direction]**: Move (e.g., 'go east'). Directions: north, south, east, west.")
        print("  - **take [item]**: Pick up an item (e.g., 'take crystal').")
        print("  - **inventory**: Check the items you are carrying.")
        print("  - **attack troll**: Engage the enemy in the Chamber.")
        print("  - **cross river**: Attempt to cross the river (requires Rope or Blade).")
        print("  - **place items**: Attempt to solve the puzzle in the Altar Room.")
        
    elif user_input == "inventory":
        if inventory:
            print("You are carrying: " + ", ".join(inventory))
        else:
            print("Your inventory is empty.")

    # Movement
    elif user_input.startswith("go "):
        direction = user_input[3:].strip()
        
        # Check if the path is blocked by the Troll
        if player_location == "Chamber" and direction == "north" and "enemy" in locations["Chamber"] and not locations["Chamber"]["enemy"]["defeated"]:
             print("The **Cave Troll** is blocking the way! You must defeat it first.")
             continue # Skip to the next loop iteration
        
        # CORRECTION 3: Drowning check at River Bank
        if player_location == "River Bank" and direction == "south":
            print("\n*** The river's current is too fierce! You are swept away to your doom! ***")
            player_hp = 0 # Instant defeat
            continue

        if direction in locations[player_location]["exits"]:
            player_location = locations[player_location]["exits"][direction]
        else:
            print("You can't go that way.")

    # Taking Items (No changes to logic, just location)
    elif user_input.startswith("take "):
        item_to_take = user_input[5:].strip().capitalize()
        
        # Taking Crystal
        if player_location == "Entrance" and item_to_take == "Crystal":
            if "Crystal" not in inventory:
                inventory.append(item_to_take)
                print("You take the shimmering **Crystal**.")
                locations["Entrance"]["description"] = locations["Entrance"]["description"].replace("A faint, glowing Crystal sits on a ledge nearby. ", "")
            else:
                 print("You already have the Crystal.")
        
        # Taking Rope
        elif player_location == "Entrance" and item_to_take == "Rope":
            if "Rope" not in inventory:
                inventory.append(item_to_take)
                print("You pick up the coiled **Rope**.")
                locations["Entrance"]["description"] = locations["Entrance"]["description"].replace("A coiled **Rope** lies on the ground.", "")
            else:
                 print("You already have the Rope.")
        
        # Taking Blade (after Troll is defeated)
        elif player_location == "Chamber" and item_to_take == "Blade":
            
            if "enemy" in locations["Chamber"] and locations["Chamber"]["enemy"]["defeated"] and "Blade" not in inventory:
                
                # IMPORTANT: Remove the enemy data after the blade is taken, reset turn_count
                del locations["Chamber"]["enemy"]
                
                inventory.append(item_to_take)
                print("You retrieve a sharp **Blade** dropped by the Troll.")
                locations["Chamber"]["description"] = locations["Chamber"]["description"].replace(" You see a shiny **Blade** dropped by the Troll.", "")
            elif "Blade" in inventory:
                 print("You already have the Blade.")
            else:
                 print("There is no Blade here to take.")

        # Taking Shield
        elif player_location == "Altar Room" and item_to_take == "Shield":
            if "Shield" not in inventory:
                inventory.append(item_to_take)
                print("You pick up the rusty **Shield**.")
                locations["Altar Room"]["description"] = locations["Altar Room"]["description"].replace("A rusty **Shield** lies discarded in a corner.", "")
            else:
                print("You already have the Shield.")
            
        else:
            print("There is no " + item_to_take.lower() + " here to take.")

    # Combat System (Attack Troll) - CORRECTION 2 APPLIED HERE
    elif user_input == "attack troll":
        if player_location == "Chamber" and "enemy" in locations["Chamber"] and not locations["Chamber"]["enemy"]["defeated"]:
            enemy = locations["Chamber"]["enemy"]
            
            # CORRECTION 2: Time-Based Damage for subsequent turns
            if enemy["turn_count"] > 0:
                player_hp -= 15
                print("The Troll capitalizes on your delay! You take **15** bonus damage! Your HP: " + str(player_hp))
            
            # Increment turn count
            enemy["turn_count"] += 1

            print("\n*** COMBAT START: You attack the " + enemy["name"] + "! ***")
            
            # Player attack (always hits for now)
            player_damage = 10
            enemy["hp"] = enemy["hp"] - player_damage
            print("You strike the Troll for **" + str(player_damage) + "** damage! Troll HP: " + str(enemy["hp"]))
            
            # Check if Troll is defeated
            if enemy["hp"] <= 0:
                enemy["defeated"] = True
                print("The **Cave Troll** collapses! You see a shiny **Blade** among its possessions.")
                
                locations["Chamber"]["description"] += " You see a shiny **Blade** dropped by the Troll."
                locations["Chamber"]["exits"]["north"] = "River Bank"
            else:
                # Troll counter-attack
                if random.random() < 0.7:
                    troll_damage = enemy["damage"]
                    player_hp = player_hp - troll_damage
                    print("The Troll smashes you for **" + str(troll_damage) + "** damage! Your HP: " + str(player_hp))
                else:
                    print("The Troll swings wildly, but you dodge the attack!")

        else:
            print("There is nothing hostile to attack here.")
            
    # Special Interaction (Crossing River)
    elif user_input == "cross river":
        if player_location == "River Bank":
            if "Rope" in inventory: 
                print("You use the sturdy **Rope** to secure a line and cross safely.")
                player_location = "Altar Room"
            elif "Blade" in inventory:
                 print("The **Blade** is sharp enough to cut a vine and make a crude Rope! You cross safely, but the Blade breaks.")
                 inventory.remove("Blade")
                 player_location = "Altar Room"
            else:
                print("The river is too fast and wide. You need a way to cross safely.")
        else:
            print("You are not at a river you can cross.")

    # Puzzle Solving (Altar Room)
    elif user_input == "place items":
        if player_location == "Altar Room":
            # Check if the player has the required items
            if "Crystal" in inventory and "Blade" in inventory and "Shield" in inventory:
                print("The **Crystal**, **Blade**, and **Shield** fit perfectly into the pedestal slots!")
                print("A hidden door opens to the North...")
                locations["Altar Room"]["exits"]["north"] = "Treasure Room"
                print("The path to the **Treasure Room** is open! (Try 'go north').")
                
                # Consume items for the puzzle
                inventory.remove("Crystal")
                inventory.remove("Blade")
                inventory.remove("Shield")
            else:
                print("The pedestal is empty. You need the **Crystal**, **Blade**, and **Shield**.")
                # Show what's missing
                missing = []
                if "Crystal" not in inventory: missing.append("Crystal")
                if "Blade" not in inventory: missing.append("Blade")
                if "Shield" not in inventory: missing.append("Shield")

                print("You are missing: " + ", ".join(missing))
        else:
            print("You can only place items on the altar in the Altar Room.")

    else:
        print("Invalid command. Type 'help' for valid actions.")

# --- End of Game ---
if player_location == "Treasure Room":
    print("\n\n####################################################################")
    print("      *** CONGRATULATIONS! YOU HAVE CLAIMED THE GLORY'S CROWN! ***")
    print("####################################################################")
print()
print("◙" *76)
print("="*25,">>>>>>❤️ END OF GLORY VERSE ❤️ <<<<<<","="*25)
print("="*36,">>>>>>>>>>      ⓿_⓿ HOPE YOU ENJOYED ⓿_⓿        <<<<<<<<<<<","="*36)
print("◙" *76)
