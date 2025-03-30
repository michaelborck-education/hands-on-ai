# Mood Journal Assistant

**Difficulty**: Beginner-Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: File I/O, date handling, text analysis

## Overview

Create a journaling assistant that helps users track moods and reflect on patterns.

## Instructions

```python
from ailabkit.chat import get_response
import datetime
import os
import json

def mood_journal():
    """Interactive mood journaling assistant"""
    journal_dir = os.path.expanduser("~/.mood_journal")
    os.makedirs(journal_dir, exist_ok=True)
    
    journal_file = os.path.join(journal_dir, "journal_entries.json")
    
    # Load existing entries
    if os.path.exists(journal_file):
        with open(journal_file, 'r') as f:
            try:
                entries = json.load(f)
            except json.JSONDecodeError:
                entries = []
    else:
        entries = []
    
    # Get today's date
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    print("=== Mood Journal Assistant ===")
    print("1. Add a new entry")
    print("2. View past entries")
    print("3. Get insights")
    
    choice = input("\nWhat would you like to do? ")
    
    if choice == "1":
        # Add new entry
        mood = input("\nHow would you rate your mood today (1-10)? ")
        activities = input("What activities did you do today? ")
        thoughts = input("Share any thoughts or reflections: ")
        
        entry = {
            "date": today,
            "mood": mood,
            "activities": activities,
            "thoughts": thoughts
        }
        
        entries.append(entry)
        
        # Save updated entries
        with open(journal_file, 'w') as f:
            json.dump(entries, f, indent=2)
        
        # Get AI reflection
        reflection_prompt = f"""
        The user rated their mood as {mood}/10 today.
        They did these activities: {activities}
        Their thoughts: {thoughts}
        
        Provide a thoughtful, supportive reflection on their entry.
        """
        
        reflection = get_response(reflection_prompt, 
                                 system="You are a supportive, empathetic journaling assistant.")
        print("\n=== Reflection ===")
        print(reflection)
        
    elif choice == "2":
        # View past entries
        if not entries:
            print("No entries found.")
            return
            
        print("\n=== Past Entries ===")
        for i, entry in enumerate(reversed(entries[-10:])):  # Show last 10 entries
            print(f"{i+1}. {entry['date']} - Mood: {entry['mood']}/10")
        
        entry_choice = input("\nWhich entry would you like to view? (number) ")
        try:
            idx = int(entry_choice) - 1
            entry = list(reversed(entries[-10:]))[idx]
            print(f"\nDate: {entry['date']}")
            print(f"Mood: {entry['mood']}/10")
            print(f"Activities: {entry['activities']}")
            print(f"Thoughts: {entry['thoughts']}")
        except (ValueError, IndexError):
            print("Invalid entry number.")
            
    elif choice == "3":
        # Get insights
        if len(entries) < 3:
            print("Need more entries to generate insights (at least 3).")
            return
            
        # Create a summary of recent entries
        recent_entries = entries[-7:]  # Last 7 entries
        entries_text = ""
        
        for entry in recent_entries:
            entries_text += f"Date: {entry['date']}, Mood: {entry['mood']}/10\n"
            entries_text += f"Activities: {entry['activities']}\n"
            entries_text += f"Thoughts: {entry['thoughts']}\n\n"
        
        insight_prompt = f"""
        Here are the user's recent journal entries:
        
        {entries_text}
        
        Based on these entries, provide:
        1. Any patterns you notice in their mood
        2. Activities that seem to correlate with higher moods
        3. Gentle suggestions that might help improve their wellbeing
        4. A positive affirmation
        """
        
        insights = get_response(insight_prompt, 
                               system="You are an insightful, supportive journaling assistant who helps identify patterns in mood and behavior.")
        print("\n=== Mood Insights ===")
        print(insights)
    
    else:
        print("Invalid choice.")

# Run the journal
if __name__ == "__main__":
    mood_journal()
```

## Extension Ideas

Add mood tracking visualizations or goal-setting features.

---