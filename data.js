// Game data converted from JSON files for web version
const gameData = {
    locations: {
        "living_room": {
            "name": "Living Room",
            "description": "You're in the cozy living room where sunlight streams through the windows. Maxwell sits by the window, staring intently at something only he can see. His tail twitches with purpose - he definitely wants you to follow him somewhere.",
            "first_visit_description": "You wake up from your afternoon nap to find Maxwell behaving very strangely. The black and brown cat with white paws and chest is sitting perfectly still by the large window, his yellow eyes focused on... nothing you can see. But his ears are perked forward and his tail does that slow, meaningful twitch that says 'I know something important.' The living room feels charged with anticipation.",
            "exits": {
                "kitchen": "kitchen",
                "bedroom": "bedroom"
            },
            "actions": {
                "follow maxwell's gaze": "maxwell_leads_to_kitchen",
                "examine window": "examine_living_window",
                "examine dog bed": "examine_dog_bed"
            },
            "items": [],
            "visited": false
        },
        "kitchen": {
            "name": "Kitchen",
            "description": "The kitchen smells of kibble and treats. Maxwell sits boldly on the forbidden counter (which he never does!), staring up at a high cabinet with laser focus. He looks at you, then at the cabinet, then back at you. His message is clear: 'Something important is up there.'",
            "first_visit_description": "You follow Maxwell into the kitchen, your claws clicking on the tile floor. The room carries the familiar scents of home, but Maxwell is acting completely out of character - sitting on the counter he's never allowed on! His yellow eyes are fixed on one particular high cabinet with unwavering intensity.",
            "exits": {
                "living room": "living_room",
                "balcony": "balcony"
            },
            "actions": {
                "get step stool": "get_step_stool_action",
                "jump on counter": "jump_kitchen_counter",
                "examine cabinet": "examine_high_cabinet"
            },
            "items": [],
            "visited": false
        },
        "bedroom": {
            "name": "Bedroom",
            "description": "The humans' quiet bedroom has a big bed and a closet. Maxwell emerges from under the bed with dusty whiskers, then sits next to it and pats the floor with his paw. He's found something under there that needs your help to retrieve.",
            "first_visit_description": "You enter the peaceful bedroom where your humans sleep. Maxwell appears from under the bed, a dusty whisker showing he's been exploring tight spaces. He looks at you meaningfully, then pats the floor next to the bed with his paw.",
            "exits": {
                "living room": "living_room"
            },
            "actions": {
                "look under bed": "examine_under_bed"
            },
            "items": [],
            "visited": false
        },
        "balcony": {
            "name": "Balcony",
            "description": "The small balcony overlooks the garden below. Plant pots and a storage box sit along the railing. Maxwell perches by the edge like a furry sentinel, staring down at something specific in the garden with complete focus.",
            "first_visit_description": "You step onto the balcony and breathe in the fresh outdoor air. The view of the garden below is spectacular, full of interesting scents. Maxwell sits by the railing like a statue, his gaze locked on one particular spot in the garden below.",
            "exits": {
                "kitchen": "kitchen",
                "garden": "garden"
            },
            "actions": {
                "examine storage box": "examine_balcony_box",
                "look at garden": "examine_garden_from_balcony"
            },
            "items": [],
            "visited": false
        },
        "garden": {
            "name": "Garden",
            "description": "Your favorite outdoor space! The garden has flower beds, a tool shed, and plenty of interesting scents. Maxwell appears from behind a large rhododendron bush, his usually pristine paws now dirty with soil. He sits precisely at a spot where the earth looks recently disturbed.",
            "first_visit_description": "You enter the garden, your outdoor paradise! The grass feels soft under your paws and every direction offers new adventures. Maxwell emerges from behind a large rhododendron, his paws uncharacteristically dirty, giving you a look that clearly says 'dig here!'",
            "exits": {
                "balcony": "balcony",
                "tool shed": "tool_shed"
            },
            "actions": {
                "dig here": "dig_behind_plants",
                "follow maxwell's gaze": "dig_behind_plants",
                "examine shed": "examine_garden_shed"
            },
            "items": [],
            "visited": false
        },
        "tool_shed": {
            "name": "Tool Shed",
            "description": "The small garden shed contains tools, plant pots, and storage. There's something special here that Maxwell has been leading you toward - something that will complete your understanding of his mysterious quest.",
            "first_visit_description": "You approach the small tool shed in the corner of the garden. The wooden structure stores garden tools and supplies, but Maxwell's behavior suggests there's something much more important here than just gardening equipment.",
            "exits": {
                "garden": "garden"
            },
            "actions": {
                "unlock shed": "unlock_garden_shed",
                "examine inside": "examine_shed_contents"
            },
            "items": [],
            "visited": false
        }
    },

    items: {
        "child_mtb_helmet": {
            "name": "Colorful Helmet",
            "description": "A mountain bike helmet with bright colors and fun stickers. It has soft padding inside and looks protective and well-made. The design suggests it's meant for someone who loves adventure.",
            "pickup_message": "You carefully retrieve the helmet. It's surprisingly light and smells new. Something about it makes you feel protective and excited at the same time.",
            "use_message": "You gently set down the helmet. Its bright colors gleam in the light, and you can't help but wag your tail looking at it.",
            "special_effect": "quest_item"
        },
        "child_mtb_gloves": {
            "name": "Mountain Bike Gloves",
            "description": "A pair of mountain biking gloves with protective padding on the palms. The bright colors and fun patterns suggest they're designed for someone who loves adventure and outdoor activities.",
            "pickup_message": "You delicately pick up the gloves with your teeth. They smell like new fabric and exciting possibilities.",
            "use_message": "You place the gloves carefully on the ground. Looking at them, you can tell they're well-made and ready for adventure.",
            "special_effect": "quest_item"
        },
        "small_mtb_bike": {
            "name": "Balance Bike",
            "description": "A beautiful balance bike with bright and cheerful colors. It's perfectly proportioned and looks ready for adventure. The sight of it fills you with excitement and anticipation.",
            "pickup_message": "This bike is too big to carry in your mouth, but you can push it with your nose. As you examine it closely, your heart starts racing with excitement. There's something very special about this bike...",
            "use_message": "You sit next to the bike, and suddenly you feel like all the pieces are starting to come together. This bike represents something wonderful that's coming to your family!",
            "special_effect": "quest_item"
        },
        "garden_key": {
            "name": "Small Garden Key",
            "description": "A small brass key that smells like metal and earth. It looks like it might open something in the garden area - perhaps the tool shed where something important is waiting.",
            "pickup_message": "You carefully pick up the small key with your teeth. The metal feels cool and important.",
            "use_message": "You drop the key with a small metallic clink. It's clearly meant to unlock something special."
        },
        "step_stool": {
            "name": "Small Step Stool",
            "description": "A wooden step stool that the humans sometimes use to reach high places. Perfect for a determined dog who needs to get to higher shelves or cabinets that might contain important discoveries.",
            "pickup_message": "You grab the step stool by its edge and start dragging it across the floor. It's heavier than expected but manageable for a strong dog like you.",
            "use_message": "You position the step stool carefully. Now you should be able to reach places that were too high before!"
        }
    },

    story: {
        "game_info": {
            "title": "Turbo's Quest",
            "version": "1.3",
            "author": "Made with Love for a Special Friend",
            "description": "A heartwarming adventure about Maxwell's mysterious intuition and Turbo's quest to prepare for something wonderful - cleaned up version!"
        },
        "game_settings": {
            "starting_location": "living_room"
        },
        "intro_text": {
            "welcome_message": "🐕 Welcome to Turbo's Quest! 🐕",
            "game_description": "You are Turbo, an energetic German Shepherd living in a cozy apartment with your family. Your cat companion Maxwell has been acting very strangely lately - staring at empty spaces and giving you meaningful looks. Something important is happening, and Maxwell seems to know what it is. Trust his guidance to discover what he's trying to show you!",
            "instruction_text": "Maxwell will guide you through your adventure. Follow his lead and trust his mysterious cat intuition!",
            "name_prompt": "Press Enter to begin Turbo's adventure..."
        },
        "special_actions": {
            "maxwell_leads_to_kitchen": {
                "description": "Maxwell stands up, stretches, and walks purposefully toward the kitchen. He pauses at the doorway and looks back at you with those intense yellow eyes, clearly wanting you to follow. His tail swishes once - a definite 'come on!' signal.",
                "repeatable": true,
                "repeat_message": "Maxwell continues to look toward the kitchen meaningfully. He definitely wants you to go there."
            },
            "examine_living_window": {
                "description": "You put your paws on the windowsill and look outside. The view shows the garden below and neighborhood beyond, but you can't see what Maxwell is focusing on. His cat intuition must be detecting something your eyes can't see.",
                "repeatable": true,
                "repeat_message": "The window shows the same peaceful view, but Maxwell's behavior suggests something more is happening."
            },
            "examine_dog_bed": {
                "description": "Your comfortable dog bed sits in its usual corner, but today something's different. Maxwell has left a single cat treat on your pillow - definitely not normal behavior! He's trying to tell you something important. His message is clear: this quest is about something special coming to your family.",
                "repeatable": false,
                "repeat_message": "Your dog bed looks normal now. Maxwell's message has been received."
            },
            "examine_high_cabinet": {
                "description": "The cabinet is way above your head with a simple latch. You can smell something interesting inside - new plastic and fabric. Maxwell's intense stare tells you this is definitely important, but you need to find a way to reach it.",
                "repeatable": true,
                "repeat_message": "The cabinet remains out of reach, but you know something important is inside."
            },
            "get_step_stool_action": {
                "description": "You nose open the lower cabinet and find a wooden step stool inside! Perfect for reaching high places. You grab it by the edge and drag it out across the kitchen floor. Maxwell watches approvingly - this is exactly what you need.",
                "effects": [
                    {"type": "give_item", "item": "step_stool"}
                ],
                "repeatable": false,
                "repeat_message": "You've already gotten the step stool from this cabinet."
            },
            "jump_kitchen_counter": {
                "description": "Using the step stool, you leap onto the counter (definitely not allowed!). From up here, you can reach the high cabinet. Maxwell purrs approvingly and rubs against you briefly. With careful nose work, you manage to open the latch and discover a colorful helmet inside! It looks well-made and sturdy, with bright colors and fun patterns.",
                "requirements": [
                    {"type": "has_item", "item": "step_stool", "message": "You need the step stool to reach the counter safely."}
                ],
                "effects": [
                    {"type": "give_item", "item": "child_mtb_helmet"}
                ],
                "repeatable": false,
                "repeat_message": "You've already found the helmet from the high cabinet."
            },
            "examine_under_bed": {
                "description": "You squeeze under the bed and peer into the dusty space. Maxwell sits at the edge, watching you explore. There's nothing hidden here, but Maxwell's guidance led you to check - perhaps he wanted you to be thorough in your search. His mysterious quest continues.",
                "repeatable": false,
                "repeat_message": "You've already searched thoroughly under the bed."
            },
            "examine_balcony_box": {
                "description": "The storage box contains garden tools - a small trowel, fertilizer, and watering supplies. But tucked underneath, you spot something metallic glinting in the sunlight. It's a small key that looks like it might unlock something important!",
                "effects": [
                    {"type": "give_item", "item": "garden_key"}
                ],
                "repeatable": false,
                "repeat_message": "The storage box now only contains the usual garden tools."
            },
            "examine_garden_from_balcony": {
                "description": "From the balcony, you have a perfect view of the garden below. Following Maxwell's gaze, you spot a specific area near the large rhododendron bush where the soil looks disturbed. Something is definitely buried there!",
                "repeatable": true,
                "repeat_message": "The disturbed soil near the rhododendron continues to catch your attention."
            },
            "dig_behind_plants": {
                "description": "You start digging enthusiastically at the exact spot Maxwell indicated. The soil gives way easily under your paws. About six inches down, you hit something soft and fabric-like. Carefully extracting it with your teeth, you uncover a pair of brightly colored gloves! They have protective padding and look designed for outdoor activities.",
                "effects": [
                    {"type": "give_item", "item": "child_mtb_gloves"}
                ],
                "repeatable": false,
                "repeat_message": "You've already found the treasure that was buried here."
            },
            "examine_garden_shed": {
                "description": "The tool shed sits in the corner, its door secured with a simple lock. Through gaps in the wooden walls, you can see garden tools and storage boxes. Maxwell keeps glancing at it meaningfully - there's definitely something important inside.",
                "repeatable": true,
                "repeat_message": "The shed continues to seem important, waiting for the right key."
            },
            "unlock_garden_shed": {
                "description": "You use the small garden key to unlock the tool shed. The door creaks open, revealing garden tools and storage boxes. But in the back corner, covered by an old blanket, you discover something amazing: a beautiful balance bike with bright and cheerful colors! It's perfectly made and looks ready for adventure.",
                "requirements": [
                    {"type": "has_item", "item": "garden_key", "message": "You need the key to unlock this shed."}
                ],
                "effects": [
                    {"type": "give_item", "item": "small_mtb_bike"},
                    {"type": "trigger_revelation"}
                ],
                "repeatable": false,
                "repeat_message": "The shed is now open, its wonderful secret revealed."
            },
            "examine_shed_contents": {
                "description": "Looking inside the unlocked shed, you see garden tools and storage boxes neatly arranged. Now that you've found the bike, this is just a normal storage space again. Maxwell's attention has moved on to more important things.",
                "requirements": [
                    {"type": "has_item", "item": "small_mtb_bike", "message": "The shed is still locked."}
                ],
                "repeatable": true,
                "repeat_message": "The shed contains the usual garden supplies. The real treasure has already been found."
            }
        },
        "messages": {
            "help_text": [
                "--- Turbo's Commands ---",
                "Movement: Use location names (kitchen, bedroom, garden, etc.)",
                "Actions: The most important actions are shown in each location",
                "Inventory: 'inventory' or 'i' - see what you're carrying",
                "Other: 'help', 'look', 'stats', 'quit'",
                "",
                "🎯 QUEST: Follow Maxwell's guidance through two phases!",
                "",
                "📋 PHASE 1: Collect three special items (helmet, gloves, bike)",
                "📋 PHASE 2: Understand what these items mean for your family",
                "",
                "🧠 Key Commands:",
                "- 'examine all items' - Compare your quest items together",
                "- This unlocks Phase 2 of Maxwell's quest!",
                "",
                "💡 Tips:",
                "- Trust Maxwell's instincts - he always has a reason",
                "- Look for items that can help you reach or unlock things",
                "- The quest has clear phases with helpful progress indicators",
                "- Pay attention to quest status messages for guidance!"
            ],
            "invalid_command": "You tilt your head, confused. Try 'help' to see what you can do, or just follow Maxwell's lead!",
            "exit_message": "Thanks for playing Turbo's Quest! 🐕 You've discovered Maxwell's wonderful secret - a new little family member is coming soon! 🎉"
        }
    }
};