# 🐕 Turbo's Quest 🐱

A heartwarming text adventure about Maxwell's mysterious intuition and Turbo's quest to discover a wonderful family secret!

## 🎯 The Story

You are **Turbo**, an energetic German Shepherd living in a cozy apartment with your family. Your cat companion **Maxwell** has been acting very strangely lately - staring at empty spaces, sitting in unusual spots, and giving you meaningful looks. 

Maxwell's feline intuition has sensed something important coming to the family, and he's mysteriously guiding you to find three special items hidden around your home. Follow his clues and discover what he's trying to tell you!

## 🎮 How to Play

### Getting Started

1. **Make sure you have Python 3.6+** installed
2. **Create the data folder structure:**
   ```
   turbo-adventure/
   ├── main.py
   ├── README.md
   └── data/
       ├── locations.json
       ├── items.json
       └── story.json
   ```
3. **Run the game:**
   ```bash
   python main.py
   ```

### Game Commands

#### Movement
- Use location names directly: `kitchen`, `bedroom`, `garden`, `balcony`, etc.

#### Dog Actions 🐕
- `examine [thing]` - Look at objects, Maxwell, or areas closely
- `follow maxwell` - Follow Maxwell's guidance
- `dig here` - Dig in the garden when Maxwell shows you where
- `jump on counter` - Jump onto surfaces (when you have the right tools)
- `open [container]` - Open cabinets, sheds, or containers

#### System Commands
- `help` - Show all available commands
- `inventory` or `i` - View items you're carrying
- `stats` - Check Turbo's status and progress
- `look` or `l` - Re-examine your current location
- `examine all items` - **Special command to understand quest items together**
- `quit` or `exit` - End the game

## 🗺️ Locations

Explore Turbo's familiar home environment:
- **Living Room** - Where Maxwell first gives you mysterious guidance
- **Kitchen** - High cabinets and hidden tools await
- **Bedroom** - Secrets under beds and in closets
- **Balcony** - Outdoor views and garden access
- **Garden** - Digging spots and a tool shed
- **Tool Shed** - Where important discoveries await

## 🎾 Quest Items

Maxwell is guiding you to find three special items:
1. **A colorful helmet** (hidden in high places)
2. **Gloves** (buried treasures)
3. **A special bike** (locked away safely)

## 💡 Tips for Success

- **Follow Maxwell's guidance** - Pay attention to where he sits and stares
- **Use your dog abilities** - Digging and exploring are your superpowers
- **Explore thoroughly** - Check every room and examine everything
- **Collect helpful tools** - Some items help you reach or unlock other areas
- **Examine all items together** - When you have all three quest items, use this special command to understand their significance
- **Trust the process** - Maxwell's mysterious behavior has a wonderful purpose

## 🎯 The Mystery

As you gather the items Maxwell wants you to find, you'll start to notice something special about them. The game has two revelation moments:

1. **Size Realization** - Understanding what these items have in common
2. **Final Revelation** - Discovering the wonderful family secret!

Trust in Maxwell's feline intuition - he knows something wonderful that he's trying to share with you!

## 📝 What's Changed in the Cleaned Version

### Removed (Never Used):
- **Health/combat system** - Turbo never gets hurt or fights
- **Item values** - No buying/selling in this game
- **Consumable item logic** - Items don't get used up
- **Magic/combat settings** - Not needed for this story
- **Unused special effects** - Like "comfort_item", "soft_tool"
- **Redundant error messages** - Simplified error handling

### Kept (Actually Used):
- **Quest item tracking** - Essential for the story progression
- **Size realization system** - Key story mechanic
- **Location visiting tracking** - For first-visit descriptions
- **Action completion tracking** - Prevents repeated actions
- **Item requirements** - For actions like using the step stool

### Benefits of Cleanup:
- **Faster loading** - Less unused code to process
- **Easier to understand** - No confusing unused features
- **Simpler to modify** - Less complexity for future changes
- **Better performance** - Removed unnecessary checks and calculations

## 📝 Technical Details

- **Built with Python 3.6+**
- **JSON-driven story system** - Easy to modify and expand
- **No external dependencies** - Uses only Python standard library
- **Beginner-friendly code** - Well-commented for learning
- **Cleaned and optimized** - Removed all unused features

---

**Happy adventuring, and trust in Maxwell's wisdom!** 🐕✨🐱

*Sometimes our pets know things before we do...*