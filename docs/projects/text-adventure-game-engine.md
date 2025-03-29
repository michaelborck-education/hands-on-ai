# Text Adventure Game Engine

**Difficulty**: Advanced  
**Time**: 90-120 minutes  
**Learning Focus**: Object-oriented programming, game design, file I/O, AI interaction

## Overview

Create a text adventure game engine that allows students to build interactive stories with rooms, items, and characters. The engine supports saving/loading games and provides AI-powered hints to guide players.

## Instructions

```python
from chatcraft import get_response
import json
import os

class Room:
    """A location in the game world with description and connections to other rooms."""
    def __init__(self, name, description, exits=None, items=None):
        self.name = name
        self.description = description
        self.exits = exits or {}  # Dictionary mapping direction -> room name
        self.items = items or []  # List of item names
    
    def add_exit(self, direction, room_name):
        """Add an exit from this room."""
        self.exits[direction] = room_name
    
    def add_item(self, item):
        """Add an item to this room."""
        self.items.append(item)
    
    def remove_item(self, item):
        """Remove an item from this room."""
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def get_details(self):
        """Get a formatted description of the room including exits and items."""
        details = f"{self.name}\n"
        details += f"{'-' * len(self.name)}\n"
        details += f"{self.description}\n"
        
        if self.exits:
            details += "\nExits:"
            for direction, room in self.exits.items():
                details += f" {direction}"
        
        if self.items:
            details += "\n\nYou can see:"
            for item in self.items:
                details += f"\n- {item}"
        
        return details
    
    def to_dict(self):
        """Convert room to dictionary for saving."""
        return {
            "name": self.name,
            "description": self.description,
            "exits": self.exits,
            "items": self.items
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create room from dictionary data."""
        return cls(
            data["name"],
            data["description"],
            data.get("exits", {}),
            data.get("items", [])
        )


class Player:
    """The player character with inventory and current location."""
    def __init__(self, name, current_room="Starting Room"):
        self.name = name
        self.current_room = current_room
        self.inventory = []
        self.game_flags = {}  # For tracking game state, quests, etc.
    
    def move(self, direction, world):
        """Try to move in a direction. Return success/failure message."""
        current_room = world.get_room(self.current_room)
        
        if direction in current_room.exits:
            self.current_room = current_room.exits[direction]
            return f"You move {direction}."
        else:
            return f"You can't go {direction} from here."
    
    def take(self, item_name, world):
        """Try to take an item from the current room."""
        current_room = world.get_room(self.current_room)
        
        for item in current_room.items:
            if item.lower() == item_name.lower():
                current_room.remove_item(item)
                self.inventory.append(item)
                return f"You take the {item}."
        
        return f"There is no {item_name} here."
    
    def drop(self, item_name, world):
        """Try to drop an item from inventory into the current room."""
        current_room = world.get_room(self.current_room)
        
        for item in self.inventory:
            if item.lower() == item_name.lower():
                self.inventory.remove(item)
                current_room.add_item(item)
                return f"You drop the {item}."
        
        return f"You don't have a {item_name}."
    
    def check_inventory(self):
        """Check what items the player is carrying."""
        if not self.inventory:
            return "Your inventory is empty."
        
        result = "You are carrying:"
        for item in self.inventory:
            result += f"\n- {item}"
        return result
    
    def to_dict(self):
        """Convert player to dictionary for saving."""
        return {
            "name": self.name,
            "current_room": self.current_room,
            "inventory": self.inventory,
            "game_flags": self.game_flags
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create player from dictionary data."""
        player = cls(data["name"], data["current_room"])
        player.inventory = data.get("inventory", [])
        player.game_flags = data.get("game_flags", {})
        return player


class World:
    """The game world containing all rooms and game state."""
    def __init__(self, title="Adventure Game"):
        self.title = title
        self.rooms = {}  # Dictionary mapping room name -> Room object
    
    def add_room(self, room):
        """Add a room to the world."""
        self.rooms[room.name] = room
    
    def get_room(self, room_name):
        """Get a room by name."""
        return self.rooms.get(room_name)
    
    def to_dict(self):
        """Convert world to dictionary for saving."""
        return {
            "title": self.title,
            "rooms": {name: room.to_dict() for name, room in self.rooms.items()}
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create world from dictionary data."""
        world = cls(data["title"])
        for name, room_data in data["rooms"].items():
            world.add_room(Room.from_dict(room_data))
        return world


class GameEngine:
    """Main game engine for running the adventure."""
    def __init__(self, player, world):
        self.player = player
        self.world = world
        self.running = False
        self.commands = {
            "go": self.cmd_go,
            "look": self.cmd_look,
            "take": self.cmd_take,
            "drop": self.cmd_drop,
            "inventory": self.cmd_inventory,
            "help": self.cmd_help,
            "quit": self.cmd_quit
        }
        self.save_dir = "game_saves"
        os.makedirs(self.save_dir, exist_ok=True)
    
    def cmd_go(self, args):
        """Handle movement command."""
        if not args:
            return "Go where? Try 'go north', 'go south', etc."
        
        direction = args[0].lower()
        return self.player.move(direction, self.world)
    
    def cmd_look(self, args):
        """Look around the current room."""
        current_room = self.world.get_room(self.player.current_room)
        return current_room.get_details()
    
    def cmd_take(self, args):
        """Take an item from the room."""
        if not args:
            return "Take what? Try 'take [item name]'."
        
        item_name = " ".join(args)
        return self.player.take(item_name, self.world)
    
    def cmd_drop(self, args):
        """Drop an item from inventory."""
        if not args:
            return "Drop what? Try 'drop [item name]'."
        
        item_name = " ".join(args)
        return self.player.drop(item_name, self.world)
    
    def cmd_inventory(self, args):
        """Check inventory."""
        return self.player.check_inventory()
    
    def cmd_help(self, args):
        """Show help information."""
        help_text = "Available commands:\n"
        help_text += "- go [direction]: Move in a direction (north, south, east, west)\n"
        help_text += "- look: Examine your surroundings\n"
        help_text += "- take [item]: Take an item from the room\n"
        help_text += "- drop [item]: Drop an item from your inventory\n"
        help_text += "- inventory: Check what you're carrying\n"
        help_text += "- help: Show this help text\n"
        help_text += "- quit: Exit the game\n"
        help_text += "- hint: Get a helpful hint (AI-powered)\n"
        help_text += "- save [name]: Save your progress\n"
        return help_text
    
    def cmd_quit(self, args):
        """Quit the game."""
        self.running = False
        return "Thanks for playing!"
    
    def save_game(self, filename):
        """Save the current game state."""
        game_data = {
            "world": self.world.to_dict(),
            "player": self.player.to_dict()
        }
        
        filepath = os.path.join(self.save_dir, f"{filename}.json")
        with open(filepath, 'w') as f:
            json.dump(game_data, f, indent=2)
        
        return f"Game saved as '{filename}'"
    
    @classmethod
    def load_game(cls, filename):
        """Load a game from a save file."""
        filepath = os.path.join("game_saves", f"{filename}.json")
        
        with open(filepath, 'r') as f:
            game_data = json.load(f)
        
        world = World.from_dict(game_data["world"])
        player = Player.from_dict(game_data["player"])
        
        return cls(player, world)
    
    def process_input(self, user_input):
        """Process user input and return the result."""
        words = user_input.lower().split()
        
        if not words:
            return "Please enter a command."
        
        command = words[0]
        args = words[1:] if len(words) > 1 else []
        
        if command in self.commands:
            return self.commands[command](args)
        else:
            return f"I don't understand '{command}'. Try 'help' for a list of commands."
    
    def run(self):
        """Run the main game loop."""
        self.running = True
        
        print(f"Welcome to {self.world.title}!")
        print(f"You are {self.player.name}, an adventurer seeking fortune and glory.")
        print("Type 'help' for a list of commands.")
        
        # Show the initial room
        current_room = self.world.get_room(self.player.current_room)
        print("\n" + current_room.get_details())
        
        while self.running:
            user_input = input("\n> ").strip()
            
            # Special case for save command
            if user_input.startswith("save "):
                save_name = user_input[5:].strip()
                if save_name:
                    print(self.save_game(save_name))
                else:
                    print("Please specify a save name: 'save [name]'")
                continue
            
            # Special case for AI hint
            if user_input.lower() == "hint":
                try:
                    current_room = self.world.get_room(self.player.current_room)
                    inventory_str = ", ".join(self.player.inventory) if self.player.inventory else "nothing"
                    
                    hint_prompt = f"""
                    In this text adventure game:
                    - The player is in: {current_room.name}
                    - Room description: {current_room.description}
                    - Available exits: {', '.join(current_room.exits.keys()) if current_room.exits else 'none'}
                    - Items in room: {', '.join(current_room.items) if current_room.items else 'none'}
                    - Player is carrying: {inventory_str}
                    
                    Based on this situation, provide a gentle hint about what the player might try next.
                    Keep it vague enough to not spoil puzzles but helpful enough to guide them.
                    """
                    
                    print("Thinking of a hint...")
                    hint = get_response(hint_prompt)
                    print(f"\nHint: {hint}")
                    
                except Exception as e:
                    print(f"Sorry, I couldn't come up with a hint right now: {e}")
                
                continue
            
            result = self.process_input(user_input)
            print(result)


def create_default_world():
    """Create a simple default world for demonstration."""
    world = World("The Forgotten Caverns")
    
    # Create rooms
    entrance = Room(
        "Cave Entrance",
        "You stand at the entrance to a mysterious cave. Sunlight filters in from above, casting eerie shadows on the walls."
    )
    
    main_passage = Room(
        "Main Passage",
        "A narrow passage stretches deeper into the cave. Water drips from the ceiling, creating small puddles on the ground."
    )
    
    chamber = Room(
        "Crystal Chamber",
        "This large chamber is filled with glowing crystals of various colors, illuminating the space with an otherworldly light."
    )
    
    side_tunnel = Room(
        "Side Tunnel",
        "A tight tunnel branches off from the main passage. The air feels stale here."
    )
    
    underground_pool = Room(
        "Underground Pool",
        "A still, dark pool of water fills most of this chamber. The surface reflects the subtle glow from the ceiling."
    )
    
    # Connect rooms
    entrance.add_exit("north", "Main Passage")
    
    main_passage.add_exit("south", "Cave Entrance")
    main_passage.add_exit("north", "Crystal Chamber")
    main_passage.add_exit("east", "Side Tunnel")
    
    chamber.add_exit("south", "Main Passage")
    chamber.add_exit("west", "Underground Pool")
    
    side_tunnel.add_exit("west", "Main Passage")
    
    underground_pool.add_exit("east", "Crystal Chamber")
    
    # Add items
    entrance.add_item("torch")
    entrance.add_item("rope")
    
    main_passage.add_item("rusty key")
    
    chamber.add_item("glowing crystal")
    
    underground_pool.add_item("ancient coin")
    
    # Add rooms to world
    world.add_room(entrance)
    world.add_room(main_passage)
    world.add_room(chamber)
    world.add_room(side_tunnel)
    world.add_room(underground_pool)
    
    return world


def play_adventure_game():
    """Start a new adventure game or load a saved one."""
    print("=== Text Adventure Game Engine ===")
    print("1. Start new game")
    print("2. Load saved game")
    
    choice = input("\nSelect an option: ")
    
    if choice == "1":
        player_name = input("\nWhat is your name, adventurer? ")
        player = Player(player_name, "Cave Entrance")
        world = create_default_world()
        game = GameEngine(player, world)
        game.run()
    
    elif choice == "2":
        # Check for save files
        save_dir = "game_saves"
        if not os.path.exists(save_dir) or not os.listdir(save_dir):
            print("No save files found. Starting a new game...")
            player_name = input("\nWhat is your name, adventurer? ")
            player = Player(player_name, "Cave Entrance")
            world = create_default_world()
            game = GameEngine(player, world)
        else:
            # List save files
            save_files = [f[:-5] for f in os.listdir(save_dir) if f.endswith(".json")]
            print("\nAvailable save files:")
            for i, save in enumerate(save_files, 1):
                print(f"{i}. {save}")
            
            save_idx = int(input("\nSelect a save file (number): ")) - 1
            if 0 <= save_idx < len(save_files):
                try:
                    game = GameEngine.load_game(save_files[save_idx])
                    print(f"Loaded save: {save_files[save_idx]}")
                except Exception as e:
                    print(f"Error loading save: {e}")
                    return
            else:
                print("Invalid selection. Starting a new game...")
                player_name = input("\nWhat is your name, adventurer? ")
                player = Player(player_name, "Cave Entrance")
                world = create_default_world()
                game = GameEngine(player, world)
        
        game.run()
    
    else:
        print("Invalid choice. Exiting.")


# Run the game
if __name__ == "__main__":
    play_adventure_game()
```

## Extension Ideas

- Add more room types with special properties (e.g., dark rooms that require a light source)
- Implement NPCs (non-player characters) that the player can talk to
- Add simple puzzles that require specific items to solve
- Create a quest system with objectives and rewards
- Design a combat system for encounters with enemies
- Build a web-based interface using a framework like Flask

---