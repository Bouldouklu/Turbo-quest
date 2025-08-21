#!/usr/bin/env python3
"""
Console Dot Adventure - A Text Adventure Engine
A simple but expandable framework for creating text-based adventures
Now powered by JSON data files for easy story modification!
FIXED VERSION: Addresses item duplication, action state tracking, and other issues
"""

import json
import os
import random


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
        # NEW: Track completed actions to prevent duplication
        self.completed_actions = []  
    
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
        print(f"Actions Completed: {len(self.completed_actions)}")
    
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
    Now loads all content from JSON files and fixes loopholes!
    """
    def __init__(self):
        self.player = None
        self.game_running = True
        self.data_loader = DataLoader()
        
        # NEW: Track game state
        self.game_won = False
        self.dark_areas = ["secret_chamber"]  # Areas that need torch
        
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
        print("\n🎯 QUEST GOAL: Find all the crystals and return to unlock the final mystery!")
        
        # Show starting location
        self.describe_current_location()
        
        # Start the main game loop
        self.game_loop()
    
    def game_loop(self):
        """Main game loop - keeps the game running until player quits"""
        while self.game_running:
            # Check win condition
            if not self.game_won and self.check_win_condition():
                self.handle_victory()
            
            # Get player input
            user_input = input("\n> ").strip().lower()
            
            # Process the command
            self.process_command(user_input)
    
    def process_command(self, command):
        """Process player commands and execute appropriate actions"""
        # Expand abbreviated directions
        direction_aliases = {
            'n': 'north', 's': 'south', 'e': 'east', 'w': 'west',
            'u': 'up', 'd': 'down'
        }
        if command in direction_aliases:
            command = direction_aliases[command]
        
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
        
        # NEW: Handle "unlock [thing]" commands
        elif command.startswith("unlock "):
            thing = command[7:].strip()
            self.handle_unlock(thing)
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
            # NEW: Check if area requires torch
            if new_location in self.dark_areas and not self.player.has_item("torch"):
                print("It's too dark to go that way! You need a torch to light your way.")
                return
            
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
        
        # NEW: Check for special conditions
        if location_id == "start" and self.player.has_item("glowing_crystal") and self.player.has_item("ancient_tome"):
            print("\n✨ The room suddenly feels different. The crystal and tome are resonating with each other!")
            if "unlock door" not in [action for action in location.get("actions", {})]:
                # Add new action dynamically
                location.setdefault("actions", {})["unlock door"] = "final_unlock"
                print("🔓 You can now 'unlock door' to reveal the final secret!")
        
        # Show available exits
        exits = location.get("exits", {})
        if exits:
            print("\nYou can go:")
            for direction in exits:
                destination = self.locations.get(exits[direction], {}).get("name", exits[direction])
                print(f"  - {direction} (to {destination})")
        
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
        
        # NEW: Check if action was already completed and shouldn't be repeated
        if action_id in self.player.completed_actions:
            repeat_message = action.get("repeat_message", "You've already done that.")
            print(repeat_message)
            return
        
        # Check requirements
        requirements = action.get("requirements", [])
        for req in requirements:
            if req.get("type") == "has_item":
                required_item = req.get("item")
                if not self.player.has_item(required_item):
                    req_message = req.get("message", f"You need {required_item} to do that.")
                    print(req_message)
                    return
        
        # Show action description
        print(action.get("description", "Something happens..."))
        
        # Apply effects
        effects = action.get("effects", [])
        for effect in effects:
            self.apply_effect(effect)
        
        # NEW: Mark action as completed if it shouldn't be repeated
        if action.get("repeatable", False) == False:
            self.player.completed_actions.append(action_id)
    
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
            direction = effect.get("direction", "secret")  # NEW: Configurable direction
            if location_id and location_id in self.locations:
                # Add a new exit to current location
                current_loc = self.locations[self.player.current_location]
                if "exits" not in current_loc:
                    current_loc["exits"] = {}
                
                current_loc["exits"][direction] = location_id
                dest_name = self.locations[location_id].get("name", location_id)
                print(f"A secret passage has been revealed! You can now go '{direction}' to the {dest_name}.")
        
        # NEW: Add more effect types
        elif effect_type == "random_effect":
            self.apply_random_effect()
        
        elif effect_type == "win_game":
            self.game_won = True
    
    def apply_random_effect(self):
        """Apply a random effect from the mysterious scroll"""
        effects = [
            {"type": "heal", "amount": 15, "message": "The scroll glows and heals your wounds!"},
            {"type": "damage", "amount": 5, "message": "The scroll backfires and hurts you slightly!"},
            {"type": "teleport", "message": "The scroll teleports you to a random location!"},
            {"type": "wisdom", "message": "The scroll fills your mind with ancient wisdom!"}
        ]
        
        effect = random.choice(effects)
        print(effect["message"])
        
        if effect["type"] == "heal":
            self.player.heal(effect["amount"])
        elif effect["type"] == "damage":
            self.player.health = max(1, self.player.health - effect["amount"])
            print(f"You now have {self.player.health} health.")
        elif effect["type"] == "teleport":
            # Teleport to a random discovered location
            if self.player.discovered_locations:
                new_loc = random.choice(self.player.discovered_locations)
                self.player.current_location = new_loc
                print(f"You find yourself back at the {self.locations[new_loc]['name']}!")
                self.describe_current_location()
    
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
        
        # NEW: Handle specific item usage
        if item_id == "rusty_key":
            print("You hold up the rusty key. It seems to be meant for a special door...")
            print("Try using 'unlock door' when you find the right door!")
            return
        
        elif item_id == "torch":
            if self.player.current_location in self.dark_areas:
                print("You raise the torch high, its flickering light pushing back the darkness!")
                print("The shadows retreat, revealing hidden details of this mysterious place.")
            else:
                print(item.get("use_message", f"You use the {item['name']}."))
            return
        
        # Use the item normally
        print(item.get("use_message", f"You use the {item['name']}."))
        
        # Apply special effects
        special_effect = item.get("special_effect")
        if special_effect == "heal_player":
            self.player.heal(25)
        elif special_effect == "wisdom_boost":
            print("You feel more knowledgeable! Your mind expands with ancient wisdom.")
        elif special_effect == "random_effect":
            self.apply_random_effect()
        
        # Remove if consumable
        if item.get("consumable", False):
            self.player.remove_item(item_id, self.items)
    
    def handle_unlock(self, thing):
        """Handle unlock commands"""
        if thing == "door":
            if self.player.current_location == "start" and self.player.has_item("rusty_key"):
                if self.player.has_item("glowing_crystal") and self.player.has_item("ancient_tome"):
                    print("You insert the rusty key into a hidden keyhole in the wall!")
                    print("The crystal provides the energy, the tome provides the knowledge,")
                    print("and the key unlocks the final secret of this place!")
                    print("\n🎉 CONGRATULATIONS! You've solved the mystery of the ancient realm!")
                    self.game_won = True
                    self.game_running = False
                else:
                    print("The key fits a hidden keyhole, but nothing happens...")
                    print("Perhaps you need more mystical items to power this ancient magic?")
            else:
                print("You don't see any door to unlock here, or you don't have the right key.")
        else:
            print(f"You can't unlock {thing}.")
    
    def check_win_condition(self):
        """Check if the player has won the game"""
        # Win condition: Have all three major items and be in the starting room
        required_items = ["rusty_key", "glowing_crystal", "ancient_tome"]
        has_all_items = all(self.player.has_item(item) for item in required_items)
        return has_all_items and self.player.current_location == "start"
    
    def handle_victory(self):
        """Handle the victory condition"""
        if not self.game_won:  # Only trigger once
            print("\n" + "="*50)
            print("🎉 QUEST COMPLETE! 🎉")
            print("="*50)
            print("You have gathered all the mystical items!")
            print("The ancient realm recognizes you as a true adventurer.")
            print("Type 'unlock door' to reveal the final secret!")
            print("="*50)
    
    def show_help(self):
        """Display available commands to the player"""
        messages = self.story_config.get("messages", {})
        help_lines = messages.get("help_text", [
            "--- Available Commands ---",
            "Movement: north (n), south (s), east (e), west (w), up (u), down (d)",
            "Actions: examine, open, read, look around, touch, unlock",
            "Inventory: inventory (or 'i') - show your items",
            "Items: use [item name] - use an item from inventory", 
            "Stats: stats - show your character info",
            "Other: help, look (or 'l'), quit",
            "",
            "🎯 GOAL: Collect the crystal, tome, and key, then return to the start!"
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