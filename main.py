#!/usr/bin/env python3
"""
Turbo's Quest - A Heartwarming Pet Adventure (Cleaned Up Version)
A special text adventure about Maxwell's mysterious intuition and Turbo's quest
Built with love for a dear friend expecting a wonderful surprise!

This cleaned version removes:
- Unused health/combat system
- Unused item values and consumable logic
- Redundant error handling
- Unused item effects
"""

import json
import os


class Player:
    """
    Represents Turbo, the adventurous German Shepherd
    This class manages Turbo's inventory and progress through the game
    """
    def __init__(self, name="Turbo"):
        self.name = name
        self.inventory = []  # Items Turbo is carrying or has found
        self.current_location = None  # Current room/area Turbo is in
        self.discovered_locations = []  # Places Turbo has visited
        self.completed_actions = []  # Actions completed (prevents repetition)
        self.quest_items_found = 0  # Track progress toward the big revelation
        self.size_realization_triggered = False  # Tracks if Turbo realized the size significance
    
    def add_item(self, item_id, items_data):
        """
        Add an item to Turbo's inventory when he finds something
        This method also tracks quest progress and shows pickup messages
        """
        if item_id in items_data:
            item = items_data[item_id]
            self.inventory.append(item_id)
            print(item.get("pickup_message", f"You found: {item['name']}"))
            
            # Check if this is a quest item (helmet, gloves, or bike)
            if item.get("special_effect") == "quest_item":
                self.quest_items_found += 1
                print(f"\n🎾 Progress: You've found {self.quest_items_found}/3 special items!")
                
                # Show encouragement as Turbo gets closer to the revelation
                if self.quest_items_found == 1:
                    print("Maxwell purrs softly. You're on the right track!")
                elif self.quest_items_found == 2:
                    print("Maxwell's tail swishes with excitement. One more to go!")
                elif self.quest_items_found == 3:
                    print("Maxwell's eyes are bright with anticipation. You have all the pieces now...")
                    print("💡 Try using 'examine all items' to understand what you've collected!")
        else:
            print(f"Error: Item '{item_id}' not found in game data.")
    
    def remove_item(self, item_id, items_data):
        """
        Remove an item from Turbo's inventory when it's used
        """
        if item_id in self.inventory:
            self.inventory.remove(item_id)
            if item_id in items_data:
                item = items_data[item_id]
                print(item.get("use_message", f"You used: {item['name']}"))
            return True
        else:
            print(f"You don't have that item with you.")
            return False
    
    def has_item(self, item_id):
        """
        Check if Turbo currently has a specific item in his inventory
        """
        return item_id in self.inventory
    
    def show_inventory(self, items_data):
        """
        Display what Turbo is currently carrying
        This helps players track their progress and available tools
        """
        if self.inventory:
            print(f"\n🎾 {self.name}'s Current Items:")
            for item_id in self.inventory:
                if item_id in items_data:
                    item = items_data[item_id]
                    print(f"  - {item['name']}: {item['description']}")
                else:
                    print(f"  - {item_id} (unknown item)")
        else:
            print(f"\n{self.name} isn't carrying anything right now.")
    
    def show_stats(self):
        """
        Display Turbo's current status including progress toward the goal
        """
        print(f"\n--- {self.name}'s Status ---")
        print(f"Location: {self.current_location}")
        print(f"Items Found: {len(self.inventory)}")
        print(f"Quest Progress: {self.quest_items_found}/3 special items")
        if self.size_realization_triggered:
            print("🧠 Understanding: You've realized something important about these items!")
        print(f"Areas Explored: {len(self.discovered_locations)}")


class DataLoader:
    """
    Handles loading all game data from JSON files
    This separates the game logic from the game content, making it easy to modify
    """
    def __init__(self, data_directory="data"):
        self.data_dir = data_directory
        self.locations = {}
        self.items = {}
        self.story_config = {}
    
    def load_all_data(self):
        """
        Load all game data from JSON files
        Returns True if successful, False if there's an error
        """
        try:
            self.locations = self.load_json_file("locations.json")
            self.items = self.load_json_file("items.json")
            self.story_config = self.load_json_file("story.json")
            print("🎮 Game data loaded successfully!")
            return True
        except Exception as e:
            print(f"❌ Error loading game data: {e}")
            print("Make sure you have the 'data' folder with all JSON files!")
            return False
    
    def load_json_file(self, filename):
        """
        Load a specific JSON file from the data directory
        Handles file not found and JSON parsing errors
        """
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise Exception(f"Could not find {filename} in {self.data_dir} directory")
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON format in {filename}")


class GameEngine:
    """
    Main game engine for Turbo's Quest
    Handles the game loop, commands, and Maxwell's mysterious guidance
    This is the heart of the game that brings everything together
    """
    def __init__(self):
        self.player = None
        self.game_running = True
        self.data_loader = DataLoader()
        self.game_won = False
        self.revelation_triggered = False
        
        # Load all game data from JSON files
        if not self.data_loader.load_all_data():
            print("Failed to load game data. Exiting...")
            exit(1)
        
        # Create quick references to loaded data for easier access
        self.locations = self.data_loader.locations
        self.items = self.data_loader.items
        self.story_config = self.data_loader.story_config
    
    def start_game(self):
        """
        Initialize and start Turbo's adventure
        Sets up the player and shows the opening story
        """
        intro = self.story_config.get("intro_text", {})
        
        print("=" * 60)
        print(intro.get("welcome_message", "🐕 Welcome to Turbo's Quest! 🐕"))
        print("=" * 60)
        print(intro.get("game_description", "A mysterious adventure awaits..."))
        print()
        
        # Simple start prompt for our story
        input(intro.get("name_prompt", "Press Enter to begin Turbo's adventure..."))
        
        # Create Turbo - no health system needed
        self.player = Player("Turbo")
        
        # Set Turbo's starting location
        starting_location = self.story_config.get("game_settings", {}).get("starting_location", "living_room")
        self.player.current_location = starting_location
        
        print(f"\n🐕 You are Turbo, and something mysterious is happening...")
        print(intro.get("instruction_text", "Follow Maxwell's guidance!"))
        print("\n🎯 Trust Maxwell's cat intuition to discover his wonderful secret!")
        
        # Show the starting location description
        self.describe_current_location()
        
        # Start the main game loop
        self.game_loop()
    
    def game_loop(self):
        """
        Main game loop - keeps Turbo's adventure running
        This continues until the player quits or wins the game
        """
        while self.game_running:
            # Check if we should trigger the final revelation
            if (not self.revelation_triggered and 
                self.player.size_realization_triggered and 
                self.check_all_items_collected()):
                self.trigger_final_revelation()
            
            # Get player input and process it
            user_input = input("\n🐕 > ").strip().lower()
            self.process_command(user_input)
    
    def process_command(self, command):
        """
        Process Turbo's commands and execute appropriate actions
        This is where we interpret what the player wants to do
        
        Automatically shows location info after most actions to help players stay oriented
        """
        # Flag to track if we should show location info after this command
        show_location_after = True
        
        # Basic commands that work everywhere
        if command in ["quit", "exit"]:
            messages = self.story_config.get("messages", {})
            exit_msg = messages.get("exit_message", f"Thanks for playing!")
            print(exit_msg)
            self.game_running = False
            return
        
        elif command == "help":
            self.show_help()
            show_location_after = False  # Help already shows what you need
            
        elif command in ["inventory", "i"]:
            self.player.show_inventory(self.items)
            show_location_after = False  # Inventory is separate from location
            
        elif command == "stats":
            self.player.show_stats()
            show_location_after = False  # Stats are separate from location
            
        elif command in ["look", "l"]:
            self.describe_current_location()
            show_location_after = False  # We just showed location info
            
        # Special command to examine all quest items together
        elif command in ["examine all items", "examine items", "compare items", "look at all items"]:
            self.examine_all_quest_items()
            # After this major story moment, show where we are
            
        # Handle movement commands - simplified to use location names
        elif self.handle_movement_command(command):
            show_location_after = False  # Movement already shows new location
            
        # Check special actions available in current location
        elif self.handle_location_action(command):
            # After performing an action, we'll show location info
            pass
            
        else:
            # Command not recognized - give helpful feedback
            messages = self.story_config.get("messages", {})
            invalid_msg = messages.get("invalid_command", "You tilt your head, confused.")
            print(invalid_msg)
            show_location_after = False  # We'll show help instead
            
            # Show available options to help the player
            self.show_current_options()
        
        # Show location info after most actions to keep player oriented
        if show_location_after and self.game_running:
            self.show_quick_location_reminder()
    
    def handle_movement_command(self, command):
        """
        Handle movement between locations
        Returns True if the command was a valid movement, False otherwise
        """
        current_loc = self.locations[self.player.current_location]
        exits = current_loc.get("exits", {})
        
        # Check if command matches any exit destination
        for exit_key, destination in exits.items():
            if command == exit_key or command == destination:
                self.move_player(destination)
                return True
        return False
    
    def handle_location_action(self, command):
        """
        Handle special actions available in the current location
        Returns True if the command was a valid action, False otherwise
        """
        current_loc = self.locations[self.player.current_location]
        actions = current_loc.get("actions", {})
        
        if command in actions:
            action_id = actions[command]
            self.handle_special_action(action_id)
            return True
        return False
    
    def show_current_options(self):
        """
        Show what the player can currently do - used when they enter invalid commands
        This helps players understand their options without being overwhelming
        """
        current_loc = self.locations[self.player.current_location]
        actions = current_loc.get("actions", {})
        exits = current_loc.get("exits", {})
        
        print("\n💡 You can try:")
        
        # Show available actions first (most important)
        if actions:
            for action in actions.keys():
                print(f"  - {action}")
        
        # Show movement options
        if exits:
            print("  Or go to:")
            for exit_name in exits.keys():
                print(f"  - {exit_name}")
        
        # Show basic commands
        print("  Other commands: 'help', 'inventory', 'look', 'stats'")
        
        # If player has all quest items but hasn't realized the size significance, give a hint
        if (self.check_all_items_collected() and 
            not self.player.size_realization_triggered):
            print("\n🎯 QUEST UPDATE: You have all three special items!")
            print("💡 HINT: Try 'examine all items' to understand what they have in common.")
        # If player has size realization but hasn't triggered final revelation
        elif (self.player.size_realization_triggered and 
              not self.revelation_triggered):
            print("\n🎯 QUEST PHASE 2: Ready for Maxwell's final revelation!")
            print("💫 Move to any location or use 'look' to discover the truth!")
    
    def show_quick_location_reminder(self):
        """
        Show a brief reminder of where Turbo is and what he can do
        This appears after actions to keep players oriented without being too verbose
        """
        location_id = self.player.current_location
        location = self.locations[location_id]
        
        print(f"\n📍 Currently in: {location['name']}")
        
        # Show available actions in a compact format
        actions = location.get("actions", {})
        if actions:
            actions_list = list(actions.keys())
            if len(actions_list) <= 3:
                # If few actions, show them all
                print(f"🎯 Can do: {', '.join(actions_list)}")
            else:
                # If many actions, show first few and indicate there are more
                print(f"🎯 Can do: {', '.join(actions_list[:3])}, and more ('look' to see all)")
        
        # Show available exits in a compact format
        exits = location.get("exits", {})
        if exits:
            exits_list = list(exits.keys())
            print(f"🚪 Can go to: {', '.join(exits_list)}")
        
        # Show quest progress if relevant
        if self.player.quest_items_found > 0:
            if not self.player.size_realization_triggered:
                print(f"🎾 Quest Phase 1: {self.player.quest_items_found}/3 special items found")
            elif not self.revelation_triggered:
                print(f"🎾 Quest Phase 2: Understanding achieved, final revelation pending")
            else:
                print(f"🎉 Quest Complete: Maxwell's wonderful secret revealed!")
    
    def examine_all_quest_items(self):
        """
        Allows Turbo to examine all quest items together
        This triggers the size realization - the intermediate step before the final revelation!
        """
        quest_items = ["child_mtb_helmet", "child_mtb_gloves", "small_mtb_bike"]
        
        # Check if player has all quest items
        if not all(self.player.has_item(item) for item in quest_items):
            print("You don't have all the special items yet to compare them properly.")
            print("Keep following Maxwell's guidance!")
            return
        
        # If already triggered, just show a brief description
        if self.player.size_realization_triggered:
            print("You look at the three items together again:")
            print("The colorful helmet, the adventure gloves, and the beautiful bike.")
            print("Now you understand - they're all designed for someone special...")
            print("Maxwell's plan is becoming clearer!")
            return
        
        # Trigger the size realization scene
        print("\n" + "="*50)
        print("🧠 MOMENT OF UNDERSTANDING 🧠")
        print("="*50)
        
        print("\nYou gather all three special items together and examine them carefully...")
        print("The colorful helmet with its protective padding...")
        print("The adventure gloves with their sturdy grip...")
        print("The beautiful bike, perfectly crafted and ready for fun...")
        print("\nYou tilt your head as you study each item more closely.")
        print("Wait a minute... something's becoming clear about these items...")
        print("\nAs you look at them all together, a pattern emerges.")
        print("They're not just random adventure gear...")
        print("They all seem to be made for the same person!")
        print("But who in your family would need ALL of these things?")
        print("\nYour ears perk up with growing excitement...")
        print("These items aren't meant for any of the adult humans you know...")
        print("They're all perfectly sized for someone much smaller!")
        print("Someone who doesn't live in your house yet...")
        print("\nYour tail starts wagging as understanding dawns.")
        print("Maxwell appears beside you, purring softly, his eyes twinkling")
        print("with approval. You're getting closer to understanding his secret!")
        
        print("\n💡 You're starting to understand Maxwell's mysterious quest!")
        print("But there's still one more piece to the puzzle...")
        print("What does this all MEAN for your family?")
        print("="*50)
        
        # Mark the size realization as triggered
        self.player.size_realization_triggered = True
        
        print("\n🎯 QUEST PROGRESS: You've unlocked the next phase!")
        print("💭 Now that you understand these items have a special purpose,")
        print("   you need to discover WHY Maxwell wanted you to find them.")
        print("\n🎮 NEXT STEP: Visit any location or use 'look' to trigger Maxwell's")
        print("   final revelation about what these items really mean!")
    
    def move_player(self, new_location):
        """
        Move Turbo to a new location
        Updates player position and shows the new area description
        """
        if new_location in self.locations:
            self.player.current_location = new_location
            
            # Add to discovered locations if not already visited
            if new_location not in self.player.discovered_locations:
                self.player.discovered_locations.append(new_location)
            
            location_name = self.locations[new_location]['name']
            print(f"\n🐕 You move to the {location_name}...")
            self.describe_current_location()
        else:
            print(f"Error: Location '{new_location}' not found!")
    
    def describe_current_location(self):
        """
        Show the full description of Turbo's current location
        Uses first-visit description for new areas, regular description for revisits
        """
        location_id = self.player.current_location
        location = self.locations[location_id]
        
        print(f"\n--- 🏠 {location['name']} ---")
        
        # Show first visit description if available and not visited before
        if not location.get("visited", False) and "first_visit_description" in location:
            print(location["first_visit_description"])
        else:
            print(location["description"])
        
        # Show available actions (simplified and clear)
        actions = location.get("actions", {})
        if actions:
            print("\n🎯 You can:")
            for action in actions:
                print(f"  - {action}")
        
        # Show available exits
        exits = location.get("exits", {})
        if exits:
            print("\n🚪 You can go to:")
            for direction in exits:
                print(f"  - {direction}")
        
        # Add quest progress hints based on current phase
        if (self.check_all_items_collected() and 
            not self.player.size_realization_triggered):
            print("\n🎯 QUEST PHASE 1: You have all three special items!")
            print("💭 Try 'examine all items' to understand their significance.")
        elif (self.player.size_realization_triggered and 
              not self.revelation_triggered):
            print("\n🎯 QUEST PHASE 2: Maxwell's final revelation awaits!")
            print("💫 Continue exploring to discover the wonderful truth!")
        
        # Mark this location as visited
        location["visited"] = True
    
    def handle_special_action(self, action_id):
        """
        Handle special actions defined in the story JSON
        This is where the main story events happen
        """
        special_actions = self.story_config.get("special_actions", {})
        
        if action_id not in special_actions:
            print(f"Error: Action '{action_id}' not found!")
            return
        
        action = special_actions[action_id]
        
        # Check if this action was already completed (prevents repetition)
        if action_id in self.player.completed_actions:
            repeat_message = action.get("repeat_message", "You've already done that.")
            print(repeat_message)
            return
        
        # Check if Turbo has the required items for this action
        requirements = action.get("requirements", [])
        for req in requirements:
            if req.get("type") == "has_item":
                required_item = req.get("item")
                if not self.player.has_item(required_item):
                    req_message = req.get("message", f"You need {required_item} to do that.")
                    print(req_message)
                    return
        
        # Show what happens when Turbo performs this action
        print(action.get("description", "Something happens..."))
        
        # Apply the effects of this action (give items, trigger events, etc.)
        effects = action.get("effects", [])
        for effect in effects:
            self.apply_effect(effect)
        
        # Mark action as completed if it shouldn't be repeated
        if action.get("repeatable", False) == False:
            self.player.completed_actions.append(action_id)
    
    def apply_effect(self, effect):
        """
        Apply an effect from a special action
        Effects can give items or trigger story events
        """
        effect_type = effect.get("type")
        
        if effect_type == "give_item":
            item_id = effect.get("item")
            if item_id:
                self.player.add_item(item_id, self.items)
        
        elif effect_type == "trigger_revelation":
            # This effect prepares for the final revelation scene
            # But now we require the size realization first!
            if self.player.size_realization_triggered:
                self.revelation_triggered = True
            else:
                print("You sense that Maxwell's quest is almost complete...")
                print("But you feel like you need to understand something about these items first.")
        
        elif effect_type == "win_game":
            self.game_won = True
            self.game_running = False
    
    def check_all_items_collected(self):
        """
        Check if Turbo has found all three quest items
        This is used for both the size realization and final revelation
        """
        required_items = ["child_mtb_helmet", "child_mtb_gloves", "small_mtb_bike"]
        return all(self.player.has_item(item) for item in required_items)
    
    def trigger_final_revelation(self):
        """
        Trigger the final revelation scene - the heart of the story!
        This is where Turbo realizes what Maxwell has been trying to tell him
        """
        if not self.revelation_triggered:
            print("\n" + "="*60)
            print("🎉 THE WONDERFUL REVELATION! 🎉")
            print("="*60)
            
            print("\nNow that you understand these special items have a purpose,")
            print("Maxwell's mysterious behavior suddenly makes perfect sense!")
            print("\nYou sit quietly, thinking about what this means...")
            print("Adventure helmet... protective gloves... beautiful bike...")
            print("All perfectly made for someone who isn't here yet...")
            print("Someone who will need these special things...")
            print("\nSuddenly, your tail starts wagging uncontrollably!")
            print("Your heart fills with pure joy and excitement!")
            print("\n🍼 A NEW LITTLE FAMILY MEMBER IS COMING! 🍼")
            print("\nA tiny human who will need these adventure items!")
            print("Someone small who will grow up to wear that helmet,")
            print("use those gloves, and ride that beautiful bike!")
            print("\nMaxwell appears beside you, purring loudly, his green eyes")
            print("sparkling with satisfaction. He rubs against your leg lovingly.")
            print("His feline intuition knew this wonderful secret all along!")
            print("\nYour family is growing! Soon there will be a little human")
            print("to protect, play with, and eventually teach about")
            print("mountain biking adventures!")
            print("\nYou spin in a happy circle, barking with joy!")
            print("Maxwell's mysterious quest was about the most wonderful")
            print("surprise of all - a new baby is coming to your family!")
            print("="*60)
            
            self.revelation_triggered = True
            self.game_won = True
            
            print("\n🎾 Congratulations! You've solved Maxwell's mystery!")
            print("Thanks for playing Turbo's Quest!")
            print("\nType 'quit' to end the adventure.")
    
    def show_help(self):
        """
        Display available commands to help the player
        Shows the simplified command set for easier gameplay
        """
        messages = self.story_config.get("messages", {})
        help_lines = messages.get("help_text", [
            "--- Turbo's Commands ---",
            "Follow Maxwell's guidance and explore each location!",
            "Type the action you want to take or the place you want to go.",
            "Use 'help', 'look', 'inventory', 'stats', or 'quit'.",
            "",
            "Special commands:",
            "- 'examine all items' - Look at your quest items together",
            "",
            "🎯 QUEST: Follow Maxwell's guidance to find three special items!",
            "",
            "💡 TIP: After each action, you'll see a quick reminder of where",
            "you are and what you can do to help you stay oriented!"
        ])
        
        for line in help_lines:
            print(line)


def main():
    """
    Main function - creates and starts Turbo's Quest
    This is the entry point that gets everything running
    """
    print("🐕 Loading Turbo's Quest...")
    print("🐱 Maxwell is waiting with mysterious guidance...")
    
    # Create a new game instance
    game = GameEngine()
    
    # Start the adventure
    game.start_game()


# This runs the game when the script is executed directly
if __name__ == "__main__":
    main()