# Journal or Reflection Bot

**Difficulty**: Beginner-Intermediate  
**Time**: 30-45 minutes  
**Learning Focus**: Lists, memory, summarization

## Overview

Create a digital journaling assistant that helps users reflect on their experiences, identify patterns in their thoughts, and provide meaningful insights or feedback on their entries.

## Instructions

```python
from ailabkit.chat import get_response
import datetime
import os

def reflection_journal():
    print("=== Personal Reflection Journal ===")
    print("Use this bot to keep track of your thoughts and receive insights.")
    print("Type 'exit' at any time to quit.\n")
    
    # Create a list to store journal entries
    memory = []
    
    # Create a simple file-based storage system
    journal_file = "journal_entries.txt"
    
    # Load previous entries if file exists
    if os.path.exists(journal_file):
        try:
            with open(journal_file, 'r') as f:
                previous_entries = f.read().strip()
                if previous_entries:
                    print("Found previous journal entries.")
                    restore = input("Would you like to include them in today's reflection? (yes/no): ").lower()
                    if restore == "yes":
                        memory.append(previous_entries)
                        print("Previous entries loaded.")
        except Exception as e:
            print(f"Error loading previous entries: {e}")
    
    # Main journaling loop
    num_entries = int(input("How many things would you like to reflect on today? (1-5): "))
    num_entries = min(max(1, num_entries), 5)  # Ensure between 1 and 5
    
    for i in range(num_entries):
        print(f"\n--- Entry {i+1}/{num_entries} ---")
        
        # Prompt options
        prompts = [
            "What's something that happened today that you'd like to reflect on?",
            "What's something you learned today?",
            "What's something you're grateful for today?",
            "What's something that challenged you today?",
            "What's something you're looking forward to?"
        ]
        
        # Let user choose a prompt or write their own
        print("Choose a prompt or create your own:")
        for j, prompt in enumerate(prompts, 1):
            print(f"{j}. {prompt}")
        print(f"{len(prompts) + 1}. Write my own prompt")
        
        prompt_choice = input("\nEnter choice (1-6): ")
        
        # Exit condition
        if prompt_choice.lower() == "exit":
            break
            
        # Get the prompt
        try:
            choice_num = int(prompt_choice)
            if 1 <= choice_num <= len(prompts):
                selected_prompt = prompts[choice_num - 1]
            else:
                selected_prompt = input("Enter your custom prompt: ")
        except ValueError:
            selected_prompt = prompts[0]  # Default to first prompt if invalid input
        
        # Get the journal entry
        print(f"\n{selected_prompt}")
        entry = input("> ")
        
        # Exit condition
        if entry.lower() == "exit":
            break
            
        # Record the timestamp and add to memory
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        full_entry = f"[{timestamp}] {selected_prompt}\n{entry}"
        memory.append(full_entry)
        
        # Give immediate reflection
        if i < num_entries - 1:  # Only for entries except the last one
            reflection = get_response(
                f"The user wrote this journal entry: {entry}\n\nGive a brief, thoughtful response that might help them reflect deeper.",
                system="You are a supportive journaling assistant. Respond with 1-2 sentences that are empathetic and thought-provoking, but not advice-giving."
            )
            print("\nReflection:")
            print(reflection)
    
    # If we have entries, save them and provide insights
    if memory:
        # Save entries to file
        try:
            with open(journal_file, 'a') as f:
                for entry in memory:
                    f.write(entry + "\n\n")
            print("\nJournal entries saved.")
        except Exception as e:
            print(f"Error saving entries: {e}")
        
        # Combine all entries for analysis
        all_entries = "\n\n".join(memory)
        
        # Generate insights
        print("\n=== Journal Insights ===")
        insights = get_response(
            f"Here are the user's journal entries:\n\n{all_entries}\n\nProvide thoughtful insights about these reflections.",
            system="You are an insightful journaling assistant. Analyze these entries for patterns, themes, or notable elements. Provide 3-4 helpful observations that might help the user understand their thoughts better. Be supportive and thoughtful."
        )
        
        print(insights)
        
        # Offer a follow-up question
        print("\n=== Reflection Question ===")
        question = get_response(
            f"Based on these journal entries:\n\n{all_entries}\n\nProvide one thoughtful question that would help the user reflect more deeply.",
            system="You are a reflective journaling coach. Create one open-ended, thought-provoking question that will help the user explore their thoughts more deeply. The question should be specific to the content of their entries."
        )
        
        print(question)
    else:
        print("No journal entries were recorded.")

# Run the reflection journal
if __name__ == "__main__":
    reflection_journal()
```

## Extension Ideas

- Add mood tracking to each entry
- Create visualizations of common themes or topics over time
- Add a guided meditation option based on journal content
- Implement a goal-setting feature that references past entries
- Create specialized journaling templates for different purposes (gratitude, productivity, etc.)

---