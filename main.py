#!/usr/bin/env python3
"""
Turbo's Training Mission - A Heartwarming Pet Adventure
A special text adventure about Maxwell's mysterious intuition and Turbo's quest
Built with love for a dear friend expecting a wonderful surprise!
"""

import json
import os
import random


class Player:
    """
    Represents Turbo, the adventurous German Shepherd hybrid
    """
    def __init__(self, name="Turbo", starting_health=100):
        self.name = name
        self.health = starting_health
        self.max_health = starting_health
        self.inventory = []  # Items Turbo is carrying in his mouth or has access to
        self.current_location = None  # Current room/area
        self.discovered_locations = []  # Places Turbo has visited
        self.completed_actions = []  # Actions completed to prevent duplication
        self.quest_items_found = 0  # Track progress toward revelation
    
    def add_item(self, item_id, items_data):
        """Add an item to Turbo's inventory (carrying in mouth or nearby)"""
        if item_id in items_data:
            item = items_data[item_id]
            self.inventory.append(item_id)
            print(item.get("pickup_message", f"You found: {item['name']}"))
            
            # Check if this is a quest item for tracking progress
            if item.get("special_effect") == "quest_item":
                self.quest_items_found += 1
                print(f"\n🎾 Progress: You've found {self.quest_items_found}/3 special items!")
                
        else:
            print(f"Error: Item '{item_id}' not found in game data.")
    
    def remove_item(self, item_id, items_data):
        """Remove an item from Turbo's inventory"""
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
        """Check if Turbo has a specific item"""
        return item_id in self.inventory
    
    def show_inventory(self, items_data):
        """Display what Turbo is currently carrying"""
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
        """Display Turbo's current status"""
        print(f"\n--- {self.name}'s Status ---")
        print(f"Energy: {self.health}/{self.max_health} 🐕")
        print(f"Location: {self.current_location}")
        print(f"Items Found: {len(self.inventory)}")
        print(f"Quest Progress: {self.quest_items_found}/3 special items")
        print(f"Areas Explored: {len(self.discovered_locations)}")
        print(f"Tasks Completed: {len(self.completed_actions)}")
    
    def heal(self, amount):
        """Restore Turbo's energy"""
        old_health = self.health
        self.health = min(self.health + amount, self.max_health)
        healed = self.health - old_health
        if healed > 0:
            print(f"You feel more energetic! Restored {healed} energy points. 🐕")
        else:
            print("You're already full of energy!")


class DataLoader:
    """
    Handles loading all game data from JSON files
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
            print("🎮 Game data loaded successfully!")
            return True
        except Exception as e:
            print(f"❌ Error loading game data: {e}")
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
    Main game engine for Turbo's Training Mission
    Handles the game loop, commands, and Maxwell's mysterious guidance
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
        
        # Quick access to loaded data
        self.locations = self.data_loader.locations
        self.items = self.data_loader.items
        self.story_config = self.data_loader.story_config
    
    def start_game(self):
        """Initialize and start Turbo's adventure"""
        intro = self.story_config.get("intro_text", {})
        game_info = self.story_config.get("game_info", {})
        
        print("=" * 60)
        print(intro.get("welcome_message", "🐕 Welcome to Turbo's Training Mission! 🐕"))
        print("=" * 60)
        print(intro.get("game_description", "A mysterious adventure awaits..."))
        print()
        
        # Simple start prompt for our specific story
        input(intro.get("name_prompt", "Press Enter to begin Turbo's adventure..."))
        
        # Create Turbo with settings from JSON
        settings = self.story_config.get("game_settings", {})
        starting_health = settings.get("starting_health", 100)
        self.player = Player("Turbo", starting_health)
        self.player.max_health = settings.get("max_health", 100)
        
        # Set starting location
        starting_location = settings.get("starting_location", "living_room")
        self.player.current_location = starting_location
        
        print(f"\n🐕 You are Turbo, and something mysterious is happening...")
        print(intro.get("instruction_text", "Type 'help' for commands."))
        print("\n🎯 Follow Maxwell's guidance and discover what he's trying to show you!")
        
        # Show starting location
        self.describe_current_location()
        
        # Start the main game loop
        self.game_loop()
    
    def game_loop(self):
        """Main game loop - keeps Turbo's adventure running"""
        while self.game_running:
            # Check if we should trigger the final revelation
            if not self.revelation_triggered and self.check_revelation_condition():
                self.trigger_final_revelation()
            
            # Get player input
            user_input = input("\n🐕 > ").strip().lower()
            
            # Process the command
            self.process_command(user_input)
    
    def process_command(self, command):
        """Process Turbo's commands and execute appropriate actions"""
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
        
        # Handle special dog commands
        elif command.startswith("sniff "):
            area = command[6:].strip()
            self.handle_sniff_command(area)
            return
        
        elif command.startswith("dig "):
            location = command[4:].strip()
            self.handle_dig_command(location)
            return
        
        elif command.startswith("jump "):
            target = command[5:].strip()
            self.handle_jump_command(target)
            return
        
        # Special command to trigger final revelation when ready
        elif command == "realize" or command == "understand":
            if self.check_revelation_condition():
                self.trigger_final_revelation()
            else:
                print("You sense something important is happening, but the picture isn't complete yet...")
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
        invalid_msg = messages.get("invalid_command", "You tilt your head, confused.")
        print(invalid_msg)
    
    def move_player(self, new_location):
        """Move Turbo to a new location"""
        if new_location in self.locations:
            self.player.current_location = new_location
            
            # Add to discovered locations if not already there
            if new_location not in self.player.discovered_locations:
                self.player.discovered_locations.append(new_location)
            
            location_name = self.locations[new_location]['name']
            print(f"\n🐕 You move to the {location_name}...")
            self.describe_current_location()
        else:
            print(f"Error: Location '{new_location}' not found!")
    
    def describe_current_location(self):
        """Show the description of Turbo's current location"""
        location_id = self.player.current_location
        location = self.locations[location_id]
        
        print(f"\n--- 🏠 {location['name']} ---")
        
        # Show first visit description if available and not visited
        if not location.get("visited", False) and "first_visit_description" in location:
            print(location["first_visit_description"])
        else:
            print(location["description"])
        
        # Show available exits
        exits = location.get("exits", {})
        if exits:
            print("\n🚪 You can go:")
            for direction in exits:
                destination = self.locations.get(exits[direction], {}).get("name", exits[direction])
                print(f"  - {direction} (to {destination})")
        
        # Show available actions
        actions = location.get("actions", {})
        if actions:
            print("\n🔍 You can also:")
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
        
        # Check if action was already completed and shouldn't be repeated
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
        
        # Mark action as completed if it shouldn't be repeated
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
        
        elif effect_type == "trigger_revelation":
            self.revelation_triggered = True
        
        elif effect_type == "win_game":
            self.game_won = True
            self.game_running = False
    
    def handle_sniff_command(self, area):
        """Handle sniffing commands"""
        # Map sniff commands to existing actions
        current_location = self.player.current_location
        if area == "around" or area == "":
            # Try to find a sniff action for current location
            sniff_action = f"sniff_{current_location}"
            if sniff_action in self.story_config.get("special_actions", {}):
                self.handle_special_action(sniff_action)
            else:
                print("You sniff around carefully but don't notice anything particularly interesting right now.")
        else:
            print(f"You sniff at {area}, but don't detect anything special.")
    
    def handle_dig_command(self, location):
        """Handle digging commands"""
        if "garden" in self.player.current_location or "balcony" in self.player.current_location:
            if "behind plants" in location or "rhododendron" in location or location == "here":
                self.handle_special_action("dig_behind_plants")
            else:
                print("You dig enthusiastically but don't find anything in that spot.")
        else:
            print("This doesn't seem like a good place for digging.")
    
    def handle_jump_command(self, target):
        """Handle jumping commands"""
        if "counter" in target and "kitchen" in self.player.current_location:
            self.handle_special_action("jump_kitchen_counter")
        else:
            print(f"You can't jump on {target} from here, or it's not safe to do so.")
    
    def check_revelation_condition(self):
        """Check if Turbo has found all three quest items for the revelation"""
        required_items = ["child_mtb_helmet", "child_mtb_gloves", "small_mtb_bike"]
        return all(self.player.has_item(item) for item in required_items)
    
    def trigger_final_revelation(self):
        """Trigger the final revelation scene"""
        if not self.revelation_triggered:
            print("\n" + "="*60)
            print("🎉 AMAZING REALIZATION! 🎉")
            print("="*60)
            
            print("You sit down and look at all the items you've found...")
            print("The tiny helmet... the small gloves... the miniature bike...")
            print("\nSuddenly, your tail starts wagging uncontrollably!")
            print("These aren't just random objects - they're all CHILD-SIZED!")
            print("\nMaxwell appears beside you, purring loudly, his green eyes")
            print("twinkling with satisfaction. He's been trying to tell you")
            print("something wonderful all along...")
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
            print("Thanks for playing Turbo's Training Mission!")
            print("\nType 'quit' to end the adventure.")
    
    def use_item(self, item_input):
        """Handle using items from Turbo's inventory"""
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
        
        # Handle specific item usage
        print(item.get("use_message", f"You use the {item['name']}."))
        
        # Apply special effects
        special_effect = item.get("special_effect")
        if special_effect == "final_revelation":
            if self.check_revelation_condition():
                self.trigger_final_revelation()
        
        # Remove if consumable
        if item.get("consumable", False):
            self.player.remove_item(item_id, self.items)
    
    def show_help(self):
        """Display available commands to Turbo"""
        messages = self.story_config.get("messages", {})
        help_lines = messages.get("help_text", [
            "--- Turbo's Commands ---",
            "Movement: north (n), south (s), east (e), west (w), up (u), down (d)",
            "Dog Actions: sniff around, examine [thing], dig [where], jump [where]",
            "Inventory: inventory (or 'i') - show what you're carrying",
            "Items: use [item name] - use something you've found",
            "Stats: stats - check your status",
            "Other: help, look (or 'l'), quit"
        ])
        
        for line in help_lines:
            print(line)


def main():
    """
    Main function - creates and starts Turbo's Training Mission
    """
    print("🐕 Loading Turbo's Training Mission...")
    print("🐱 Maxwell is waiting with mysterious guidance...")
    
    # Create a new game instance
    game = GameEngine()
    
    # Start the adventure
    game.start_game()


# This runs the game when the script is executed
if __name__ == "__main__":
    main()