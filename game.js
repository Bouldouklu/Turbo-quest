// Turbo's Quest - JavaScript Web Version
class Player {
    constructor(name = "Turbo") {
        this.name = name;
        this.inventory = [];
        this.currentLocation = null;
        this.discoveredLocations = [];
        this.completedActions = [];
        this.questItemsFound = 0;
        this.sizeRealizationTriggered = false;
    }

    addItem(itemId, itemsData) {
        if (itemId in itemsData) {
            const item = itemsData[itemId];
            this.inventory.push(itemId);
            this.displayMessage(item.pickup_message || `You found: ${item.name}`);
            
            if (item.special_effect === "quest_item") {
                this.questItemsFound++;
                this.displayMessage(`\n🎾 Progress: You've found ${this.questItemsFound}/3 special items!`);
                
                if (this.questItemsFound === 1) {
                    this.displayMessage("Maxwell purrs softly. You're on the right track!");
                } else if (this.questItemsFound === 2) {
                    this.displayMessage("Maxwell's tail swishes with excitement. One more to go!");
                } else if (this.questItemsFound === 3) {
                    this.displayMessage("Maxwell's eyes are bright with anticipation. You have all the pieces now...");
                    this.displayMessage("💡 Try using 'examine all items' to understand what you've collected!");
                }
            }
        } else {
            this.displayMessage(`Error: Item '${itemId}' not found in game data.`);
        }
        this.updateUI();
    }

    hasItem(itemId) {
        return this.inventory.includes(itemId);
    }

    showInventory(itemsData) {
        if (this.inventory.length > 0) {
            this.displayMessage(`\n🎾 ${this.name}'s Current Items:`);
            for (let itemId of this.inventory) {
                if (itemId in itemsData) {
                    const item = itemsData[itemId];
                    this.displayMessage(`  - ${item.name}: ${item.description}`);
                } else {
                    this.displayMessage(`  - ${itemId} (unknown item)`);
                }
            }
        } else {
            this.displayMessage(`\n${this.name} isn't carrying anything right now.`);
        }
    }

    showStats() {
        this.displayMessage(`\n--- ${this.name}'s Status ---`);
        this.displayMessage(`Location: ${this.currentLocation}`);
        this.displayMessage(`Items Found: ${this.inventory.length}`);
        this.displayMessage(`Quest Progress: ${this.questItemsFound}/3 special items`);
        if (this.sizeRealizationTriggered) {
            this.displayMessage("🧠 Understanding: You've realized something important about these items!");
        }
        this.displayMessage(`Areas Explored: ${this.discoveredLocations.length}`);
    }

    displayMessage(message) {
        const output = document.getElementById('gameOutput');
        const div = document.createElement('div');
        div.innerHTML = message.replace(/\n/g, '<br>');
        output.appendChild(div);
        output.scrollTop = output.scrollHeight;
    }

    updateUI() {
        document.getElementById('currentLocation').textContent = 
            gameData.locations[this.currentLocation]?.name || this.currentLocation;
        document.getElementById('itemCount').textContent = this.inventory.length;
        
        let questStatus = "Starting...";
        if (this.questItemsFound > 0) {
            if (!this.sizeRealizationTriggered) {
                questStatus = `Phase 1: ${this.questItemsFound}/3 special items found`;
            } else if (!game.revelationTriggered) {
                questStatus = "Phase 2: Understanding achieved, final revelation pending";
            } else {
                questStatus = "Quest Complete: Maxwell's wonderful secret revealed!";
            }
        }
        document.getElementById('questStatus').textContent = questStatus;
    }
}

class GameEngine {
    constructor() {
        this.player = null;
        this.gameRunning = true;
        this.locations = gameData.locations;
        this.items = gameData.items;
        this.story = gameData.story;
        this.gameWon = false;
        this.revelationTriggered = false;
        
        this.setupEventListeners();
    }

    setupEventListeners() {
        const input = document.getElementById('gameInput');
        const submitBtn = document.getElementById('submitBtn');
        
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.processInput();
            }
        });
        
        submitBtn.addEventListener('click', () => {
            this.processInput();
        });

        document.getElementById('helpBtn').addEventListener('click', () => {
            this.showHelp();
        });

        document.getElementById('inventoryBtn').addEventListener('click', () => {
            this.player.showInventory(this.items);
        });

        document.getElementById('lookBtn').addEventListener('click', () => {
            this.describeCurrentLocation();
        });

        document.getElementById('statsBtn').addEventListener('click', () => {
            this.player.showStats();
        });
    }

    startGame() {
        const intro = this.story.intro_text;
        
        this.player = new Player("Turbo");
        this.player.displayMessage("=" + "=".repeat(60));
        this.player.displayMessage(intro.welcome_message);
        this.player.displayMessage("=" + "=".repeat(60));
        this.player.displayMessage(intro.game_description);
        this.player.displayMessage("");
        this.player.displayMessage("🐕 You are Turbo, and something mysterious is happening...");
        this.player.displayMessage(intro.instruction_text);
        this.player.displayMessage("\n🎯 Trust Maxwell's cat intuition to discover his wonderful secret!");
        
        const startingLocation = this.story.game_settings.starting_location;
        this.player.currentLocation = startingLocation;
        
        this.describeCurrentLocation();
        this.player.updateUI();
    }

    processInput() {
        const input = document.getElementById('gameInput');
        const command = input.value.trim().toLowerCase();
        input.value = '';
        
        if (!command) return;

        this.player.displayMessage(`\n🐕 > ${command}`);
        this.processCommand(command);
    }

    processCommand(command) {
        let showLocationAfter = true;

        if (command === "quit" || command === "exit") {
            const exitMsg = this.story.messages.exit_message;
            this.player.displayMessage(exitMsg);
            this.gameRunning = false;
            return;
        } else if (command === "help") {
            this.showHelp();
            showLocationAfter = false;
        } else if (command === "inventory" || command === "i") {
            this.player.showInventory(this.items);
            showLocationAfter = false;
        } else if (command === "stats") {
            this.player.showStats();
            showLocationAfter = false;
        } else if (command === "look" || command === "l") {
            this.describeCurrentLocation();
            showLocationAfter = false;
        } else if (command === "examine all items" || command === "examine items" || 
                   command === "compare items" || command === "look at all items") {
            this.examineAllQuestItems();
        } else if (this.handleMovementCommand(command)) {
            showLocationAfter = false;
        } else if (this.handleLocationAction(command)) {
            // Action handled
        } else {
            const invalidMsg = this.story.messages.invalid_command;
            this.player.displayMessage(invalidMsg);
            showLocationAfter = false;
            this.showCurrentOptions();
        }

        if (showLocationAfter && this.gameRunning) {
            this.showQuickLocationReminder();
        }

        // Check for final revelation
        if (!this.revelationTriggered && 
            this.player.sizeRealizationTriggered && 
            this.checkAllItemsCollected()) {
            this.triggerFinalRevelation();
        }
    }

    handleMovementCommand(command) {
        const currentLoc = this.locations[this.player.currentLocation];
        const exits = currentLoc.exits || {};
        
        for (let [exitKey, destination] of Object.entries(exits)) {
            if (command === exitKey || command === destination) {
                this.movePlayer(destination);
                return true;
            }
        }
        return false;
    }

    handleLocationAction(command) {
        const currentLoc = this.locations[this.player.currentLocation];
        const actions = currentLoc.actions || {};
        
        if (command in actions) {
            const actionId = actions[command];
            this.handleSpecialAction(actionId);
            return true;
        }
        return false;
    }

    movePlayer(newLocation) {
        if (newLocation in this.locations) {
            this.player.currentLocation = newLocation;
            
            if (!this.player.discoveredLocations.includes(newLocation)) {
                this.player.discoveredLocations.push(newLocation);
            }
            
            const locationName = this.locations[newLocation].name;
            this.player.displayMessage(`\n🐕 You move to the ${locationName}...`);
            this.describeCurrentLocation();
            this.player.updateUI();
        } else {
            this.player.displayMessage(`Error: Location '${newLocation}' not found!`);
        }
    }

    describeCurrentLocation() {
        const locationId = this.player.currentLocation;
        const location = this.locations[locationId];
        
        this.player.displayMessage(`\n--- 🏠 ${location.name} ---`);
        
        if (!location.visited && location.first_visit_description) {
            this.player.displayMessage(location.first_visit_description);
        } else {
            this.player.displayMessage(location.description);
        }
        
        const actions = location.actions || {};
        if (Object.keys(actions).length > 0) {
            this.player.displayMessage("\n🎯 You can:");
            for (let action of Object.keys(actions)) {
                this.player.displayMessage(`  - ${action}`);
            }
        }
        
        const exits = location.exits || {};
        if (Object.keys(exits).length > 0) {
            this.player.displayMessage("\n🚪 You can go to:");
            for (let direction of Object.keys(exits)) {
                this.player.displayMessage(`  - ${direction}`);
            }
        }
        
        // Quest progress hints
        if (this.checkAllItemsCollected() && !this.player.sizeRealizationTriggered) {
            this.player.displayMessage("\n🎯 QUEST PHASE 1: You have all three special items!");
            this.player.displayMessage("💭 Try 'examine all items' to understand their significance.");
        } else if (this.player.sizeRealizationTriggered && !this.revelationTriggered) {
            this.player.displayMessage("\n🎯 QUEST PHASE 2: Maxwell's final revelation awaits!");
            this.player.displayMessage("💫 Continue exploring to discover the wonderful truth!");
        }
        
        location.visited = true;
    }

    handleSpecialAction(actionId) {
        const specialActions = this.story.special_actions;
        
        if (!(actionId in specialActions)) {
            this.player.displayMessage(`Error: Action '${actionId}' not found!`);
            return;
        }
        
        const action = specialActions[actionId];
        
        if (this.player.completedActions.includes(actionId)) {
            const repeatMessage = action.repeat_message || "You've already done that.";
            this.player.displayMessage(repeatMessage);
            return;
        }
        
        const requirements = action.requirements || [];
        for (let req of requirements) {
            if (req.type === "has_item") {
                const requiredItem = req.item;
                if (!this.player.hasItem(requiredItem)) {
                    const reqMessage = req.message || `You need ${requiredItem} to do that.`;
                    this.player.displayMessage(reqMessage);
                    return;
                }
            }
        }
        
        this.player.displayMessage(action.description || "Something happens...");
        
        const effects = action.effects || [];
        for (let effect of effects) {
            this.applyEffect(effect);
        }
        
        if (action.repeatable === false) {
            this.player.completedActions.push(actionId);
        }
    }

    applyEffect(effect) {
        const effectType = effect.type;
        
        if (effectType === "give_item") {
            const itemId = effect.item;
            if (itemId) {
                this.player.addItem(itemId, this.items);
            }
        } else if (effectType === "trigger_revelation") {
            if (this.player.sizeRealizationTriggered) {
                this.revelationTriggered = true;
            } else {
                this.player.displayMessage("You sense that Maxwell's quest is almost complete...");
                this.player.displayMessage("But you feel like you need to understand something about these items first.");
            }
        } else if (effectType === "win_game") {
            this.gameWon = true;
            this.gameRunning = false;
        }
    }

    examineAllQuestItems() {
        const questItems = ["child_mtb_helmet", "child_mtb_gloves", "small_mtb_bike"];
        
        if (!questItems.every(item => this.player.hasItem(item))) {
            this.player.displayMessage("You don't have all the special items yet to compare them properly.");
            this.player.displayMessage("Keep following Maxwell's guidance!");
            return;
        }
        
        if (this.player.sizeRealizationTriggered) {
            this.player.displayMessage("You look at the three items together again:");
            this.player.displayMessage("The colorful helmet, the adventure gloves, and the beautiful bike.");
            this.player.displayMessage("Now you understand - they're all designed for someone special...");
            this.player.displayMessage("Maxwell's plan is becoming clearer!");
            return;
        }
        
        this.player.displayMessage("\n" + "=".repeat(50));
        this.player.displayMessage("🧠 MOMENT OF UNDERSTANDING 🧠");
        this.player.displayMessage("=".repeat(50));
        
        this.player.displayMessage("\nYou gather all three special items together and examine them carefully...");
        this.player.displayMessage("The colorful helmet with its protective padding...");
        this.player.displayMessage("The adventure gloves with their sturdy grip...");
        this.player.displayMessage("The beautiful bike, perfectly crafted and ready for fun...");
        this.player.displayMessage("\nYou tilt your head as you study each item more closely.");
        this.player.displayMessage("Wait a minute... something's becoming clear about these items...");
        this.player.displayMessage("\nAs you look at them all together, a pattern emerges.");
        this.player.displayMessage("They're not just random adventure gear...");
        this.player.displayMessage("They all seem to be made for the same person!");
        this.player.displayMessage("But who in your family would need ALL of these things?");
        this.player.displayMessage("\nYour ears perk up with growing excitement...");
        this.player.displayMessage("These items aren't meant for any of the adult humans you know...");
        this.player.displayMessage("They're all perfectly sized for someone much smaller!");
        this.player.displayMessage("Someone who doesn't live in your house yet...");
        this.player.displayMessage("\nYour tail starts wagging as understanding dawns.");
        this.player.displayMessage("Maxwell appears beside you, purring softly, his eyes twinkling");
        this.player.displayMessage("with approval. You're getting closer to understanding his secret!");
        
        this.player.displayMessage("\n💡 You're starting to understand Maxwell's mysterious quest!");
        this.player.displayMessage("But there's still one more piece to the puzzle...");
        this.player.displayMessage("What does this all MEAN for your family?");
        this.player.displayMessage("=".repeat(50));
        
        this.player.sizeRealizationTriggered = true;
        
        this.player.displayMessage("\n🎯 QUEST PROGRESS: You've unlocked the next phase!");
        this.player.displayMessage("💭 Now that you understand these items have a special purpose,");
        this.player.displayMessage("   you need to discover WHY Maxwell wanted you to find them.");
        this.player.displayMessage("\n🎮 NEXT STEP: Visit any location or use 'look' to trigger Maxwell's");
        this.player.displayMessage("   final revelation about what these items really mean!");
        
        this.player.updateUI();
    }

    triggerFinalRevelation() {
        if (!this.revelationTriggered) {
            this.player.displayMessage("\n" + "=".repeat(60));
            this.player.displayMessage("🎉 THE WONDERFUL REVELATION! 🎉");
            this.player.displayMessage("=".repeat(60));
            
            this.player.displayMessage("\nMaxwell's mysterious behavior suddenly makes perfect sense!");
            this.player.displayMessage("You sit quietly, thinking about the special items...");
            this.player.displayMessage("Helmet... gloves... bike... all perfectly sized for someone small...");
            this.player.displayMessage("\nSuddenly, your tail starts wagging uncontrollably!");
            this.player.displayMessage("\n🍼 A NEW LITTLE FAMILY MEMBER IS COMING! 🍼");
            this.player.displayMessage("\nA tiny human who will grow up to use these adventure items!");
            this.player.displayMessage("\nMaxwell appears beside you, purring loudly.");
            this.player.displayMessage("His feline intuition knew this wonderful secret all along!");
            this.player.displayMessage("\nYou spin in a happy circle, barking with joy!");
            this.player.displayMessage("A new baby is coming to your family!");
            this.player.displayMessage("=".repeat(60));
            
            this.revelationTriggered = true;
            this.gameWon = true;
            
            this.player.displayMessage("\n🎾 Congratulations! You've solved Maxwell's mystery!");
            this.player.displayMessage("Thanks for playing Turbo's Quest!");
            this.player.displayMessage("\nType 'quit' to end the adventure.");
            
            this.player.updateUI();
        }
    }

    checkAllItemsCollected() {
        const requiredItems = ["child_mtb_helmet", "child_mtb_gloves", "small_mtb_bike"];
        return requiredItems.every(item => this.player.hasItem(item));
    }

    showCurrentOptions() {
        const currentLoc = this.locations[this.player.currentLocation];
        const actions = currentLoc.actions || {};
        const exits = currentLoc.exits || {};
        
        this.player.displayMessage("\n💡 You can try:");
        
        if (Object.keys(actions).length > 0) {
            for (let action of Object.keys(actions)) {
                this.player.displayMessage(`  - ${action}`);
            }
        }
        
        if (Object.keys(exits).length > 0) {
            this.player.displayMessage("  Or go to:");
            for (let exitName of Object.keys(exits)) {
                this.player.displayMessage(`  - ${exitName}`);
            }
        }
        
        this.player.displayMessage("  Other commands: 'help', 'inventory', 'look', 'stats'");
        
        if (this.checkAllItemsCollected() && !this.player.sizeRealizationTriggered) {
            this.player.displayMessage("\n🎯 QUEST UPDATE: You have all three special items!");
            this.player.displayMessage("💡 HINT: Try 'examine all items' to understand what they have in common.");
        } else if (this.player.sizeRealizationTriggered && !this.revelationTriggered) {
            this.player.displayMessage("\n🎯 QUEST PHASE 2: Ready for Maxwell's final revelation!");
            this.player.displayMessage("💫 Move to any location or use 'look' to discover the truth!");
        }
    }

    showQuickLocationReminder() {
        const locationId = this.player.currentLocation;
        const location = this.locations[locationId];
        
        this.player.displayMessage(`\n📍 Currently in: ${location.name}`);
        
        const actions = location.actions || {};
        if (Object.keys(actions).length > 0) {
            const actionsList = Object.keys(actions);
            if (actionsList.length <= 3) {
                this.player.displayMessage(`🎯 Can do: ${actionsList.join(', ')}`);
            } else {
                this.player.displayMessage(`🎯 Can do: ${actionsList.slice(0, 3).join(', ')}, and more ('look' to see all)`);
            }
        }
        
        const exits = location.exits || {};
        if (Object.keys(exits).length > 0) {
            const exitsList = Object.keys(exits);
            this.player.displayMessage(`🚪 Can go to: ${exitsList.join(', ')}`);
        }
        
        if (this.player.questItemsFound > 0) {
            if (!this.player.sizeRealizationTriggered) {
                this.player.displayMessage(`🎾 Quest Phase 1: ${this.player.questItemsFound}/3 special items found`);
            } else if (!this.revelationTriggered) {
                this.player.displayMessage(`🎾 Quest Phase 2: Understanding achieved, final revelation pending`);
            } else {
                this.player.displayMessage(`🎉 Quest Complete: Maxwell's wonderful secret revealed!`);
            }
        }
    }

    showHelp() {
        const helpLines = this.story.messages.help_text;
        for (let line of helpLines) {
            this.player.displayMessage(line);
        }
    }
}

// Initialize the game when the page loads
let game;
window.addEventListener('load', () => {
    game = new GameEngine();
    game.startGame();
});