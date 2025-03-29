## Choose Your Own Adventure

**Difficulty**: Intermediate  
**Time**: 60-90 minutes  
**Learning Focus**: State management, narrative design, user input handling

### Overview

Create an interactive story where the bot generates narrative segments based on user choices.

### Instructions

```python
from chatcraft import get_response

def adventure_game():
    """Interactive Choose Your Own Adventure game powered by an LLM"""
    # Story state tracking
    story_context = {
        "setting": "",
        "character": "",
        "inventory": [],
        "goals": [],
        "events": []
    }
    
    print("=== Choose Your Own Adventure Generator ===")
    print("Let's create your custom adventure!\n")
    
    # Get initial story parameters
    setting_options = ["fantasy kingdom", "space station", "haunted mansion", 
                       "prehistoric world", "cyberpunk city", "desert island"]
    
    print("Choose a setting:")
    for i, setting in enumerate(setting_options):
        print(f"{i+1}. {setting}")
    
    setting_choice = int(input("\nSetting (1-6): ")) - 1
    story_context["setting"] = setting_options[setting_choice]
    
    character_type = input("\nWhat type of character do you want to play? ")
    story_context["character"] = character_type
    
    goal = input("\nWhat is your character's main goal? ")
    story_context["goals"].append(goal)
    
    # Generate story intro
    story_prompt = f"""
    Create the introduction to an interactive adventure story with these details:
    - Setting: {story_context['setting']}
    - Main character: {story_context['character']}
    - Character's goal: {story_context['goals'][0]}
    
    End with exactly two choices the player can make.
    Format the choices as:
    CHOICE 1: (first option)
    CHOICE 2: (second option)
    """
    
    story_system = """
    You are a creative storyteller crafting an interactive adventure.
    Create vivid descriptions and meaningful choices.
    For each story segment, provide exactly two choices for the player.
    """
    
    # Generate and print first segment
    current_segment = get_response(story_prompt, system=story_system)
    print("\n=== Your Adventure Begins ===\n")
    
    # Split segment from choices
    parts = current_segment.split("CHOICE 1:")
    narrative = parts[0].strip()
    choices = "CHOICE 1:" + parts[1]
    
    print(narrative + "\n")
    print(choices)
    
    # Story loop
    turns = 0
    max_turns = 5
    
    while turns < max_turns:
        choice = input("\nEnter 1 or 2 to choose: ")
        
        if choice not in ["1", "2"]:
            print("Please enter 1 or 2.")
            continue
            
        # Add to story context
        if choice == "1":
            chosen_option = choices.split("CHOICE 1:")[1].split("CHOICE 2:")[0].strip()
        else:
            chosen_option = choices.split("CHOICE 2:")[1].strip()
            
        story_context["events"].append(chosen_option)
        
        # Generate next segment based on choice and story so far
        context_summary = f"""
        Setting: {story_context['setting']}
        Character: {story_context['character']}
        Goal: {story_context['goals'][0]}
        Previous events: {' '.join(story_context['events'])}
        """
        
        continuation_prompt = f"""
        Continue the story based on these details:
        {context_summary}
        
        The player just chose: {chosen_option}
        
        Continue the story from there and provide two new choices.
        End with:
        CHOICE 1: (first option)
        CHOICE 2: (second option)
        """
        
        # Generate next segment
        next_segment = get_response(continuation_prompt, system=story_system)
        print("\n" + "="*50 + "\n")
        
        # Split segment from choices
        parts = next_segment.split("CHOICE 1:")
        narrative = parts[0].strip()
        
        # Check if we've reached the ending
        if "CHOICE 1:" not in next_segment:
            print(next_segment)
            print("\n=== The End ===")
            break
            
        choices = "CHOICE 1:" + parts[1]
        
        print(narrative + "\n")
        print(choices)
        
        turns += 1
        
        # Final turn
        if turns >= max_turns:
            # Generate conclusion
            conclusion_prompt = f"""
            Create a satisfying conclusion to the story based on these details:
            {context_summary}
            
            The player just chose: {chosen_option}
            
            Write a final paragraph that wraps up the adventure.
            """
            
            conclusion = get_response(conclusion_prompt, system=story_system)
            
            print("\n" + "="*50 + "\n")
            print(conclusion)
            print("\n=== The End ===")
            
    print("\nThanks for playing!")

# Run the adventure game
if __name__ == "__main__":
    adventure_game()
```

### Extension Ideas

Add inventory management, character stats, or multiple endings based on decisions.

---