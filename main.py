#!/usr/bin/env python3
"""
Console Dot Adventure - A Text Adventure Engine
A simple but expandable framework for creating text-based adventures
"""

class Player:
    """
    Represents the player character with basic stats and inventory
    """
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = []
        self.current_location = "start"  # Where the player currently is
    
    def add_item(self, item):
        """Add an item to the player's inventory"""
        self.inventory.append(item)
        print(f"You picked up: {item}")
    
    def remove_item(self, item):
        """Remove an item from the player's inventory"""
        if item in self.inventory:
            self.inventory.remove(item)
            print(f"You used: {item}")
            return True
        else:
            print(f"You don't have: {item}")
            return False
    
    def show_inventory(self):
        """Display the player's current inventory"""
        if self.inventory:
            print(f"\n{self.name}'s Inventory:")
            for item in self.inventory:
                print(f"  - {item}")
        else:
            print("\nYour inventory is empty.")
    
    def show_stats(self):
        """Display player's current stats"""
        print(f"\n--- {self.name}'s Stats ---")
        print(f"Health: {self.health}")
        print(f"Location: {self.current_location}")
        print(f"Items: {len(self.inventory)}")


class GameEngine:
    """
    Main game engine that handles the game loop, commands, and story flow
    """
    def __init__(self):
        self.player = None
        self.game_running = True
        self.locations = self.create_locations()
    
    def create_locations(self):
        """
        Create all the locations/rooms in the game
        Each location has a description and available actions
        """
        locations = {
            "start": {
                "description": "You find yourself in a mysterious room with dim lighting. "
                             "There's a door to the NORTH and a chest in the corner.",
                "actions": {
                    "north": "hallway",
                    "examine chest": "examine_chest",
                    "open chest": "open_chest"
                },
                "visited": False
            },
            "hallway": {
                "description": "A long, narrow hallway stretches before you. "
                             "You can go SOUTH back to where you came from, or continue EAST.",
                "actions": {
                    "south": "start",
                    "east": "library"
                },
                "visited": False
            },
            "library": {
                "description": "You're in an ancient library filled with dusty books. "
                             "There's a WEST passage back to the hallway, and stairs going UP.",
                "actions": {
                    "west": "hallway",
                    "up": "tower",
                    "read book": "read_book"
                },
                "visited": False
            },
            "tower": {
                "description": "You've climbed to the top of a tower. The view is breathtaking! "
                             "You can see the entire realm from here. Stairs lead DOWN.",
                "actions": {
                    "down": "library",
                    "look around": "tower_view"
                },
                "visited": False
            }
        }
        return locations
    
    def start_game(self):
        """Initialize the game and start the main game loop"""
        print("=" * 50)
        print("Welcome to Console.Adventure!")
        print("=" * 50)
        
        # Get player name
        player_name = input("What's your name, adventurer? ").strip()
        if not player_name:
            player_name = "Unknown Adventurer"
        
        self.player = Player(player_name)
        
        print(f"\nWelcome, {self.player.name}!")
        print("Type 'help' for available commands.")
        print("Type 'quit' to exit the game.")
        
        # Show starting location
        self.describe_current_location()
        
        # Start the main game loop
        self.game_loop()
    
    def game_loop(self):
        """
        Main game loop - keeps the game running until player quits
        """
        while self.game_running:
            # Get player input
            user_input = input("\n> ").strip().lower()
            
            # Process the command
            self.process_command(user_input)
    
    def process_command(self, command):
        """
        Process player commands and execute appropriate actions
        """
        # Basic commands that work everywhere
        if command == "quit" or command == "exit":
            print(f"Thanks for playing, {self.player.name}! See you next time!")
            self.game_running = False
            return
        
        elif command == "help":
            self.show_help()
            return
        
        elif command == "inventory" or command == "i":
            self.player.show_inventory()
            return
        
        elif command == "stats":
            self.player.show_stats()
            return
        
        elif command == "look" or command == "l":
            self.describe_current_location()
            return
        
        # Location-specific commands
        current_loc = self.locations[self.player.current_location]
        
        if command in current_loc["actions"]:
            action_result = current_loc["actions"][command]
            
            # If it's a location name, move the player
            if action_result in self.locations:
                self.move_player(action_result)
            else:
                # It's a special action
                self.handle_special_action(action_result)
        else:
            print("I don't understand that command. Type 'help' for available commands.")
    
    def move_player(self, new_location):
        """Move the player to a new location"""
        self.player.current_location = new_location
        print(f"\nYou move to the {new_location}...")
        self.describe_current_location()
    
    def describe_current_location(self):
        """Show the description of the current location"""
        current_loc = self.locations[self.player.current_location]
        
        print(f"\n--- {self.player.current_location.title()} ---")
        print(current_loc["description"])
        
        # Show available actions
        print("\nYou can:")
        for action in current_loc["actions"]:
            print(f"  - {action}")
        
        # Mark as visited
        current_loc["visited"] = True
    
    def handle_special_action(self, action):
        """Handle special actions that aren't just movement"""
        if action == "examine_chest":
            print("The chest looks old and weathered. It might contain something useful.")
        
        elif action == "open_chest":
            print("You open the chest and find a rusty key inside!")
            self.player.add_item("rusty key")
        
        elif action == "read_book":
            print("You pick up a dusty tome. The pages contain mysterious symbols...")
            print("You feel slightly wiser after reading it.")
            # Could add experience points or knowledge here
        
        elif action == "tower_view":
            print("From up here, you can see a vast forest to the east,")
            print("mountains to the north, and a shimmering lake to the south.")
            print("This view fills you with determination!")
    
    def show_help(self):
        """Display available commands to the player"""
        print("\n--- Available Commands ---")
        print("Movement: north, south, east, west, up, down")
        print("Actions: examine, open, read, look around")
        print("Inventory: inventory (or 'i') - show your items")
        print("Stats: stats - show your character info")
        print("Other: help, look (or 'l'), quit")
        print("\nTry typing the actions you see listed in each location!")


def main():
    """
    Main function - creates and starts the game
    """
    # Create a new game instance
    game = GameEngine()
    
    # Start the game
    game.start_game()


# This runs the game when the script is executed
if __name__ == "__main__":
    main()