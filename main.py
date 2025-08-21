#!/usr/bin/env python3
"""
Turbo's Quest - A Heartwarming Pet Adventure (Streamlined Version)
A special text adventure about Maxwell's mysterious intuition and Turbo's quest
Built with love for a dear friend expecting a wonderful surprise!
"""

import json
import os
import random


class Player:
    """
    Represents Turbo, the adventurous German Shepherd
    This class manages Turbo's status, inventory, and progress through the game
    """
    def __init__(self, name="Turbo", starting_health=100):
        self.name = name
        self.health = starting_health
        self.max_health = starting_health
        self.inventory = []  # Items Turbo is carrying or has found
        self.current_location = None  # Current room/area Turbo is in
        self.discovered_locations = []  # Places Turbo has visited
        self.completed_actions = []  # Actions completed (prevents repetition)
        self.quest_items_found = 0  # Track progress toward the big revelation
    
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
                
        else:
            print(f"Error: Item '{item_id}' not found in game data.")
    
    def remove_item(self, item_id, items_data):
        """
        Remove an item from Turbo's inventory when it's used or consumed
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
        print(f"Energy: {self.health}/{self.max_health} 🐕")
        print(f"Location: {self.current_location}")
        print(f"Items Found: {len(self.inventory)}")
        print(f"Quest Progress: {self.quest_items_found}/3 special items")
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
        
        # Create Turbo with settings from the story configuration
        settings = self.story_config.get("game_settings", {})
        starting_health = settings.get("starting_health", 100)
        self.player = Player("Turbo", starting_health)
        self.player.max_health = settings.get("max_health", 100)
        
        # Set Turbo's starting location
        starting_location = settings.get("starting_location", "living_room")
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
            if not self.revelation_triggered and self.check_revelation_condition():
                self.trigger_final_revelation()
            
            # Get player input and process it
            user_input = input("\n🐕 > ").strip().lower()
            self.process_command(user_input)
    
    def process_command(self, command):
        """
        Process Turbo's commands and execute appropriate actions
        This is where we interpret what the player wants to do
        """
        # Basic commands that work everywhere
        if command in ["quit", "exit"]:
            messages = self.story_config.get("messages", {})
            exit_msg = messages.get("exit_message", f"Thanks for playing!")
            print(exit_msg)
            self.game_running = False
            return
        
        elif command == "help":
            self.show_help()
            return
        
        elif command in ["inventory", "i"]:
            self.player.show_inventory(self.items)
            return
        
        elif command == "stats":
            self.player.show_stats()
            return
        
        elif command in ["look", "l"]:
            self.describe_current_location()
            return
        
        # Handle movement commands - simplified to use location names
        current_loc = self.locations[self.player.current_location]
        exits = current_loc.get("exits", {})
        
        # Check if command matches any exit destination
        for exit_key, destination in exits.items():
            if command == exit_key or command == destination:
                self.move_player(destination)
                return
        
        # Check special actions available in current location
        actions = current_loc.get("actions", {})
        if command in actions:
            action_id = actions[command]
            self.handle_special_action(action_id)
            return
        
        # Command not recognized - give helpful feedback
        messages = self.story_config.get("messages", {})
        invalid_msg = messages.get("invalid_command", "You tilt your head, confused.")
        print(invalid_msg)
        
        # Show available options to help the player
        print("\n💡 You can try:")
        for action in actions.keys():
            print(f"  - {action}")
        if exits:
            print("  Or go to:")
            for exit_name in exits.keys():
                print(f"  - {exit_name}")
    
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
        Show the description of Turbo's current location
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
        Effects can give items, heal the player, or trigger story events
        """
        effect_type = effect.get("type")
        
        if effect_type == "give_item":
            item_id = effect.get("item")
            if item_id:
                self.player.add_item(item_id, self.items)
        
        elif effect_type == "heal_player":
            amount = effect.get("amount", 10)
            old_health = self.player.health
            self.player.health = min(self.player.health + amount, self.player.max_health)
            healed = self.player.health - old_health
            if healed > 0:
                print(f"You feel more energetic! Restored {healed} energy points. 🐕")
        
        elif effect_type == "trigger_revelation":
            # This effect prepares for the final revelation scene
            self.revelation_triggered = True
        
        elif effect_type == "win_game":
            self.game_won = True
            self.game_running = False
    
    def check_revelation_condition(self):
        """
        Check if Turbo has found all three quest items for the revelation
        The big reveal happens when Turbo has the helmet, gloves, and bike
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
            print("🎉 AMAZING REALIZATION! 🎉")
            print("="*60)
            
            print("\nYou sit down and look at all the items you've found...")
            print("The tiny helmet... the small gloves... the miniature bike...")
            print("\nSuddenly, your tail starts wagging uncontrollably!")
            print("These aren't just random objects - they're all CHILD-SIZED!")
            print("\nMaxwell appears beside you, purring loudly, his green eyes")
            print("twinkling with satisfaction. He rubs against your leg affectionately.")
            print("He's been trying to tell you something wonderful all along...")
            print("\n🍼 A NEW LITTLE FAMILY MEMBER IS COMING! 🍼")
            print("\nSomeone tiny enough to need these small adventure items!")
            print("Your family is growing, and Maxwell's mysterious cat")
            print("intuition knew before anyone else!")
            print("\nYour heart fills with joy and excitement. Soon there")
            print("will be a small human to protect, play with, and")
            print("eventually teach about mountain biking adventures!")
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
            "Use 'help', 'look', 'inventory', 'stats', or 'quit'."
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