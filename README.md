# Console.Adventure 🎮

A simple but expandable text-based adventure game engine built in Python. Navigate through mysterious locations, collect items, and uncover the secrets of your adventure!

## 🎯 Features

- **Interactive Storytelling** - Navigate through connected locations with rich descriptions
- **Inventory System** - Find and collect items throughout your journey
- **Player Stats** - Track your character's health and progress
- **Expandable Framework** - Easily add new locations, items, and game mechanics
- **Simple Commands** - Intuitive text-based interface for all players

## 🎮 How to Play

### Getting Started

1. **Download or Clone** this repository
2. **Make sure you have Python 3.6+** installed on your system
3. **Run the game:**
   ```bash
   python main.py
   ```
   or
   ```bash
   python3 main.py
   ```

### Game Commands

#### Movement
- `north`, `south`, `east`, `west` - Move between locations
- `up`, `down` - Use stairs or climb

#### Interaction
- `examine chest` - Look at objects closely
- `open chest` - Interact with containers
- `read book` - Read items in the environment
- `look around` - Get detailed views of special areas

#### System Commands
- `help` - Show all available commands
- `inventory` or `i` - View your collected items
- `stats` - Check your character information
- `look` or `l` - Re-read current location description
- `quit` or `exit` - End the game

## 🛠️ Development

This project is designed to be beginner-friendly and easily expandable!

### Project Structure

```
console-dot-adventure/
├── main.py          # Main game engine and all classes
└── README.md        # This file
```

### Key Classes

- **`Player`** - Manages character stats, inventory, and current location
- **`GameEngine`** - Handles game loop, commands, and location management

### Adding New Content

Want to expand the game? Here are some easy modifications:

#### Add New Locations
```python
# In the create_locations() method, add:
"new_location": {
    "description": "Your location description here...",
    "actions": {
        "direction": "connected_location",
        "special_action": "custom_action"
    },
    "visited": False
}
```

#### Add New Items
```python
# In any special action:
self.player.add_item("new_item_name")
```

#### Add New Special Actions
```python
# In the handle_special_action() method:
elif action == "your_action":
    print("What happens when player does this action")
```

## 🎯 Future Enhancement Ideas

- **Combat System** - Add enemies and battle mechanics
- **Character Classes** - Warrior, Mage, Thief with different abilities
- **Save/Load System** - Allow players to save their progress
- **Puzzle System** - Add riddles and brain teasers
- **Magic System** - Spells and magical items
- **Quest System** - Structured objectives and rewards
- **Multiple Endings** - Different story outcomes based on choices

## 🐍 Requirements

- **Python 3.6 or higher**
- No external libraries required - uses only Python standard library!

## 🚀 Running in Different Environments

### Local Computer
```bash
python main.py
```

### GitHub Codespaces
1. Open repository in Codespaces
2. Open terminal
3. Run `python main.py`

### Online Python Environments
Works in Repl.it, Trinket, or any online Python interpreter!

## 🤝 Contributing

This is a learning project, but feel free to:
- Fork the repository
- Add new features
- Submit pull requests
- Share your own story adaptations

## 📝 License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).

---

**Happy adventuring!** 🗡️✨

*Built with ❤️ and lots of `console.log()` jokes*