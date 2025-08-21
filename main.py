#!/usr/bin/env python3
"""
Console Dot Adventure - A Text Adventure Engine
A simple but expandable framework for creating text-based adventures
Now powered by JSON data files for easy story modification!
"""

import json
import os


class Player:
    """
    Represents the player character with basic stats and inventory
    """
    def __init__(self, name, starting_health=100):
        self.name = name
        self.health = starting_health
        self.max_health = starting_health
        self.inventory = []
        self.current_location = None  # Will be set by game engine
        self.discovered_locations = []  # Track which locations player has found
    
    def add_item(self, item_id, items_data):
        """Add an item to the player's inventory"""
        if item_id in items_data:
            item = items_data[item_id]
            self.inventory.append(item_id)
            print(item.get("pickup_message", f"You picked up: {item['name']}"))
        else:
            print(f"Error: Item '{item_id}' not found in game data.")
    
    def remove_item(self, item_id, items_data):
        """Remove an item from the player's inventory"""
        if item_id in self.inventory:
            self.inventory.remove(item_id)
            if item_id in items_data:
                item = items_data[item_id]
                print(item.get("use_message", f"You used: {item['name']}"))
            return True
        else:
            print(f"You don't have that item.")
            return False
    
    def has_item(self, item_id):
        """Check if player has a specific item"""
        return item_id in self.inventory
    
    def show_inventory(self, items_data):
        """Display the player's current inventory"""
        if self.inventory:
            print(f"\n{self.name}'s Inventory:")
            for item_id in self.inventory:
                if item_id in items_data:
                    item = items_data[item_id]
                    print(f"  - {item['name']}: {item['description']}")
                else:
                    print(f"  - {item_id} (unknown item)")
        else:
            print("\nYour inventory is empty.")
    
    def show_stats(self):
        """Display player's current stats"""
        print(f"\n--- {self.name}'s Stats ---")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Location: {self.current_location}")
        print(f"Items: {len(self.inventory)}")
        print(f"Locations Discovered: {len(self.discovered_locations)}")
    
    def heal(self, amount):
        """Heal the player by specified amount"""
        old_health = self.health
        self.health = min(self.health + amount, self.max_health)
        healed = self.health - old_health
        if healed > 0:
            print(f"You feel better! Healed {healed} health points.")
        else:
            print("You're already at full health!")


class DataLoader:
    """
    Handles loading and managing all game data from JSON files
    """
    def __init__(self, data_directory="data"):
        self.data_dir = data_directory
        self.locations = {}
        self.items = {}
        self.story_config = {}
    
    def load_all_data(self):
        """Load all game data from JSON files"""
        try:
            self.locations = self.load_json_file("locations.json")
            self.items = self.load_json_file("items.json")
            self.story_config = self.load_json_file("story.json")
            print("Game data loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading game data: {e}")
            print("Make sure you have the 'data' folder with all JSON files!")
            return False
    
    def load_json_file(self, filename):
        """Load a specific JSON file from the data directory"""
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
    Main game engine that handles the game loop, commands, and story flow
    Now loads all content from JSON files!
    """
    def __init__(self):
        self.player = None
        self.game_running = True
        self.data_loader = DataLoader()
        
        # Load all game data from JSON files
        if not self.data_loader.load_all_data():
            print("Failed to load game data. Exiting...")
            exit(1)
        
        # Quick access to loaded data
        self.locations = self.data_loader.locations
        self.items = self.data_loader.items
        self.story_config = self.data_loader.story_config
    
    def start_game(self):
        """Initialize the game and start the main game loop"""
        intro = self.story_config.get("intro_text", {})
        game_info = self.story_config.get("game_info", {})
        
        print("=" * 50)
        print(intro.get("welcome_message", "Welcome to Console.Adventure!"))
        print("=" * 50)
        print(intro.get("game_description", "A mysterious adventure awaits..."))
        print()
        
        # Get player name
        name_prompt = intro.get("name_prompt", "What's your name, adventurer?")
        player_name = input(f"{name_prompt} ").strip()
        if not player_name:
            player_name = "Unknown Adventurer"
        
        # Create player with settings from JSON
        settings = self.story_config.get("game_settings", {})
        starting_health = settings.get("starting_health", 100)
        self.player = Player(player_name, starting_health)
        self.player.max_health = settings.get("max_health", 150)
        
        # Set starting location
        starting_location = settings.get("starting_location", "start")
        self.player.current_location = starting_location
        
        print(f"\nWelcome, {self.player.name}!")
        print(intro.get("instruction_text", "Type 'help' for commands."))
        
        # Show starting location
        self.describe_current_location()
        
        # Start the main game loop
        self.game_loop()
    
    def game_loop(self):
        """Main game loop - keeps the game running until player quits"""
        while self.game_running:
            # Get player input
            user_input = input("\n> ").strip().lower()
            
            # Process the command
            self.process_command(user_input)
    
    def process_command(self, command):
        """Process player commands and execute appropriate actions"""
        # Basic commands that work everywhere
        if command in ["quit", "exit"]:
            messages = self.story_config.get("messages", {})
            exit_msg = messages.get("exit_message", f"Thanks for playing, {self.player.name}!")
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
        
        # Handle "use [item]" commands
        elif command.startswith("use "):
            item_name = command[4:].strip()
            self.use_item(item_name)
            return
        
        # Location-specific commands
        current_loc = self.locations[self.player.current_location]
        
        # Check exits (movement)
        exits = current_loc.get("exits", {})
        if command in exits:
            new_location = exits[command]
            self.move_player(new_location)
            return
        
        # Check special actions
        actions = current_loc.get("actions", {})
        if command in actions:
            action_id = actions[command]
            self.handle_special_action(action_id)
            return
        
        # Command not recognized
        messages = self.story_config.get("messages", {})
        invalid_msg = messages.get("invalid_command", "I don't understand that command.")
        print(invalid_msg)
    
    def move_player(self, new_location):
        """Move the player to a new location"""
        if new_location in self.locations:
            self.player.current_location = new_location
            
            # Add to discovered locations if not already there
            if new_location not in self.player.discovered_locations:
                self.player.discovered_locations.append(new_location)
            
            print(f"\nYou move to the {self.locations[new_location]['name']}...")
            self.describe_current_location()
        else:
            print(f"Error: Location '{new_location}' not found!")
    
    def describe_current_location(self):
        """Show the description of the current location"""
        location_id = self.player.current_location
        location = self.locations[location_id]
        
        print(f"\n--- {location['name']} ---")
        
        # Show first visit description if available and not visited
        if not location.get("visited", False) and "first_visit_description" in location:
            print(location["first_visit_description"])
        else:
            print(location["description"])
        
        # Show available exits
        exits = location.get("exits", {})
        if exits:
            print("\nYou can go:")
            for direction in exits:
                print(f"  - {direction}")
        
        # Show available actions
        actions = location.get("actions", {})
        if actions:
            print("\nYou can also:")
            for action in actions:
                print(f"  - {action}")
        
        # Mark as visited
        location["visited"] = True
    
    def handle_special_action(self, action_id):
        """Handle special actions defined in the story JSON"""
        special_actions = self.story_config.get("special_actions", {})
        
        if action_id not in special_actions:
            print(f"Error: Action '{action_id}' not found!")
            return
        
        action = special_actions[action_id]
        
        # Check requirements (future feature)
        requirements = action.get("requirements", [])
        # TODO: Implement requirement checking
        
        # Show action description
        print(action.get("description", "Something happens..."))
        
        # Apply effects
        effects = action.get("effects", [])
        for effect in effects:
            self.apply_effect(effect)
    
    def apply_effect(self, effect):
        """Apply an effect from a special action"""
        effect_type = effect.get("type")
        
        if effect_type == "give_item":
            item_id = effect.get("item")
            if item_id:
                self.player.add_item(item_id, self.items)
        
        elif effect_type == "heal_player":
            amount = effect.get("amount", 10)
            self.player.heal(amount)
        
        elif effect_type == "reveal_location":
            location_id = effect.get("location")
            if location_id and location_id in self.locations:
                # Add a new exit to current location
                current_loc = self.locations[self.player.current_location]
                if "exits" not in current_loc:
                    current_loc["exits"] = {}
                
                # Add a way to get to the secret location
                current_loc["exits"]["secret"] = location_id
                print(f"A secret passage has been revealed!")
        
        # Add more effect types as needed
    
    def use_item(self, item_input):
        """Handle using items from inventory"""
        # Find item by name (partial matching)
        item_id = None
        for inv_item_id in self.player.inventory:
            if inv_item_id in self.items:
                item = self.items[inv_item_id]
                if item_input.lower() in item["name"].lower():
                    item_id = inv_item_id
                    break
        
        if not item_id:
            print("You don't have that item, or I don't understand which item you mean.")
            return
        
        item = self.items[item_id]
        
        # Use the item
        print(item.get("use_message", f"You use the {item['name']}."))
        
        # Apply special effects
        special_effect = item.get("special_effect")
        if special_effect == "heal_player":
            self.player.heal(25)
        elif special_effect == "wisdom_boost":
            print("You feel more knowledgeable!")
        # Add more special effects as needed
        
        # Remove if consumable
        if item.get("consumable", False):
            self.player.remove_item(item_id, self.items)
    
    def show_help(self):
        """Display available commands to the player"""
        messages = self.story_config.get("messages", {})
        help_lines = messages.get("help_text", [
            "--- Available Commands ---",
            "Type 'help' for this message again."
        ])
        
        for line in help_lines:
            print(line)


def main():
    """
    Main function - creates and starts the game
    """
    print("Loading Console.Adventure...")
    
    # Create a new game instance
    game = GameEngine()
    
    # Start the game
    game.start_game()


# This runs the game when the script is executed
if __name__ == "__main__":
    main()