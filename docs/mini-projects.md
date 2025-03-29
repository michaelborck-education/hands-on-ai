# Mini Project Examples

This document contains ready-to-use mini-projects and activities for using ChatCraft in educational settings. Each project includes learning objectives, difficulty level, estimated time, and complete code examples.

## Table of Contents

1. [Advanced Journal Assistant](#advanced-journal-assistant)
2. [Run the personality menu](#run-the-personality-menu)
3. [Example bot personality](#example-bot-personality)
4. [Run the adventure game](#run-the-adventure-game)
5. [Run the classroom simulation](#run-the-classroom-simulation)
6. [Run the code explainer](#run-the-code-explainer)
7. [Run the writing partner](#run-the-writing-partner)
8. [Run the dashboard](#run-the-dashboard)
9. [Run the dialogue simulator](#run-the-dialogue-simulator)
10. [Run the emotional support bot](#run-the-emotional-support-bot)
11. [Run the historical figure chat](#run-the-historical-figure-chat)
12. [Run the gallery creator](#run-the-gallery-creator)
13. [Run the reflection journal](#run-the-reflection-journal)
14. [Run the quiz](#run-the-quiz)
15. [Run the translation helper](#run-the-translation-helper)
16. [Run the journal](#run-the-journal)
17. [Run the chatbot](#run-the-chatbot)
18. [Example personalities students can create:](#example-personalities-students-can-create:)
19. [Run the to-do list](#run-the-to-do-list)
20. [Run the tutor bot](#run-the-tutor-bot)
21. [Run the game](#run-the-game)
22. [Run the quiz](#run-the-quiz)
23. [Run the dashboard](#run-the-dashboard)
24. [YouTube to Blog Converter](#youtube-to-blog-converter)

---

# Advanced Journal Assistant

**Difficulty**: Intermediate-Advanced  
**Time**: 60-90 minutes  
**Learning Focus**: Data structures, file I/O, data visualization, natural language processing, user experience design

### Overview

Create a comprehensive journaling application that combines structured mood tracking with flexible reflection prompts, offering users deep insights through data visualization and AI-powered analysis.

### Instructions

```python
from chatcraft import get_response
import datetime
import os
import json
import matplotlib.pyplot as plt
from collections import Counter
import re

class AdvancedJournalAssistant:
    def __init__(self):
        """Initialize the journal assistant with necessary directories and files"""
        # Set up storage directories
        self.journal_dir = os.path.expanduser("~/.advanced_journal")
        self.visualization_dir = os.path.join(self.journal_dir, "visualizations")
        os.makedirs(self.journal_dir, exist_ok=True)
        os.makedirs(self.visualization_dir, exist_ok=True)
        
        # Define file paths
        self.journal_file = os.path.join(self.journal_dir, "journal_entries.json")
        self.prompt_file = os.path.join(self.journal_dir, "custom_prompts.json")
        
        # Initialize data structures
        self.entries = self._load_entries()
        self.custom_prompts = self._load_custom_prompts()
        
        # Default prompts
        self.default_prompts = [
            "What's something that happened today that you'd like to reflect on?",
            "What's something you learned today?",
            "What's something you're grateful for today?",
            "What's something that challenged you today?",
            "What's something you're looking forward to?",
            "How did you take care of yourself today?",
            "Was there a moment today that stood out? Why?",
            "What's something you'd like to remember about today?"
        ]
        
        # Define mood labels for better interpretation
        self.mood_labels = {
            1: "Very Low", 2: "Low", 3: "Somewhat Low", 4: "Below Average", 5: "Neutral", 
            6: "Slightly Positive", 7: "Good", 8: "Very Good", 9: "Excellent", 10: "Outstanding"
        }
        
        # Track user preferences
        self.preferences = self._load_preferences()
        
    def _load_entries(self):
        """Load existing journal entries or return an empty list"""
        if os.path.exists(self.journal_file):
            try:
                with open(self.journal_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    
    def _load_custom_prompts(self):
        """Load custom prompts or return an empty list"""
        if os.path.exists(self.prompt_file):
            try:
                with open(self.prompt_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    
    def _load_preferences(self):
        """Load user preferences or set defaults"""
        pref_file = os.path.join(self.journal_dir, "preferences.json")
        defaults = {
            "auto_insights": True,
            "daily_reminder": False,
            "reminder_time": "20:00",
            "favorite_prompts": [],
            "theme": "standard",
            "insight_frequency": "weekly"
        }
        
        if os.path.exists(pref_file):
            try:
                with open(pref_file, 'r') as f:
                    stored_prefs = json.load(f)
                    # Update defaults with stored preferences
                    defaults.update(stored_prefs)
            except json.JSONDecodeError:
                pass
        
        return defaults
    
    def _save_entries(self):
        """Save journal entries to file"""
        with open(self.journal_file, 'w') as f:
            json.dump(self.entries, f, indent=2)
    
    def _save_custom_prompts(self):
        """Save custom prompts to file"""
        with open(self.prompt_file, 'w') as f:
            json.dump(self.custom_prompts, f, indent=2)
    
    def _save_preferences(self):
        """Save user preferences to file"""
        pref_file = os.path.join(self.journal_dir, "preferences.json")
        with open(pref_file, 'w') as f:
            json.dump(self.preferences, f, indent=2)
    
    def display_menu(self):
        """Display the main menu and handle user choices"""
        print("\n======================================")
        print("=== Advanced Journal Assistant ===")
        print("======================================")
        print("1. Create new journal entry")
        print("2. View past entries")
        print("3. Get insights and analytics")
        print("4. Manage custom prompts")
        print("5. Set goals and intentions")
        print("6. Preferences")
        print("7. Export journal")
        print("8. Exit")
        
        try:
            choice = input("\nWhat would you like to do? (1-8): ")
            
            menu_actions = {
                "1": self.create_entry,
                "2": self.view_entries,
                "3": self.get_insights,
                "4": self.manage_prompts,
                "5": self.set_goals,
                "6": self.set_preferences,
                "7": self.export_journal,
                "8": self.exit_app
            }
            
            # Execute the chosen action or show error
            if choice in menu_actions:
                menu_actions[choice]()
            else:
                print("Invalid choice. Please try again.")
                self.display_menu()
                
        except KeyboardInterrupt:
            self.exit_app()
    
    def create_entry(self):
        """Create a new journal entry with structured and free-form components"""
        print("\n=== New Journal Entry ===")
        
        # Get date/time
        today = datetime.datetime.now()
        date_str = today.strftime("%Y-%m-%d")
        time_str = today.strftime("%H:%M")
        
        # Check if we already have an entry for today
        existing_entries = [e for e in self.entries if e["date"] == date_str]
        if existing_entries:
            print(f"You already have {len(existing_entries)} entries for today.")
            add_another = input("Would you like to add another entry? (y/n): ").lower()
            if add_another != 'y':
                self.display_menu()
                return
        
        # Collect mood data
        try:
            mood = int(input("\nHow would you rate your mood right now (1-10)? "))
            if not 1 <= mood <= 10:
                print("Please enter a number between 1 and 10.")
                mood = 5  # Default to neutral if invalid
            mood_label = self.mood_labels[mood]
            print(f"Mood: {mood}/10 - {mood_label}")
        except ValueError:
            print("Invalid input. Setting mood to neutral (5/10).")
            mood = 5
            mood_label = self.mood_labels[mood]
        
        # Get energy level
        try:
            energy = int(input("\nHow is your energy level (1-10)? "))
            if not 1 <= energy <= 10:
                energy = 5  # Default if invalid
        except ValueError:
            energy = 5
        
        # Get prompt for reflection
        print("\nChoose a prompt for reflection:")
        all_prompts = self.default_prompts + self.custom_prompts
        
        # Show prompts
        for i, prompt in enumerate(all_prompts, 1):
            print(f"{i}. {prompt}")
        print(f"{len(all_prompts) + 1}. Create a custom prompt")
        
        try:
            prompt_choice = int(input("\nSelect a prompt (number): "))
            if 1 <= prompt_choice <= len(all_prompts):
                selected_prompt = all_prompts[prompt_choice - 1]
            else:
                custom_prompt = input("Enter your custom prompt: ")
                selected_prompt = custom_prompt
                # Ask if they want to save this prompt for future use
                save_prompt = input("Would you like to save this prompt for future use? (y/n): ").lower()
                if save_prompt == 'y':
                    self.custom_prompts.append(custom_prompt)
                    self._save_custom_prompts()
                    print("Custom prompt saved.")
        except (ValueError, IndexError):
            # Default to first prompt if invalid
            selected_prompt = all_prompts[0]
            print(f"Using default prompt: {selected_prompt}")
        
        # Display the selected prompt and get reflection
        print(f"\n> {selected_prompt}")
        reflection = input("Your reflection: ")
        
        # Get activities
        activities = input("\nWhat activities did you do today? (comma-separated): ")
        activity_list = [a.strip() for a in activities.split(",") if a.strip()]
        
        # Get any tags the user wants to associate with this entry
        tags = input("\nAdd any tags to help categorize this entry (comma-separated): ")
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        
        # Create the entry object
        entry = {
            "date": date_str,
            "time": time_str,
            "mood": mood,
            "mood_label": mood_label,
            "energy": energy,
            "prompt": selected_prompt,
            "reflection": reflection,
            "activities": activity_list,
            "tags": tag_list,
            "ai_insights": None  # Will be filled in by AI
        }
        
        # Get AI reflection if user wants it
        if self.preferences["auto_insights"]:
            print("\nGenerating insights for your entry...")
            entry["ai_insights"] = self._generate_entry_insight(entry)
            print("\n=== AI Reflection ===")
            print(entry["ai_insights"])
        
        # Add entry to the list and save
        self.entries.append(entry)
        self._save_entries()
        print("\nJournal entry saved successfully!")
        
        # Return to menu
        input("\nPress Enter to continue...")
        self.display_menu()
    
    def view_entries(self):
        """View and search past journal entries"""
        if not self.entries:
            print("\nNo journal entries found.")
            input("\nPress Enter to continue...")
            self.display_menu()
            return
        
        print("\n=== View Journal Entries ===")
        print("1. View recent entries")
        print("2. Search by date")
        print("3. Search by mood")
        print("4. Search by tag")
        print("5. Search by text")
        print("6. Return to main menu")
        
        choice = input("\nWhat would you like to do? (1-6): ")
        
        if choice == "1":
            # Show recent entries
            recent = self.entries[-10:]  # Last 10 entries
            recent.reverse()  # Most recent first
            self._display_entry_list(recent, "Recent Entries")
            
        elif choice == "2":
            # Search by date
            date_query = input("\nEnter date (YYYY-MM-DD) or month (YYYY-MM): ")
            matching = [e for e in self.entries if e["date"].startswith(date_query)]
            self._display_entry_list(matching, f"Entries for {date_query}")
            
        elif choice == "3":
            # Search by mood
            try:
                mood_min = int(input("\nEnter minimum mood (1-10): "))
                mood_max = int(input("Enter maximum mood (1-10): "))
                matching = [e for e in self.entries 
                           if mood_min <= e["mood"] <= mood_max]
                self._display_entry_list(matching, f"Entries with mood {mood_min}-{mood_max}")
            except ValueError:
                print("Invalid input. Please enter numbers for mood range.")
                
        elif choice == "4":
            # Search by tag
            tag = input("\nEnter tag to search for: ").strip().lower()
            matching = [e for e in self.entries 
                       if any(t.lower() == tag for t in e["tags"])]
            self._display_entry_list(matching, f"Entries tagged with '{tag}'")
            
        elif choice == "5":
            # Search by text
            text = input("\nEnter text to search for: ").strip().lower()
            matching = [e for e in self.entries 
                       if text in e["reflection"].lower() or 
                       text in e["prompt"].lower() or
                       any(text in a.lower() for a in e["activities"])]
            self._display_entry_list(matching, f"Entries containing '{text}'")
            
        elif choice == "6":
            self.display_menu()
            return
        
        else:
            print("Invalid choice.")
        
        # After any search, go back to view menu
        self.view_entries()
    
    def _display_entry_list(self, entries, title):
        """Display a list of entries and allow user to select one to view in detail"""
        if not entries:
            print(f"\nNo entries found for {title}.")
            input("\nPress Enter to continue...")
            return
        
        print(f"\n=== {title} ===")
        for i, entry in enumerate(entries, 1):
            date_str = entry["date"]
            mood = entry["mood"]
            
            # Get a preview of the reflection (first 40 chars)
            preview = entry["reflection"][:40] + "..." if len(entry["reflection"]) > 40 else entry["reflection"]
            
            print(f"{i}. {date_str} - Mood: {mood}/10 - {preview}")
        
        print(f"{len(entries) + 1}. Back")
        
        try:
            choice = int(input("\nSelect an entry to view (number): "))
            if 1 <= choice <= len(entries):
                self._display_entry_detail(entries[choice - 1])
            elif choice == len(entries) + 1:
                return
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    def _display_entry_detail(self, entry):
        """Display details of a single entry"""
        print("\n" + "=" * 50)
        print(f"Date: {entry['date']} at {entry['time']}")
        print(f"Mood: {entry['mood']}/10 - {entry['mood_label']}")
        print(f"Energy: {entry['energy']}/10")
        print("\nPrompt:")
        print(f"{entry['prompt']}")
        print("\nReflection:")
        print(f"{entry['reflection']}")
        
        if entry["activities"]:
            print("\nActivities:")
            for activity in entry["activities"]:
                print(f"- {activity}")
        
        if entry["tags"]:
            print("\nTags:")
            print(", ".join(entry["tags"]))
        
        if entry.get("ai_insights"):
            print("\nAI Insights:")
            print(entry["ai_insights"])
        
        print("=" * 50)
        
        # Options after viewing an entry
        print("\n1. Edit this entry")
        print("2. Delete this entry")
        print("3. Generate AI insights for this entry")
        print("4. Back")
        
        choice = input("\nWhat would you like to do? (1-4): ")
        
        if choice == "1":
            self._edit_entry(entry)
        elif choice == "2":
            self._delete_entry(entry)
        elif choice == "3":
            if not entry.get("ai_insights"):
                print("\nGenerating insights...")
                entry["ai_insights"] = self._generate_entry_insight(entry)
                self._save_entries()
            print("\n=== AI Insights ===")
            print(entry["ai_insights"])
            input("\nPress Enter to continue...")
        elif choice == "4":
            return
        else:
            print("Invalid choice.")
            self._display_entry_detail(entry)
    
    def _edit_entry(self, entry):
        """Edit an existing journal entry"""
        print("\n=== Edit Entry ===")
        print("What would you like to modify?")
        print("1. Mood rating")
        print("2. Energy rating")
        print("3. Reflection text")
        print("4. Activities")
        print("5. Tags")
        print("6. Cancel edit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == "1":
            try:
                new_mood = int(input("Enter new mood rating (1-10): "))
                if 1 <= new_mood <= 10:
                    entry["mood"] = new_mood
                    entry["mood_label"] = self.mood_labels[new_mood]
                    print("Mood updated.")
                else:
                    print("Invalid mood rating. Must be between 1 and 10.")
            except ValueError:
                print("Invalid input. Mood not changed.")
                
        elif choice == "2":
            try:
                new_energy = int(input("Enter new energy rating (1-10): "))
                if 1 <= new_energy <= 10:
                    entry["energy"] = new_energy
                    print("Energy updated.")
                else:
                    print("Invalid energy rating. Must be between 1 and 10.")
            except ValueError:
                print("Invalid input. Energy not changed.")
                
        elif choice == "3":
            print(f"Current reflection: {entry['reflection']}")
            new_text = input("Enter new reflection (or press Enter to keep current): ")
            if new_text:
                entry["reflection"] = new_text
                print("Reflection updated.")
                
        elif choice == "4":
            print(f"Current activities: {', '.join(entry['activities'])}")
            new_activities = input("Enter new activities (comma-separated): ")
            if new_activities:
                entry["activities"] = [a.strip() for a in new_activities.split(",") if a.strip()]
                print("Activities updated.")
                
        elif choice == "5":
            print(f"Current tags: {', '.join(entry['tags'])}")
            new_tags = input("Enter new tags (comma-separated): ")
            if new_tags:
                entry["tags"] = [t.strip() for t in new_tags.split(",") if t.strip()]
                print("Tags updated.")
                
        elif choice == "6":
            print("Edit canceled.")
            self._display_entry_detail(entry)
            return
            
        else:
            print("Invalid choice.")
            self._edit_entry(entry)
            return
        
        # After any edit, regenerate insights if auto-insights is enabled
        if self.preferences["auto_insights"]:
            print("Regenerating insights for updated entry...")
            entry["ai_insights"] = self._generate_entry_insight(entry)
        
        # Save changes
        self._save_entries()
        print("Entry updated successfully.")
        
        # Show the updated entry
        self._display_entry_detail(entry)
    
    def _delete_entry(self, entry):
        """Delete a journal entry"""
        confirm = input("\nAre you sure you want to delete this entry? (y/n): ").lower()
        if confirm == 'y':
            self.entries.remove(entry)
            self._save_entries()
            print("Entry deleted successfully.")
        else:
            print("Deletion canceled.")
            self._display_entry_detail(entry)
    
    def _generate_entry_insight(self, entry):
        """Generate AI insights for a journal entry"""
        prompt = f"""
        The user wrote a journal entry with the following details:
        - Date: {entry['date']}
        - Mood: {entry['mood']}/10 ({entry['mood_label']})
        - Energy: {entry['energy']}/10
        - Prompt: "{entry['prompt']}"
        - Reflection: "{entry['reflection']}"
        - Activities: {', '.join(entry['activities']) if entry['activities'] else 'None mentioned'}
        - Tags: {', '.join(entry['tags']) if entry['tags'] else 'None'}
        
        Please provide a thoughtful, empathetic reflection on this entry. Include:
        1. An observation about their mood and energy
        2. A meaningful insight about their reflection
        3. A gentle question to deepen their self-awareness
        
        Keep your response concise and supportive (150 words max).
        """
        
        return get_response(prompt, 
                          system="You are an empathetic journaling assistant who helps users gain deeper insights from their reflections.")
    
    def get_insights(self):
        """Generate analytics and AI insights from journal entries"""
        if len(self.entries) < 3:
            print("\nYou need at least 3 journal entries to generate insights.")
            input("\nPress Enter to continue...")
            self.display_menu()
            return
        
        print("\n=== Journal Insights & Analytics ===")
        print("1. Mood trends visualization")
        print("2. Activity impact analysis")
        print("3. Word cloud and themes")
        print("4. Weekly summary")
        print("5. Monthly review")
        print("6. Custom date range analysis")
        print("7. Return to main menu")
        
        choice = input("\nWhat would you like to see? (1-7): ")
        
        if choice == "1":
            self._visualize_mood_trends()
        elif choice == "2":
            self._analyze_activity_impact()
        elif choice == "3":
            self._generate_word_cloud()
        elif choice == "4":
            self._generate_weekly_summary()
        elif choice == "5":
            self._generate_monthly_review()
        elif choice == "6":
            self._custom_date_analysis()
        elif choice == "7":
            self.display_menu()
            return
        else:
            print("Invalid choice.")
        
        # Return to insights menu
        input("\nPress Enter to continue...")
        self.get_insights()
    
    def _visualize_mood_trends(self):
        """Visualize mood trends over time"""
        # Extract dates and moods
        dates = [datetime.datetime.strptime(e["date"], "%Y-%m-%d") for e in self.entries]
        moods = [e["mood"] for e in self.entries]
        energy = [e["energy"] for e in self.entries]
        
        # Create the visualization
        plt.figure(figsize=(12, 6))
        plt.plot(dates, moods, 'b-o', label='Mood')
        plt.plot(dates, energy, 'r-o', label='Energy')
        plt.axhline(y=5, color='g', linestyle='--', alpha=0.3, label='Neutral')
        
        plt.title('Mood and Energy Trends')
        plt.xlabel('Date')
        plt.ylabel('Rating (1-10)')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Format the x-axis to show dates nicely
        plt.gcf().autofmt_xdate()
        
        # Save the visualization
        viz_path = os.path.join(self.visualization_dir, f"mood_trends_{datetime.datetime.now().strftime('%Y%m%d')}.png")
        plt.savefig(viz_path)
        
        print(f"\nMood trend visualization saved to: {viz_path}")
        print("\nInsights about your mood trends:")
        
        # Calculate some basic statistics
        avg_mood = sum(moods) / len(moods)
        avg_energy = sum(energy) / len(energy)
        mood_trend = "improving" if moods[-1] > moods[0] else "declining" if moods[-1] < moods[0] else "stable"
        
        print(f"- Your average mood is {avg_mood:.1f}/10")
        print(f"- Your average energy level is {avg_energy:.1f}/10")
        print(f"- Your overall mood trend appears to be {mood_trend}")
        
        # Generate AI insights on mood trends
        if len(self.entries) >= 5:  # Need enough data for meaningful trends
            entries_text = "\n".join([
                f"Date: {e['date']}, Mood: {e['mood']}/10, Energy: {e['energy']}/10, Activities: {', '.join(e['activities'])}"
                for e in self.entries[-10:]  # Last 10 entries
            ])
            
            prompt = f"""
            Here are the user's recent journal entries with mood and energy ratings:
            
            {entries_text}
            
            Based on this data, provide:
            1. Any patterns you notice in their mood and energy levels
            2. Potential correlations between activities and mood
            3. A gentle suggestion based on these patterns
            
            Keep your response concise (150 words max).
            """
            
            insights = get_response(prompt, 
                                  system="You are an analytical journaling assistant who helps identify patterns in mood, energy, and behavior.")
            
            print("\nAI Analysis:")
            print(insights)
    
    def _analyze_activity_impact(self):
        """Analyze how different activities impact mood"""
        if not any(e.get("activities") for e in self.entries):
            print("\nNot enough activity data found in your entries.")
            return
        
        # Create a dictionary to track activities and associated moods
        activity_moods = {}
        
        # Collect data
        for entry in self.entries:
            mood = entry["mood"]
            for activity in entry.get("activities", []):
                activity = activity.lower().strip()
                if activity:
                    if activity not in activity_moods:
                        activity_moods[activity] = []
                    activity_moods[activity].append(mood)
        
        # Filter to activities with at least 2 data points
        activity_moods = {k: v for k, v in activity_moods.items() if len(v) >= 2}
        
        if not activity_moods:
            print("\nNot enough repeated activities found to analyze impact.")
            return
        
        # Calculate average mood for each activity
        activity_avg_moods = {activity: sum(moods)/len(moods) 
                             for activity, moods in activity_moods.items()}
        
        # Sort activities by average mood (highest first)
        sorted_activities = sorted(activity_avg_moods.items(), 
                                  key=lambda x: x[1], reverse=True)
        
        # Display results
        print("\n=== Activity Impact Analysis ===")
        print("Activities sorted by average mood impact:")
        
        for activity, avg_mood in sorted_activities:
            count = len(activity_moods[activity])
            print(f"- {activity.title()}: {avg_mood:.1f}/10 (mentioned {count} times)")
        
        # Visualize top activities
        top_activities = sorted_activities[:min(8, len(sorted_activities))]
        
        activities = [a[0].title() for a in top_activities]
        avg_moods = [a[1] for a in top_activities]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(activities, avg_moods, color='skyblue')
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.1f}', ha='center', va='bottom')
        
        plt.title('Activities and Their Impact on Mood')
        plt.xlabel('Activities')
        plt.ylabel('Average Mood (1-10)')
        plt.ylim(0, 10.5)  # Set y-axis limit with some padding
        plt.grid(axis='y', alpha=0.3)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Save the visualization
        viz_path = os.path.join(self.visualization_dir, f"activity_impact_{datetime.datetime.now().strftime('%Y%m%d')}.png")
        plt.savefig(viz_path)
        
        print(f"\nActivity impact visualization saved to: {viz_path}")
        
        # Generate AI insights
        activities_text = "\n".join([
            f"Activity: {activity}, Average Mood: {avg_mood:.1f}/10, Occurrences: {len(activity_moods[activity])}"
            for activity, avg_mood in sorted_activities
        ])
        
        prompt = f"""
        Here's an analysis of how different activities affect the user's mood:
        
        {activities_text}
        
        Based on this data, provide:
        1. Observations about which activities seem to have the most positive impact
        2. Suggestions for which activities they might want to prioritize
        3. A gentle question about their activity patterns
        
        Keep your response concise (150 words max).
        """
        
        insights = get_response(prompt, 
                              system="You are an analytical journaling assistant who helps identify patterns between activities and well-being.")
        
        print("\nAI Analysis:")
        print(insights)
    
    def _generate_word_cloud(self):
        """Generate a word frequency analysis of journal entries"""
        if not self.entries:
            print("\nNo journal entries found.")
            return
        
        # Combine all reflections
        all_text = " ".join([e["reflection"] for e in self.entries])
        
        # Remove common stop words (simplified)
        stop_words = ["the", "and", "a", "to", "of", "in", "i", "it", "is", "that", 
                     "was", "for", "on", "you", "he", "be", "with", "as", "by", "at", 
                     "have", "are", "this", "but", "not", "from", "had", "has", "was", 
                     "were", "they", "will", "would", "could", "should", "did", "do",
                     "does", "their", "there", "then", "than", "them", "these", "those"]
        
        # Extract words, convert to lowercase, and remove punctuation
        words = re.findall(r'\b[a-zA-Z]+\b', all_text.lower())
        
        # Filter out stop words
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Count word frequencies
        word_counts = Counter(filtered_words)
        
        # Get the top 20 most frequent words
        top_words = word_counts.most_common(20)
        
        # Display results
        print("\n=== Word Frequency Analysis ===")
        print("Most common words in your journal:")
        
        for word, count in top_words:
            print(f"- {word}: {count} occurrences")
        
        # Visualize word frequencies
        words = [w[0] for w in top_words]
        counts = [w[1] for w in top_words]
        
        plt.figure(figsize=(12, 6))
        bars = plt.barh(words[::-1], counts[::-1], color='lightgreen')  # Reverse to show highest at top
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 0.5, bar.get_y() + bar.get_height()/2., 
                    f'{width}', ha='left', va='center')
        
        plt.title('Most Common Words in Journal Entries')
        plt.xlabel('Frequency')
        plt.tight_layout()
        
        # Save the visualization
        viz_path = os.path.join(self.visualization_dir, f"word_frequency_{datetime.datetime.now().strftime('%Y%m%d')}.png")
        plt.savefig(viz_path)
        
        print(f"\nWord frequency visualization saved to: {viz_path}")
        
        # Generate AI insights on themes
        prompt = f"""
        These are the most common words in the user's journal entries:
        
        {', '.join([f"{word} ({count})" for word, count in top_words])}
        
        Based on these words, please:
        1. Identify potential themes or patterns in their journaling
        2. Suggest areas for deeper reflection
        3. Provide a gentle observation about what these themes might indicate
        
        Keep your response concise (150 words max).
        """
        
        insights = get_response(prompt, 
                              system="You are an insightful journaling assistant who helps identify themes and patterns in journal entries.")
        
        print("\nAI Theme Analysis:")
        print(insights)
    
    def _generate_weekly_summary(self):
        """Generate a weekly summary of journal entries"""
        # Get entries from the past 7 days
        today = datetime.datetime.now().date()
        week_ago = today - datetime.timedelta(days=7)
        
        weekly_entries = [e for e in self.entries 
                         if datetime.datetime.strptime(e["date"], "%Y-%m-%d").date() >= week_ago]
        
        if len(weekly_entries) < 2:
            print("\nNot enough entries in the past week for a meaningful summary.")
            return
        
        # Compile weekly data
        weekly_moods = [e["mood"] for e in weekly_entries]
        avg_mood = sum(weekly_moods) / len(weekly_moods)
        
        weekly_energy = [e["energy"] for e in weekly_entries]
        avg_energy = sum(weekly_energy) / len(weekly_energy)
        
        # Get all activities
        all_activities = []
        for entry in weekly_entries:
            all_activities.extend(entry.get("activities", []))
        
        # Count activity frequencies
        activity_counts = Counter(all_activities)
        most_common = activity_counts.most_common(5)
        
        # Display weekly summary
        print("\n=== Weekly Summary ===")
        print(f"Period: {week_ago.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}")
        print(f"Number of entries: {len(weekly_entries)}")
        print(f"Average mood: {avg_mood:.1f}/10")
        print(f"Average energy: {avg_energy:.1f}/10")
        
        if most_common:
            print("\nMost common activities:")
            for activity, count in most_common:
                print(f"- {activity}: {count} times")
        
        # Generate AI summary
        entries_text = "\n\n".join([
            f"Date: {e['date']}\nMood: {e['mood']}/10\nEnergy: {e['energy']}/10\n"
            f"Activities: {', '.join(e.get('activities', []))}\nReflection: {e['reflection']}"
            for e in weekly_entries
        ])
        
        prompt = f"""
        Here's a summary of the user's journal entries for the past week:
        
        {entries_text}
        
        Please provide a weekly reflection that includes:
        1. Notable patterns or trends in their mood and energy
        2. Observations about activities and their potential impact
        3. A gentle suggestion for the coming week
        4. A thoughtful reflection question
        
        Keep your response concise and supportive (200 words max).
        """
        
        insights = get_response(prompt, 
                              system="You are an empathetic journaling assistant who helps provide weekly summaries and insights.")
        
        print("\nAI Weekly Reflection:")
        print(insights)
    
    def _generate_monthly_review(self):
        """Generate a monthly review of journal entries"""
        # Get entries from the current month
        today = datetime.datetime.now()
        first_day = datetime.datetime(today.year, today.month, 1)
        
        # For previous month, use:
        # prev_month = first_day - datetime.timedelta(days=1)
        # first_day = datetime.datetime(prev_month.year, prev_month.month, 1)
        
        monthly_entries = [e for e in self.entries 
                          if datetime.datetime.strptime(e["date"], "%Y-%m-%d") >= first_day]
        
        if len(monthly_entries) < 3:
            print("\nNot enough entries this month for a meaningful review.")
            return
        
        # Compile monthly data
        monthly_moods = [e["mood"] for e in monthly_entries]
        avg_mood = sum(monthly_moods) / len(monthly_moods)
        high_mood = max(monthly_moods)
        low_mood = min(monthly_moods)
        
        high_entry = next(e for e in monthly_entries if e["mood"] == high_mood)
        low_entry = next(e for e in monthly_entries if e["mood"] == low_mood)
        
        # Get all activities and tags
        all_activities = []
        all_tags = []
        for entry in monthly_entries:
            all_activities.extend(entry.get("activities", []))
            all_tags.extend(entry.get("tags", []))
        
        # Count frequencies
        activity_counts = Counter(all_activities)
        tag_counts = Counter(all_tags)
        
        # Display monthly review
        print("\n=== Monthly Review ===")
        print(f"Month: {first_day.strftime('%B %Y')}")
        print(f"Number of entries: {len(monthly_entries)}")
        print(f"Average mood: {avg_mood:.1f}/10")
        print(f"Highest mood: {high_mood}/10 on {high_entry['date']}")
        print(f"Lowest mood: {low_mood}/10 on {low_entry['date']}")
        
        if activity_counts:
            print("\nTop activities this month:")
            for activity, count in activity_counts.most_common(5):
                print(f"- {activity}: {count} times")
        
        if tag_counts:
            print("\nTop themes/tags this month:")
            for tag, count in tag_counts.most_common(5):
                print(f"- {tag}: {count} times")
        
        # Generate AI review
        entries_summary = "\n".join([
            f"Date: {e['date']}, Mood: {e['mood']}/10, Energy: {e['energy']}/10, "
            f"Activities: {', '.join(e.get('activities', []))}, Tags: {', '.join(e.get('tags', []))}"
            for e in monthly_entries
        ])
        
        prompt = f"""
        Here's a summary of the user's journal entries for {first_day.strftime('%B %Y')}:
        
        {entries_summary}
        
        Please provide a monthly review that includes:
        1. Overall patterns in mood and energy
        2. Key achievements or challenges that stood out
        3. Activities that seemed most beneficial
        4. Gentle suggestions for next month
        5. A thoughtful reflection question
        
        Keep your response supportive and actionable (250 words max).
        """
        
        insights = get_response(prompt, 
                              system="You are an insightful journaling assistant who helps provide monthly reviews and insights.")
        
        print("\nAI Monthly Review:")
        print(insights)
    
    def _custom_date_analysis(self):
        """Generate insights for a custom date range"""
        print("\n=== Custom Date Range Analysis ===")
        
        # Get start date
        start_date_str = input("Enter start date (YYYY-MM-DD): ")
        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Using 30 days ago as default.")
            start_date = datetime.datetime.now().date() - datetime.timedelta(days=30)
        
        # Get end date
        end_date_str = input("Enter end date (YYYY-MM-DD) or press Enter for today: ")
        if end_date_str:
            try:
                end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Using today as default.")
                end_date = datetime.datetime.now().date()
        else:
            end_date = datetime.datetime.now().date()
        
        # Validate date range
        if start_date > end_date:
            print("Start date must be before end date. Swapping dates.")
            start_date, end_date = end_date, start_date
        
        # Filter entries by date range
        filtered_entries = [e for e in self.entries 
                           if start_date <= datetime.datetime.strptime(e["date"], "%Y-%m-%d").date() <= end_date]
        
        if len(filtered_entries) < 2:
            print(f"\nNot enough entries between {start_date} and {end_date} for analysis.")
            return
        
        # Display basic stats
        moods = [e["mood"] for e in filtered_entries]
        avg_mood = sum(moods) / len(moods)
        
        print(f"\nPeriod: {start_date} to {end_date}")
        print(f"Number of entries: {len(filtered_entries)}")
        print(f"Average mood: {avg_mood:.1f}/10")
        
        # Create mood trend visualization
        dates = [datetime.datetime.strptime(e["date"], "%Y-%m-%d") for e in filtered_entries]
        moods = [e["mood"] for e in filtered_entries]
        energy = [e["energy"] for e in filtered_entries]
        
        plt.figure(figsize=(12, 6))
        plt.plot(dates, moods, 'b-o', label='Mood')
        plt.plot(dates, energy, 'r-o', label='Energy')
        plt.axhline(y=5, color='g', linestyle='--', alpha=0.3, label='Neutral')
        
        plt.title(f'Mood and Energy Trends ({start_date} to {end_date})')
        plt.xlabel('Date')
        plt.ylabel('Rating (1-10)')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Format the x-axis to show dates nicely
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        
        # Save the visualization
        viz_path = os.path.join(self.visualization_dir, 
                              f"custom_trend_{start_date}_{end_date}.png")
        plt.savefig(viz_path)
        
        print(f"\nCustom trend visualization saved to: {viz_path}")
        
        # Generate AI insights
        entries_summary = "\n".join([
            f"Date: {e['date']}, Mood: {e['mood']}/10, Energy: {e['energy']}/10, "
            f"Activities: {', '.join(e.get('activities', []))}, Reflection: {e['reflection'][:100]}..."
            for e in filtered_entries
        ])
        
        prompt = f"""
        Here's a summary of the user's journal entries from {start_date} to {end_date}:
        
        {entries_summary}
        
        Please provide a custom period analysis that includes:
        1. Notable trends or patterns in mood and energy
        2. Key themes or recurring topics
        3. Activities that appeared to influence mood
        4. A thoughtful observation about this period
        
        Keep your response insightful and supportive (200 words max).
        """
        
        insights = get_response(prompt, 
                              system="You are an analytical journaling assistant who helps identify patterns across custom time periods.")
        
        print("\nAI Period Analysis:")
        print(insights)
    
    def manage_prompts(self):
        """Manage custom prompts"""
        print("\n=== Manage Custom Prompts ===")
        print("1. View all prompts")
        print("2. Add new prompt")
        print("3. Delete prompt")
        print("4. Return to main menu")
        
        choice = input("\nWhat would you like to do? (1-4): ")
        
        if choice == "1":
            # View all prompts
            print("\n=== Available Prompts ===")
            print("Default prompts:")
            for i, prompt in enumerate(self.default_prompts, 1):
                print(f"{i}. {prompt}")
            
            if self.custom_prompts:
                print("\nCustom prompts:")
                for i, prompt in enumerate(self.custom_prompts, 1):
                    print(f"{i}. {prompt}")
            else:
                print("\nNo custom prompts yet.")
                
        elif choice == "2":
            # Add new prompt
            new_prompt = input("\nEnter a new journal prompt: ")
            if new_prompt:
                self.custom_prompts.append(new_prompt)
                self._save_custom_prompts()
                print("Custom prompt added successfully!")
                
        elif choice == "3":
            # Delete prompt
            if not self.custom_prompts:
                print("\nNo custom prompts to delete.")
                self.manage_prompts()
                return
                
            print("\nCustom prompts:")
            for i, prompt in enumerate(self.custom_prompts, 1):
                print(f"{i}. {prompt}")
                
            try:
                idx = int(input("\nEnter the number of the prompt to delete: ")) - 1
                if 0 <= idx < len(self.custom_prompts):
                    deleted = self.custom_prompts.pop(idx)
                    self._save_custom_prompts()
                    print(f"Deleted prompt: {deleted}")
                else:
                    print("Invalid prompt number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
                
        elif choice == "4":
            self.display_menu()
            return
            
        else:
            print("Invalid choice.")
            
        # Return to prompt management menu
        self.manage_prompts()
    
    def set_goals(self):
        """Set goals and intentions"""
        print("\n=== Goals and Intentions ===")
        print("1. View current goals")
        print("2. Add new goal")
        print("3. Update goal progress")
        print("4. Delete goal")
        print("5. Generate goal suggestions")
        print("6. Return to main menu")
        
        # Load goals from file
        goals_file = os.path.join(self.journal_dir, "goals.json")
        if os.path.exists(goals_file):
            try:
                with open(goals_file, 'r') as f:
                    goals = json.load(f)
            except json.JSONDecodeError:
                goals = []
        else:
            goals = []
        
        choice = input("\nWhat would you like to do? (1-6): ")
        
        if choice == "1":
            # View current goals
            if not goals:
                print("\nNo goals found.")
            else:
                print("\n=== Current Goals ===")
                for i, goal in enumerate(goals, 1):
                    status = f"{goal['progress']}% complete" if 'progress' in goal else "Not started"
                    target_date = goal.get('target_date', 'No target date')
                    print(f"{i}. {goal['description']} - {status} - Target: {target_date}")
                    
                    if 'milestones' in goal and goal['milestones']:
                        print("   Milestones:")
                        for m in goal['milestones']:
                            check = "✓" if m.get('completed', False) else "○"
                            print(f"   {check} {m['description']}")
                
        elif choice == "2":
            # Add new goal
            print("\n=== Add New Goal ===")
            description = input("Goal description: ")
            if not description:
                print("Goal description cannot be empty.")
                self.set_goals()
                return
                
            target_date = input("Target date (YYYY-MM-DD) or leave blank: ")
            if target_date:
                try:
                    # Validate date format
                    datetime.datetime.strptime(target_date, "%Y-%m-%d")
                except ValueError:
                    print("Invalid date format. Using no target date.")
                    target_date = ""
                    
            # Create goal object
            goal = {
                "description": description,
                "created_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "progress": 0
            }
            
            if target_date:
                goal["target_date"] = target_date
                
            # Ask for milestones
            add_milestones = input("Would you like to add milestones? (y/n): ").lower()
            if add_milestones == 'y':
                milestones = []
                while True:
                    milestone = input("Enter milestone (or leave blank to finish): ")
                    if not milestone:
                        break
                    milestones.append({"description": milestone, "completed": False})
                
                if milestones:
                    goal["milestones"] = milestones
            
            # Add goal to list and save
            goals.append(goal)
            with open(goals_file, 'w') as f:
                json.dump(goals, f, indent=2)
                
            print("Goal added successfully!")
            
        elif choice == "3":
            # Update goal progress
            if not goals:
                print("\nNo goals found.")
                self.set_goals()
                return
                
            print("\n=== Update Goal Progress ===")
            for i, goal in enumerate(goals, 1):
                status = f"{goal['progress']}% complete" if 'progress' in goal else "Not started"
                print(f"{i}. {goal['description']} - {status}")
                
            try:
                idx = int(input("\nEnter the number of the goal to update: ")) - 1
                if 0 <= idx < len(goals):
                    goal = goals[idx]
                    
                    print(f"\nUpdating goal: {goal['description']}")
                    
                    # Update progress
                    try:
                        new_progress = int(input(f"Enter new progress (0-100) [current: {goal.get('progress', 0)}%]: "))
                        if 0 <= new_progress <= 100:
                            goal['progress'] = new_progress
                        else:
                            print("Progress must be between 0 and 100.")
                    except ValueError:
                        print("Invalid input. Progress not updated.")
                    
                    # Update milestones if they exist
                    if 'milestones' in goal and goal['milestones']:
                        print("\nUpdate milestones:")
                        for i, milestone in enumerate(goal['milestones'], 1):
                            status = "Completed" if milestone.get('completed', False) else "Not completed"
                            print(f"{i}. {milestone['description']} - {status}")
                            
                            update = input(f"Mark as {'not ' if milestone.get('completed', False) else ''}completed? (y/n): ").lower()
                            if update == 'y':
                                milestone['completed'] = not milestone.get('completed', False)
                    
                    # Save updated goals
                    with open(goals_file, 'w') as f:
                        json.dump(goals, f, indent=2)
                        
                    print("Goal updated successfully!")
                else:
                    print("Invalid goal number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
                
        elif choice == "4":
            # Delete goal
            if not goals:
                print("\nNo goals found.")
                self.set_goals()
                return
                
            print("\n=== Delete Goal ===")
            for i, goal in enumerate(goals, 1):
                print(f"{i}. {goal['description']}")
                
            try:
                idx = int(input("\nEnter the number of the goal to delete: ")) - 1
                if 0 <= idx < len(goals):
                    goal = goals.pop(idx)
                    
                    # Save updated goals
                    with open(goals_file, 'w') as f:
                        json.dump(goals, f, indent=2)
                        
                    print(f"Goal '{goal['description']}' deleted successfully!")
                else:
                    print("Invalid goal number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
                
        elif choice == "5":
            # Generate goal suggestions
            if not self.entries or len(self.entries) < 5:
                print("\nNot enough journal entries to generate meaningful goal suggestions.")
                self.set_goals()
                return
                
            print("\nGenerating goal suggestions based on your journal entries...")
            
            # Get recent entries
            recent_entries = self.entries[-15:]  # Last 15 entries
            entries_text = "\n\n".join([
                f"Date: {e['date']}\nMood: {e['mood']}/10\nActivities: {', '.join(e.get('activities', []))}\n"
                f"Tags: {', '.join(e.get('tags', []))}\nReflection: {e['reflection']}"
                for e in recent_entries
            ])
            
            prompt = f"""
            Here are some recent journal entries from the user:
            
            {entries_text}
            
            Based on these entries, suggest 3-5 meaningful goals or intentions that might help the user's wellbeing or personal growth. For each goal:
            1. Provide a clear, actionable description
            2. Explain briefly why this goal might be beneficial (based on patterns in their journal)
            3. Suggest 2-3 possible milestones for the goal
            
            Make the goals specific, measurable, and aligned with what seems to matter to the user.
            """
            
            suggestions = get_response(prompt, 
                                     system="You are a supportive goal-setting assistant who helps users identify meaningful goals based on their journal patterns.")
            
            print("\n=== Goal Suggestions ===")
            print(suggestions)
                
        elif choice == "6":
            self.display_menu()
            return
            
        else:
            print("Invalid choice.")
            
        # Return to goals menu
        self.set_goals()
    
    def set_preferences(self):
        """Set user preferences"""
        print("\n=== Preferences ===")
        print(f"1. Auto-generate insights: {self.preferences['auto_insights']}")
        print(f"2. Daily reminder: {self.preferences['daily_reminder']}")
        print(f"3. Reminder time: {self.preferences['reminder_time']}")
        print(f"4. Theme: {self.preferences['theme']}")
        print(f"5. Insight frequency: {self.preferences['insight_frequency']}")
        print("6. Return to main menu")
        
        choice = input("\nWhat would you like to change? (1-6): ")
        
        if choice == "1":
            # Toggle auto-insights
            self.preferences['auto_insights'] = not self.preferences['auto_insights']
            print(f"Auto-generate insights: {self.preferences['auto_insights']}")
            
        elif choice == "2":
            # Toggle daily reminder
            self.preferences['daily_reminder'] = not self.preferences['daily_reminder']
            print(f"Daily reminder: {self.preferences['daily_reminder']}")
            
        elif choice == "3":
            # Set reminder time
            time_str = input("Enter reminder time (HH:MM): ")
            try:
                # Validate time format
                datetime.datetime.strptime(time_str, "%H:%M")
                self.preferences['reminder_time'] = time_str
                print(f"Reminder time set to: {time_str}")
            except ValueError:
                print("Invalid time format. Using previous setting.")
                
        elif choice == "4":
            # Set theme
            print("\nAvailable themes:")
            themes = ["standard", "dark", "light", "colorful"]
            for i, theme in enumerate(themes, 1):
                print(f"{i}. {theme}")
                
            try:
                idx = int(input("\nSelect theme number: ")) - 1
                if 0 <= idx < len(themes):
                    self.preferences['theme'] = themes[idx]
                    print(f"Theme set to: {themes[idx]}")
                else:
                    print("Invalid theme number.")
            except ValueError:
                print("Invalid input. Theme not changed.")
                
        elif choice == "5":
            # Set insight frequency
            print("\nInsight frequency options:")
            frequencies = ["daily", "weekly", "monthly"]
            for i, freq in enumerate(frequencies, 1):
                print(f"{i}. {freq}")
                
            try:
                idx = int(input("\nSelect frequency number: ")) - 1
                if 0 <= idx < len(frequencies):
                    self.preferences['insight_frequency'] = frequencies[idx]
                    print(f"Insight frequency set to: {frequencies[idx]}")
                else:
                    print("Invalid frequency number.")
            except ValueError:
                print("Invalid input. Frequency not changed.")
                
        elif choice == "6":
            self._save_preferences()
            self.display_menu()
            return
            
        else:
            print("Invalid choice.")
            
        # Save preferences after any change
        self._save_preferences()
        
        # Return to preferences menu
        self.set_preferences()
    
    def export_journal(self):
        """Export journal to different formats"""
        if not self.entries:
            print("\nNo journal entries to export.")
            input("\nPress Enter to continue...")
            self.display_menu()
            return
            
        print("\n=== Export Journal ===")
        print("1. Export as text file")
        print("2. Export as CSV")
        print("3. Export as PDF (plain)")
        print("4. Export with visualizations")
        print("5. Return to main menu")
        
        choice = input("\nChoose export format (1-5): ")
        
        if choice == "1":
            # Export as text
            export_path = os.path.join(self.journal_dir, f"journal_export_{datetime.datetime.now().strftime('%Y%m%d')}.txt")
            
            with open(export_path, 'w') as f:
                f.write("===== JOURNAL EXPORT =====\n\n")
                
                for entry in sorted(self.entries, key=lambda e: e["date"]):
                    f.write(f"Date: {entry['date']} at {entry.get('time', '00:00')}\n")
                    f.write(f"Mood: {entry['mood']}/10 - {entry.get('mood_label', '')}\n")
                    f.write(f"Energy: {entry.get('energy', 'N/A')}/10\n\n")
                    f.write(f"Prompt: {entry.get('prompt', 'No prompt')}\n\n")
                    f.write(f"Reflection:\n{entry['reflection']}\n\n")
                    
                    if entry.get('activities'):
                        f.write(f"Activities: {', '.join(entry['activities'])}\n")
                        
                    if entry.get('tags'):
                        f.write(f"Tags: {', '.join(entry['tags'])}\n")
                        
                    f.write("\n" + "=" * 50 + "\n\n")
            
            print(f"\nJournal exported to: {export_path}")
                
        elif choice == "2":
            # Export as CSV
            export_path = os.path.join(self.journal_dir, f"journal_export_{datetime.datetime.now().strftime('%Y%m%d')}.csv")
            
            with open(export_path, 'w') as f:
                # Write header
                f.write("date,time,mood,energy,prompt,reflection,activities,tags\n")
                
                # Write entries
                for entry in self.entries:
                    date = entry['date']
                    time = entry.get('time', '')
                    mood = entry['mood']
                    energy = entry.get('energy', '')
                    prompt = entry.get('prompt', '').replace('"', '""')
                    reflection = entry['reflection'].replace('"', '""').replace('\n', ' ')
                    activities = "|".join(entry.get('activities', []))
                    tags = "|".join(entry.get('tags', []))
                    
                    f.write(f'"{date}","{time}",{mood},{energy},"{prompt}","{reflection}","{activities}","{tags}"\n')
            
            print(f"\nJournal exported to: {export_path}")
                
        elif choice == "3" or choice == "4":
            # Export as PDF (would require additional libraries like reportlab)
            print("\nPDF export would require additional libraries not included in this example.")
            print("In a full implementation, this would generate a formatted PDF document.")
            
        elif choice == "5":
            self.display_menu()
            return
            
        else:
            print("Invalid choice.")
        
        # Return to export menu
        input("\nPress Enter to continue...")
        self.export_journal()
    
    def exit_app(self):
        """Exit the application"""
        print("\nThank you for using Advanced Journal Assistant. Goodbye!")
        exit()

def main():
    """Main function to run the application"""
    journal = AdvancedJournalAssistant()
    journal.display_menu()

if __name__ == "__main__":
    main()
```

### Extension Ideas

- **Data Visualization Enhancements**: Add interactive visualizations using libraries like Plotly or Bokeh
- **Natural Language Processing**: Implement sentiment analysis to automatically detect the emotional tone of entries
- **Machine Learning Integration**: Build a recommendation system that suggests activities based on past mood correlations
- **Multiple Journaling Modes**: Add specialized templates for gratitude journaling, goal tracking, habit formation, etc.
- **Social Features**: Add optional sharing of insights (anonymized) with trusted friends or mentors
- **Integrations**: Connect with other applications like calendar, fitness trackers, or meditation apps
- **Mobile Compatibility**: Create a companion mobile app for on-the-go journaling
- **Voice Journaling**: Add speech-to-text functionality for verbal journaling
- **Export Options**: Enhanced export formats including PDF with embedded visualizations, interactive web formats
- **Cloud Sync**: Add secure cloud synchronization for access across multiple devices
- **Guided Journaling Sessions**: AI-guided journaling sessions focused on specific topics or goals

---

---

## Bot Personality Menu Generator

**Difficulty**: Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: Dictionaries, functions, menu systems

### Overview

Create a flexible menu system that allows users to interact with multiple bot personalities on demand, practicing dictionary management, function mappings, and user interface design.

### Instructions

```python
from chatcraft import get_response

def personality_menu():
    print("=== Bot Personality Menu Generator ===")
    print("Interact with various bot personalities!")
    print("Type 'exit' at any time to quit.\n")
    
    # Define different bot personalities
    def friendly_bot(prompt):
        return get_response(
            prompt,
            system="You are a friendly, helpful assistant who is always positive and encouraging. You use warm language and provide supportive responses."
        )
    
    def emoji_bot(prompt):
        return get_response(
            prompt,
            system="You are an emoji enthusiast who includes multiple relevant emojis in every response. Your tone is upbeat and playful. Make sure to use at least 3-5 emojis in each message."
        )
    
    def pirate_bot(prompt):
        return get_response(
            prompt,
            system="You are a salty pirate captain from the Golden Age of Piracy. You speak with pirate slang (arr, matey, avast, etc.) and make frequent references to sailing, treasure, and the sea. Your responses are brief and colorful."
        )
    
    def teacher_bot(prompt):
        return get_response(
            prompt,
            system="You are a patient, knowledgeable teacher who explains concepts clearly. You break down complex ideas into simple terms and use examples to illustrate points. Your tone is educational but never condescending."
        )
    
    def detective_bot(prompt):
        return get_response(
            prompt,
            system="You are a sharp-witted detective with keen analytical skills. You approach every question like a mystery to solve, looking for clues and making deductions. Your tone is contemplative and slightly dramatic, similar to classic detective novels."
        )
    
    def poet_bot(prompt):
        return get_response(
            prompt,
            system="You are a lyrical poet who often speaks in verse or uses metaphorical language. Your responses are thoughtful and artistic, with attention to the rhythm and beauty of language. Occasionally include short poems in your responses."
        )
    
    # Store bot functions in a dictionary for easy access
    bots = {
        "1": {"name": "Friendly Assistant", "function": friendly_bot, "description": "Warm and supportive"},
        "2": {"name": "Emoji Enthusiast", "function": emoji_bot, "description": "Playful with lots of emojis"},
        "3": {"name": "Pirate Captain", "function": pirate_bot, "description": "Salty sea dog with nautical flair"},
        "4": {"name": "Wise Teacher", "function": teacher_bot, "description": "Patient and educational"},
        "5": {"name": "Detective", "function": detective_bot, "description": "Analytical problem-solver"},
        "6": {"name": "Poet", "function": poet_bot, "description": "Lyrical and metaphorical"}
    }
    
    # Function to display the menu
    def show_menu():
        print("\n=== Available Bot Personalities ===")
        for key, bot_info in bots.items():
            print(f"{key}. {bot_info['name']} - {bot_info['description']}")
        print("7. Exit")
    
    # Main interaction loop
    current_bot = None
    current_bot_name = None
    
    while True:
        if current_bot is None:
            show_menu()
            choice = input("\nSelect a bot personality (1-7): ")
            
            # Exit condition
            if choice == "7" or choice.lower() == "exit":
                print("Thanks for using the Bot Personality Menu! Goodbye!")
                break
                
            if choice in bots:
                current_bot = bots[choice]["function"]
                current_bot_name = bots[choice]["name"]
                print(f"\nYou're now chatting with the {current_bot_name}!")
                
                # Welcome message from the selected bot
                welcome = current_bot("Give a brief introduction of yourself.")
                print(f"{current_bot_name}: {welcome}")
            else:
                print("Invalid choice. Please select a number from 1-7.")
                continue
        
        # Interaction with the current bot
        user_input = input("\nYou: ")
        
        # Check for exit or menu commands
        if user_input.lower() == "exit":
            print("Thanks for using the Bot Personality Menu! Goodbye!")
            break
        elif user_input.lower() == "menu":
            current_bot = None
            continue
        
        # Get response from the current bot
        response = current_bot(user_input)
        print(f"\n{current_bot_name}: {response}")
        
        # Option to change bots
        print("\nType 'menu' to switch bots or 'exit' to quit")

# Run the personality menu
if __name__ == "__main__":
    personality_menu()
```

### Extension Ideas

- Allow users to create and save their own custom bot personalities
- Add a "random" option that selects a personality at random
- Create a rating system where users can score responses
- Implement a "conversation history" feature that remembers past interactions
- Create themed conversation scenarios for different bot personalities

---

## Build Your Own Personality Bot

**Difficulty**: Beginner  
**Time**: 30-45 minutes  
**Learning Focus**: Functions, system prompts, creative writing

### Overview

Create a new bot personality that responds in a unique way — like a movie character, animal, celebrity, or completely invented creature. Students will learn how to craft system prompts that reflect specific voices or styles.

### Instructions

```python
from chatcraft import get_response

# Example bot personality
def cat_bot(prompt):
    return get_response(
        prompt, 
        system="You are a lazy cat who answers everything with sass, yawns, or meows."
    )

# Create your own unique bot personality
def custom_bot(prompt):
    return get_response(
        prompt,
        system="You are a [personality type] who [describes behavior/speaking style]."
    )

# Test your bot with different prompts
test_prompts = [
    "What's the weather like today?",
    "Explain quantum physics to me.",
    "What should I do this weekend?",
    "Tell me a joke."
]

# Choose which bot to use
my_bot = cat_bot  # Replace with your custom bot

# Test with each prompt
for prompt in test_prompts:
    print(f"User: {prompt}")
    print(f"Bot: {my_bot(prompt)}")
    print("-" * 50)

# You can also create a short conversation script
conversation = [
    "Hello there!",
    "What's your favorite food?",
    "Tell me something interesting about yourself.",
    "Goodbye!"
]

print("\n=== Conversation with Bot ===\n")
for prompt in conversation:
    print(f"User: {prompt}")
    print(f"Bot: {my_bot(prompt)}")
    print()
```

### Extension Ideas

- Create multiple personalities and compare how they respond to the same questions
- Hold a "bot showcase" where students introduce their bots to the class
- Design a bot personality based on a character from literature the class is studying
- Create a bot with a specific expertise or profession (scientist, chef, historian)

---

---

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

---

## Classroom Simulation Bot

**Difficulty**: Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: Functions, menu systems, multiple bot use

### Overview

Create a classroom simulation where students can interact with different characters or experts on various topics, practicing both coding skills and exploring different perspectives.

### Instructions

```python
from chatcraft import get_response

def classroom_simulation():
    print("=== Virtual Classroom Simulation ===")
    print("Ask questions to different characters about any topic!")
    print("Type 'exit' at any time to quit.\n")
    
    # Define different bot personalities
    def teacher_bot(prompt):
        return get_response(
            prompt,
            system="You are a knowledgeable, patient teacher who explains concepts clearly with examples. You encourage critical thinking and use analogies to simplify complex ideas. Keep explanations concise but thorough."
        )
    
    def hacker_bot(prompt):
        return get_response(
            prompt,
            system="You are an ethical hacker with expertise in cybersecurity. You explain technical concepts with a slightly rebellious attitude but always emphasize ethical practices and security. Never provide instructions for illegal activities. Use technical terminology but explain it."
        )
    
    def pirate_bot(prompt):
        return get_response(
            prompt,
            system="You are a pirate captain from the Golden Age of Piracy. You speak with pirate slang and terminology (arr, matey, etc.). Despite your rough manner, you're surprisingly knowledgeable about navigation, history, and seafaring. Keep responses brief and entertaining."
        )
    
    def scientist_bot(prompt):
        return get_response(
            prompt,
            system="You are a brilliant scientist who is excited about all fields of science. You explain scientific concepts with enthusiasm and wonder, citing relevant research and discoveries. You are factual and precise but can make complex ideas accessible."
        )
    
    # Display available characters
    def show_menu():
        print("\n=== Available Characters ===")
        print("1. Teacher - Clear explanations and educational guidance")
        print("2. Hacker - Cybersecurity and tech knowledge with attitude")
        print("3. Pirate - Nautical expertise with a swashbuckling style")
        print("4. Scientist - Enthusiastic scientific explanations")
        print("5. Exit simulation")
    
    # Main interaction loop
    while True:
        show_menu()
        choice = input("\nChoose a character (1-5): ")
        
        # Exit condition
        if choice == "5" or choice.lower() == "exit":
            print("Exiting the classroom simulation. Thanks for participating!")
            break
            
        # Select the appropriate bot based on user choice
        if choice == "1":
            bot = teacher_bot
            name = "Teacher"
        elif choice == "2":
            bot = hacker_bot
            name = "Hacker"
        elif choice == "3":
            bot = pirate_bot
            name = "Pirate Captain"
        elif choice == "4":
            bot = scientist_bot
            name = "Scientist"
        else:
            print("Invalid choice. Please enter a number from 1-5.")
            continue
        
        # Get the question from the user
        question = input(f"\nWhat would you like to ask the {name}? ")
        
        # Exit condition
        if question.lower() == "exit":
            print("Exiting the classroom simulation. Thanks for participating!")
            break
            
        # Get the response from the selected bot
        print(f"\n{name}:")
        response = bot(question)
        print(response)
        
        # Ask if they want to ask another question to the same character
        while True:
            another = input(f"\nWould you like to ask the {name} another question? (yes/no): ").lower()
            
            if another == "no" or another == "exit":
                break
            elif another == "yes":
                question = input(f"\nWhat's your next question for the {name}? ")
                
                # Exit condition
                if question.lower() == "exit":
                    print("Exiting the classroom simulation. Thanks for participating!")
                    return
                    
                print(f"\n{name}:")
                response = bot(question)
                print(response)
            else:
                print("Please answer 'yes' or 'no'.")

# Run the classroom simulation
if __name__ == "__main__":
    classroom_simulation()
```

### Extension Ideas

- Add more character types like historian, artist, or fictional character
- Create a debate mode where two characters discuss the same topic
- Add a quiz feature where characters test the user's knowledge
- Create a storyline or scenario that involves multiple characters
- Allow characters to "remember" previous interactions in the session

---

---

## Code Explainer Tool

**Difficulty**: Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: Code analysis, documentation

### Overview

Create a tool that explains code snippets and helps users understand programming concepts.

### Instructions

```python
from chatcraft import get_response
import sys

def code_explainer():
    """Tool to explain code and help with programming concepts"""
    print("=== Code Explainer Tool ===")
    print("1. Explain a code snippet")
    print("2. Simplify complex code")
    print("3. Debug problematic code")
    print("4. Learn a programming concept")
    
    choice = input("\nWhat would you like to do? ")
    
    if choice == "1":
        # Explain code
        print("\nPaste your code snippet below (type 'DONE' on a new line when finished):")
        code_lines = []
        while True:
            line = input()
            if line == "DONE":
                break
            code_lines.append(line)
        
        code = "\n".join(code_lines)
        
        detail_level = input("\nExplanation detail (brief/detailed/step-by-step): ")
        audience = input("Target audience (beginner/intermediate/advanced): ")
        
        system_prompt = f"""
        You are an expert programming tutor specializing in code explanation.
        You break down code in a way that's understandable to {audience} programmers.
        You provide {detail_level} explanations that help users truly understand the code.
        """
        
        explain_prompt = f"""
        Explain this code:
        ```
        {code}
        ```
        
        Provide a {detail_level} explanation suitable for a {audience} programmer.
        If possible, identify:
        1. The programming language
        2. What the code does
        3. Key concepts it demonstrates
        4. Any potential issues or improvements
        """
        
        print("\nAnalyzing code...")
        explanation = get_response(explain_prompt, system=system_prompt)
        
        print("\n=== Code Explanation ===")
        print(explanation)
        
    elif choice == "2":
        # Simplify complex code
        print("\nPaste the complex code below (type 'DONE' on a new line when finished):")
        code_lines = []
        while True:
            line = input()
            if line == "DONE":
                break
            code_lines.append(line)
        
        code = "\n".join(code_lines)
        
        system_prompt = """
        You are an expert in code refactoring and simplification.
        You take complex code and make it more readable while preserving functionality.
        You explain your changes clearly so the user understands the improvements.
        """
        
        simplify_prompt = f"""
        Simplify this code to make it more readable and maintainable:
        ```
        {code}
        ```
        
        Provide:
        1. A simplified version of the code
        2. An explanation of what changes you made and why
        3. How the simplified version improves upon the original
        """
        
        print("\nSimplifying code...")
        simplified = get_response(simplify_prompt, system=system_prompt)
        
        print("\n=== Simplified Code ===")
        print(simplified)
        
    elif choice == "3":
        # Debug code
        print("\nPaste the problematic code below (type 'DONE' on a new line when finished):")
        code_lines = []
        while True:
            line = input()
            if line == "DONE":
                break
            code_lines.append(line)
        
        code = "\n".join(code_lines)
        
        error = input("\nDescribe any error messages you're seeing: ")
        expected = input("What did you expect the code to do? ")
        
        system_prompt = """
        You are an expert debugging assistant who helps find and fix code issues.
        You are an expert debugging assistant who helps find and fix code issues.
        You carefully analyze code to identify bugs, logic errors, and other problems.
        You explain issues clearly and provide working solutions.
        """
        
        debug_prompt = f"""
        Debug this code:
        ```
        {code}
        ```
        
        Error information: {error}
        Expected behavior: {expected}
        
        Provide:
        1. Identification of the likely issue(s)
        2. An explanation of what's causing the problem
        3. A corrected version of the code
        4. Testing suggestions to verify the fix
        """
        
        print("\nDebugging code...")
        debug_info = get_response(debug_prompt, system=system_prompt)
        
        print("\n=== Debugging Results ===")
        print(debug_info)
        
    elif choice == "4":
        # Learn programming concept
        concept = input("\nWhat programming concept would you like to learn about? ")
        language = input("For which programming language? ")
        
        system_prompt = """
        You are a programming educator who excels at explaining technical concepts clearly.
        You use examples and analogies to make abstract ideas concrete and understandable.
        You provide practical code examples to illustrate concepts.
        """
        
        learn_prompt = f"""
        Explain the programming concept of {concept} in {language}.
        
        Include:
        1. A clear definition of the concept
        2. Why it's important and when to use it
        3. At least 2 practical code examples in {language}
        4. Common pitfalls or misconceptions
        5. Best practices when using this concept
        """
        
        print(f"\nResearching {concept} in {language}...")
        concept_explanation = get_response(learn_prompt, system=system_prompt)
        
        print(f"\n=== {concept.title()} in {language.title()} ===")
        print(concept_explanation)
    
    else:
        print("Invalid choice.")

# Run the code explainer
if __name__ == "__main__":
    code_explainer()
```

### Extension Ideas

Add functionality to generate test cases or convert code between languages.

---

---

## Creative Writing Partner

**Difficulty**: Beginner-Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: Narrative development, creative collaboration, editing

### Overview

A collaborative writing tool that helps students develop stories, poems, or essays.

### Instructions

```python
from chatcraft import get_response

def writing_partner():
    """Interactive creative writing assistant"""
    print("=== Creative Writing Partner ===")
    print("1. Story development")
    print("2. Poetry assistant")
    print("3. Essay outliner")
    print("4. Character creator")
    print("5. Writing feedback")
    
    choice = input("\nWhat would you like to do? ")
    
    if choice == "1":
        # Story development
        print("\n=== Story Development ===")
        genre = input("What genre is your story? ")
        premise = input("What's the basic premise or idea? ")
        
        system_prompt = """
        You are a creative writing coach who helps develop stories.
        You ask thoughtful questions, offer suggestions, and help organize ideas.
        You're supportive and encouraging while providing constructive guidance.
        """
        
        story_prompt = f"""
        Help the user develop a {genre} story with this premise:
        "{premise}"
        
        Provide:
        1. Three potential directions the story could take
        2. Key elements that would make this story engaging
        3. Suggestions for main characters and their motivations
        4. A potential outline for the beginning, middle, and end
        5. Questions that would help the user further develop their idea
        """
        
        print("\nDeveloping story ideas...")
        story_ideas = get_response(story_prompt, system=system_prompt)
        
        print("\n" + story_ideas)
        
        # Follow-up questions
        print("\nWould you like help with a specific aspect of your story?")
        print("1. Develop a character")
        print("2. Create a setting")
        print("3. Generate a plot twist")
        print("4. Write an opening paragraph")
        
        follow_up = input("\nChoose an option (1-4): ")
        
        if follow_up == "1":
            character_type = input("\nWhat type of character (protagonist, villain, sidekick, etc.)? ")
            
            character_prompt = f"""
            Help create a compelling {character_type} for a {genre} story with this premise:
            "{premise}"
            
            Develop:
            1. Name and brief physical description
            2. Background/history
            3. Personality traits and quirks
            4. Motivations and goals
            5. Internal and external conflicts
            """
            
            character = get_response(character_prompt, system=system_prompt)
            print("\n=== Character Profile ===")
            print(character)
            
        elif follow_up == "2":
            setting_type = input("\nWhat type of setting (time period, location, etc.)? ")
            
            setting_prompt = f"""
            Create a vivid setting for a {genre} story with this premise:
            "{premise}"
            
            The setting is: {setting_type}
            
            Include:
            1. Detailed sensory descriptions (sights, sounds, smells)
            2. Unique features of this world/place
            3. How the setting influences the story
            4. Potential conflicts arising from the setting
            """
            
            setting = get_response(setting_prompt, system=system_prompt)
            print("\n=== Setting Description ===")
            print(setting)
            
        elif follow_up == "3":
            twist_prompt = f"""
            Generate three potential plot twists for a {genre} story with this premise:
            "{premise}"
            
            For each twist, explain:
            1. What the twist is
            2. When it might occur in the story
            3. How it would change the direction of the narrative
            4. Why it would be surprising but still logical within the story
            """
            
            twists = get_response(twist_prompt, system=system_prompt)
            print("\n=== Plot Twist Ideas ===")
            print(twists)
            
        elif follow_up == "4":
            style = input("\nDescribe the writing style you'd like to use: ")
            
            opening_prompt = f"""
            Write an engaging opening paragraph for a {genre} story with this premise:
            "{premise}"
            
            Using this writing style: {style}
            
            The opening should:
            1. Hook the reader's attention
            2. Establish tone and atmosphere
            3. Introduce either a character, setting, or conflict
            4. Hint at the larger story to come
            """
            
            opening = get_response(opening_prompt, system=system_prompt)
            print("\n=== Opening Paragraph ===")
            print(opening)
    
    elif choice == "2":
        # Poetry assistant
        print("\n=== Poetry Assistant ===")
        poetry_type = input("What type of poem (sonnet, haiku, free verse, etc.)? ")
        theme = input("What theme or topic for your poem? ")
        
        system_prompt = """
        You are a poetry writing coach who helps develop beautiful, meaningful poems.
        You provide guidance on form, structure, language, and imagery.
        You're artistic and thoughtful while remaining accessible and supportive.
        """
        
        poetry_prompt = f"""
        Help the user write a {poetry_type} about {theme}.
        
        Provide:
        1. A brief explanation of the {poetry_type} form and its characteristics
        2. Suggested imagery, metaphors, or symbols related to {theme}
        3. A list of evocative words related to the theme
        4. An example first stanza or line to get started
        5. Tips for writing effectively in this form
        """
        
        print("\nGenerating poetry guidance...")
        poetry_guidance = get_response(poetry_prompt, system=system_prompt)
        
        print("\n" + poetry_guidance)
        
        # User writes poem
        print("\nWrite your poem below (type 'DONE' on a new line when finished):")
        poem_lines = []
        while True:
            line = input()
            if line == "DONE":
                break
            poem_lines.append(line)
        
        poem = "\n".join(poem_lines)
        
        # Feedback on poem
        feedback_prompt = f"""
        The user has written this {poetry_type} about {theme}:
        
        {poem}
        
        Provide constructive, supportive feedback, including:
        1. What works well in the poem
        2. Suggestions for strengthening imagery or language
        3. Ideas for revision if appropriate
        4. One or two specific lines that could be enhanced, with suggestions
        """
        
        print("\nAnalyzing your poem...")
        feedback = get_response(feedback_prompt, system=system_prompt)
        
        print("\n=== Poetry Feedback ===")
        print(feedback)
    
    elif choice == "3":
        # Essay outliner
        print("\n=== Essay Outliner ===")
        essay_type = input("What type of essay (argumentative, expository, etc.)? ")
        topic = input("What's your essay topic? ")
        
        system_prompt = """
        You are an academic writing coach who helps develop well-structured essays.
        You help organize ideas, develop arguments, and create coherent outlines.
        You provide guidance on thesis statements, evidence, and logical flow.
        """
        
        essay_prompt = f"""
        Help the user outline a {essay_type} essay on the topic:
        "{topic}"
        
        Provide:
        1. Potential thesis statements or research questions
        2. A suggested structure with main sections
        3. Key points to cover in each section
        4. Types of evidence or examples that could support each point
        5. Ideas for a strong introduction and conclusion
        """
        
        print("\nDeveloping essay outline...")
        essay_outline = get_response(essay_prompt, system=system_prompt)
        
        print("\n" + essay_outline)
        
        # Thesis refinement
        thesis = input("\nBased on these suggestions, write your thesis statement: ")
        
        refine_prompt = f"""
        Analyze this thesis statement for a {essay_type} essay on {topic}:
        
        "{thesis}"
        
        Provide feedback on:
        1. Clarity and specificity
        2. Arguability (is it something that could be supported/contested?)
        3. Scope (is it appropriately focused for an essay?)
        4. Suggested revisions if needed
        """
        
        print("\nAnalyzing thesis statement...")
        thesis_feedback = get_response(refine_prompt, system=system_prompt)
        
        print("\n=== Thesis Feedback ===")
        print(thesis_feedback)
    
    elif choice == "4":
        # Character creator
        print("\n=== Character Creator ===")
        role = input("What role will this character play (protagonist, villain, etc.)? ")
        story_type = input("What type of story is this character for? ")
        
        system_prompt = """
        You are a character development coach who helps create deep, nuanced characters.
        You ask insightful questions and provide suggestions for well-rounded character creation.
        You focus on psychology, motivation, and authentic human behavior.
        """
        
        character_prompt = f"""
        Help the user create a compelling {role} for a {story_type}.
        
        Provide:
        1. Questions to consider about the character's background
        2. Suggestions for interesting personality traits and quirks
        3. Ideas for internal and external conflicts
        4. Potential character arcs or growth journeys
        5. Tips for making the character authentic and three-dimensional
        """
        
        print("\nGenerating character development ideas...")
        character_ideas = get_response(character_prompt, system=system_prompt)
        
        print("\n" + character_ideas)
        
        # Character profile
        print("\nBased on these ideas, let's create a character profile.")
        name = input("Character name: ")
        traits = input("Three key personality traits: ")
        background = input("Brief background: ")
        goal = input("Main goal or motivation: ")
        
        profile_prompt = f"""
        Develop a complete character profile for {name}, a {role} in a {story_type}.
        
        Use this information:
        - Key traits: {traits}
        - Background: {background}
        - Goal/motivation: {goal}
        
        Create a comprehensive profile including:
        1. Physical description and appearance
        2. Detailed personality analysis
        3. Relationships with other potential characters
        4. Internal contradictions or complexities
        5. How they might respond in various situations
        6. Character arc - how they might change throughout the story
        """
        
        print("\nCreating detailed character profile...")
        profile = get_response(profile_prompt, system=system_prompt)
        
        print("\n=== Character Profile: " + name + " ===")
        print(profile)
    
    elif choice == "5":
        # Writing feedback
        print("\n=== Writing Feedback ===")
        writing_type = input("What type of writing (story, poem, essay, etc.)? ")
        
        print("\nPaste your writing below (type 'DONE' on a new line when finished):")
        writing_lines = []
        while True:
            line = input()
            if line == "DONE":
                break
            writing_lines.append(line)
        
        writing = "\n".join(writing_lines)
        
        focus_areas = input("\nWhat aspects would you like feedback on (e.g., structure, characters, language)? ")
        
        system_prompt = """
        You are a supportive writing coach who provides constructive feedback.
        You balance positive observations with suggestions for improvement.
        You're specific, actionable, and encouraging in your feedback.
        """
        
        feedback_prompt = f"""
        Provide constructive feedback on this {writing_type}:
        
        {writing}
        
        Focus on these areas: {focus_areas}
        
        Include in your feedback:
        1. Overall impression and strengths
        2. Specific suggestions for improvement in the requested areas
        3. Examples from the text with suggested revisions
        4. Next steps for revision
        
        Be supportive and constructive while providing honest feedback.
        """
        
        print("\nAnalyzing your writing...")
        feedback = get_response(feedback_prompt, system=system_prompt)
        
        print("\n=== Writing Feedback ===")
        print(feedback)
    
    else:
        print("Invalid choice.")

# Run the writing partner
if __name__ == "__main__":
    writing_partner()
```

### Extension Ideas

Add a collaborative storytelling mode where student and bot take turns adding to a story.

---

## Implementation Tips

When using these mini-projects in a classroom setting:

1. **Scaffold appropriately**: Start with simpler projects for beginners, then progress to more complex ones.
2. **Modify complexity**: Adjust project requirements based on student skill level and available time.
3. **Pair programming**: Have students work in pairs to encourage collaboration.
4. **Challenge extensions**: Provide additional challenges for students who finish early.
5. **Focus on concepts**: Emphasize the programming concepts being used rather than just creating a functioning bot.
6. **Ethical discussions**: Use these projects as opportunities to discuss AI ethics, bias, and limitations.

## Assessment Ideas

- Have students document their process in a digital portfolio
- Create a "bot showcase" where students present their creations
- Ask students to write reflections on what they learned
- Evaluate code structure, comments, and organization
- Have students peer-review each other's projects

---

*These examples are designed to be flexible starting points. Adjust and expand them to suit your specific educational needs and student skill levels.*

---

## Data Visualization Dashboard

**Difficulty**: Intermediate  
**Time**: 60-90 minutes  
**Learning Focus**: Data analysis, visualization, pandas, matplotlib

### Overview

Create an interactive dashboard that allows users to visualize and explore data relationships through various chart types. Students will learn data manipulation with pandas and visualization with matplotlib.

### Instructions

```python
from chatcraft import get_response
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import random
import os
import numpy as np

def data_dashboard():
    """Interactive data visualization dashboard for exploring datasets"""
    
    # Sample dataset (students could replace with their own CSV)
    sample_data = {
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'Temperature': [12, 14, 16, 19, 22, 25, 27, 26, 23, 19, 15, 13],
        'Rainfall': [50, 45, 35, 30, 25, 15, 10, 12, 20, 35, 40, 48],
        'Visitors': [120, 135, 190, 240, 310, 430, 590, 560, 420, 320, 190, 150]
    }
    
    # Create a DataFrame from the sample data
    df = pd.DataFrame(sample_data)
    
    print("=== Data Visualization Dashboard ===")
    print("This dashboard allows you to explore relationships in data.")
    
    # Create directory for plots if it doesn't exist
    plots_dir = "dashboard_plots"
    os.makedirs(plots_dir, exist_ok=True)
    
    while True:
        print("\nOptions:")
        print("1. View data summary")
        print("2. Line chart")
        print("3. Bar chart")
        print("4. Scatter plot")
        print("5. Get AI insights")
        print("6. Exit")
        
        choice = input("\nSelect an option (1-6): ")
        
        if choice == '1':
            # Data summary
            print("\n=== Data Summary ===")
            print(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
            print("\nColumns:")
            for column in df.columns:
                print(f"- {column}")
            
            print("\nSummary statistics:")
            print(df.describe())
            
            print("\nFirst few rows:")
            print(df.head())
            
        elif choice == '2':
            # Line chart
            print("\n=== Line Chart ===")
            print("Available columns:")
            for i, column in enumerate(df.columns[1:], 1):  # Skip 'Month' column
                print(f"{i}. {column}")
            
            column_idx = int(input("\nSelect column to plot (1-3): ")) - 1
            column_to_plot = df.columns[column_idx + 1]  # +1 to account for skipping 'Month'
            
            plt.figure(figsize=(10, 6))
            plt.plot(df['Month'], df[column_to_plot], marker='o', linewidth=2)
            plt.title(f'{column_to_plot} by Month')
            plt.xlabel('Month')
            plt.ylabel(column_to_plot)
            plt.grid(True, linestyle='--', alpha=0.7)
            
            # Save plot to file
            plot_filename = os.path.join(plots_dir, f"line_{column_to_plot.lower()}.png")
            plt.savefig(plot_filename)
            plt.close()
            
            print(f"\nLine chart created and saved as {plot_filename}")
            
        elif choice == '3':
            # Bar chart
            print("\n=== Bar Chart ===")
            print("Available columns:")
            for i, column in enumerate(df.columns[1:], 1):  # Skip 'Month' column
                print(f"{i}. {column}")
            
            column_idx = int(input("\nSelect column to plot (1-3): ")) - 1
            column_to_plot = df.columns[column_idx + 1]  # +1 to account for skipping 'Month'
            
            plt.figure(figsize=(10, 6))
            plt.bar(df['Month'], df[column_to_plot], color='skyblue', edgecolor='navy')
            plt.title(f'{column_to_plot} by Month')
            plt.xlabel('Month')
            plt.ylabel(column_to_plot)
            plt.grid(True, axis='y', linestyle='--', alpha=0.7)
            
            # Save plot to file
            plot_filename = os.path.join(plots_dir, f"bar_{column_to_plot.lower()}.png")
            plt.savefig(plot_filename)
            plt.close()
            
            print(f"\nBar chart created and saved as {plot_filename}")
            
        elif choice == '4':
            # Scatter plot
            print("\n=== Scatter Plot ===")
            print("Available columns for X-axis:")
            for i, column in enumerate(df.columns[1:], 1):  # Skip 'Month' column
                print(f"{i}. {column}")
            
            x_idx = int(input("\nSelect X-axis column (1-3): ")) - 1
            x_column = df.columns[x_idx + 1]  # +1 to account for skipping 'Month'
            
            print("\nAvailable columns for Y-axis:")
            for i, column in enumerate(df.columns[1:], 1):  # Skip 'Month' column
                if column != x_column:  # Don't show the X column again
                    print(f"{i}. {column}")
            
            y_idx = int(input("\nSelect Y-axis column (1-3): ")) - 1
            y_column = df.columns[y_idx + 1]  # +1 to account for skipping 'Month'
            
            plt.figure(figsize=(10, 6))
            plt.scatter(df[x_column], df[y_column], color='purple', alpha=0.7, s=100)
            
            # Add month labels to each point
            for i, month in enumerate(df['Month']):
                plt.annotate(month, (df[x_column][i], df[y_column][i]), 
                             xytext=(5, 5), textcoords='offset points')
            
            plt.title(f'{y_column} vs {x_column}')
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.grid(True, linestyle='--', alpha=0.7)
            
            # Optional: Add trendline
            plt.plot(np.unique(df[x_column]), 
                     np.poly1d(np.polyfit(df[x_column], df[y_column], 1))(np.unique(df[x_column])),
                     color='red', linestyle='--', alpha=0.7)
            
            # Save plot to file
            plot_filename = os.path.join(plots_dir, f"scatter_{x_column.lower()}_{y_column.lower()}.png")
            plt.savefig(plot_filename)
            plt.close()
            
            print(f"\nScatter plot created and saved as {plot_filename}")
            
        elif choice == '5':
            # AI insights
            print("\n=== AI Data Insights ===")
            
            try:
                # Prepare data summary for AI
                data_description = f"""
                Dataset with columns: {', '.join(df.columns)}
                Summary statistics:
                {df.describe().to_string()}
                
                First few rows:
                {df.head().to_string()}
                """
                
                insight_prompt = f"""
                Analyze this dataset and provide 3-5 key insights:
                {data_description}
                
                Focus on:
                1. Patterns or trends over months
                2. Correlations between variables
                3. Anomalies or interesting data points
                4. Suggestions for further analysis
                """
                
                print("Generating AI insights...")
                insights = get_response(insight_prompt)
                
                print("\n=== AI Analysis Results ===")
                print(insights)
                
            except Exception as e:
                print(f"Error getting AI insights: {e}")
                print("AI insight generation is not available.")
            
        elif choice == '6':
            print("\nExiting Dashboard. Goodbye!")
            break
            
        else:
            print("\nInvalid choice. Please select a number between 1 and 6.")

# Run the dashboard
if __name__ == "__main__":
    data_dashboard()
```

### Extension Ideas

- Add more visualization types like pie charts, histograms, or heatmaps
- Implement data filtering options to explore subsets of the data
- Add the ability to load CSV files from disk
- Create a feature to export all visualizations as a report
- Implement interactive plots using libraries like Plotly
- Add clustering or other basic data analysis techniques

---

---

## AI Persona Dialogue Simulator

**Difficulty**: Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: Function calls, lists, creativity, dialogue simulation

### Overview

Simulate interactive dialogues between multiple AI personas with different personalities or perspectives. This flexible tool enables both multi-participant panel discussions and focused one-on-one debates, allowing students to explore how different characters approach the same topics. The simulator can also be configured to run simulated interviews by selecting appropriate personas and question formats.

Simulate an interview or debate between multiple bots with different personalities or perspectives, exploring how different characters might approach the same questions or topics.

This project offers flexibility to run either panel discussions with multiple participants or focused one-on-one debates, allowing students to explore how different personas respond to the same topics.

### Instructions

```python
from chatcraft import get_response
import time

def ai_persona_dialogue_simulator():
    """
    Simulate a dialogue between multiple AI personas with different personalities,
    exploring how different characters approach the same questions or topics.
    
    This tool supports multiple dialogue formats:
    1. Panel discussion - Multiple personas exchange views with less structure
    2. Formal debate - Two personas engage in structured argument with multiple rounds
    3. Interview - One persona can be set as an "interviewer" asking questions 
       of other personas serving as "interviewees"
    """
    print("=== AI Persona Dialogue Simulator ===")
    
    # Define different bot personalities
    # Each personality has a unique perspective that influences how they respond
    bot_personalities = {
        "Professor": "You are a logical, analytical professor who values facts, research, and intellectual rigor. You speak formally and cite evidence for your claims. You believe in rational inquiry and skepticism.",
        "Coach": "You are an inspirational coach who focuses on motivation, emotional intelligence, and personal growth. You believe in the power of passion, intuition, and human potential. You speak with enthusiasm and use motivational language.",
        "Artist": "You are a creative artist who values beauty, expression, and innovation. You think metaphorically and appreciate the abstract and subjective. You believe in breaking rules to create something new. Your language is colorful and expressive.",
        "Entrepreneur": "You are a practical entrepreneur focused on results, efficiency, and real-world applications. You value solutions that work and ideas that can be implemented. You speak directly and focus on action.",
        "Dr. Logic": "You value logical reasoning and empirical evidence above all. You cite studies and statistics to support your points. You believe decisions should be made based on data, not emotions.",
        "Empathetic Emma": "You believe emotional impact and human stories are most important. You consider how policies and ideas affect real people. You speak with compassion and emphasize the human element in every issue.",
        "Traditional Tom": "You value tradition, stability, and time-tested approaches. You're skeptical of rapid change and new untested ideas. You believe in preserving what works and making careful, incremental improvements.",
        "Interviewer": "You are a professional interviewer who asks insightful, probing questions. You're curious and neutral, aiming to bring out the most interesting perspectives from others. You follow up with clarifying questions when needed."
    }
    
    # List of debate/discussion topics
    # These can be used for debates, panel discussions, or interview topics
    dialogue_topics = [
        "What's more important: creativity or logic?",
        "Is technology improving or harming society?",
        "Should education focus more on facts or skills?",
        "Is it better to be a specialist or a generalist?",
        "Are humans naturally cooperative or competitive?",
        "What's the best way to measure success in life?",
        "Should we prioritize individual freedom or collective welfare?",
        "Is artificial intelligence more likely to help or harm humanity?",
        "Should governments regulate social media platforms?"
    ]
    
    # Let user select a dialogue topic
    # TODO: Add input validation to handle non-integer inputs
    print("Choose a topic:")
    for i, question in enumerate(dialogue_topics, 1):
        print(f"{i}. {question}")
    print(f"{len(dialogue_topics) + 1}. Custom topic (enter your own)")
    
    # Input validation could be added here to handle non-integer inputs
    try:
        choice = int(input("\nEnter topic number: "))
        if choice <= 0 or choice > len(dialogue_topics) + 1:
            print("Invalid choice. Using default topic #1.")
            choice = 1
    except ValueError:
        print("Invalid input. Using default topic #1.")
        choice = 1
    
    if choice <= len(dialogue_topics):
        dialogue_topic = dialogue_topics[choice - 1]
    else:
        dialogue_topic = input("\nEnter your custom topic: ")
    
    # Choose dialogue format
    # The format affects how the personas interact with each other
    print("\nChoose dialogue format:")
    print("1. Panel discussion (multiple personas participate in an open exchange)")
    print("2. One-on-one debate (two personas engage in structured argument)")
    print("3. Interview (one persona interviews the others)")
    
    # TODO: Add input validation for format choice
    try:
        format_choice = int(input("\nEnter format number (1-3): "))
        if format_choice < 1 or format_choice > 3:
            print("Invalid format. Using panel discussion (1).")
            format_choice = 1
    except ValueError:
        print("Invalid input. Using panel discussion (1).")
        format_choice = 1
    
    # Select personas based on format
    if format_choice == 1:
        # Panel discussion - let user select multiple participants
        # This mode simulates a roundtable where each persona responds to the previous one
        print("\nAvailable personalities:")
        for i, (name, perspective) in enumerate(bot_personalities.items(), 1):
            print(f"{i}. {name}: {perspective[:60]}...")
        
        # TODO: Add more robust input validation for selections
        selections = input("\nSelect personalities (comma-separated numbers, e.g., 1,3,4): ")
        try:
            selected_indices = [int(idx.strip()) - 1 for idx in selections.split(",")]
            # Check if indices are valid
            if any(idx < 0 or idx >= len(bot_personalities) for idx in selected_indices):
                print("Some selections were invalid. Using first 3 personalities.")
                selected_indices = [0, 1, 2]
        except ValueError:
            print("Invalid input. Using first 3 personalities.")
            selected_indices = [0, 1, 2]
        
        # Get the selected personalities
        personalities = list(bot_personalities.items())
        participants = {personalities[idx][0]: personalities[idx][1] for idx in selected_indices if 0 <= idx < len(personalities)}
        
        # Panel discussions typically have fewer rounds with more participants
        rounds = 1  
        
    elif format_choice == 2:
        # One-on-one debate - let user select exactly two participants
        # This mode creates a structured back-and-forth exchange with multiple rounds
        print("\nChoose two debaters:")
        for i, (name, perspective) in enumerate(bot_personalities.items(), 1):
            print(f"{i}. {name}: {perspective[:60]}...")
        
        # TODO: Add input validation for debater selections
        try:
            choice1 = int(input("\nSelect first debater (1-8): ")) - 1
            choice2 = int(input("Select second debater (1-8): ")) - 1
            
            if choice1 < 0 or choice1 >= len(bot_personalities) or choice2 < 0 or choice2 >= len(bot_personalities):
                print("Invalid selection. Using Professor and Coach.")
                choice1, choice2 = 0, 1
        except ValueError:
            print("Invalid input. Using Professor and Coach.")
            choice1, choice2 = 0, 1
        
        # Get the selected personalities
        personalities = list(bot_personalities.items())
        participants = {
            personalities[choice1][0]: personalities[choice1][1],
            personalities[choice2][0]: personalities[choice2][1]
        }
        
        # Set number of rounds for one-on-one debate
        try:
            rounds = int(input("\nHow many response rounds? (1-5): "))
            rounds = min(max(1, rounds), 5)  # Ensure rounds is between 1 and 5
        except ValueError:
            print("Invalid input. Using 2 rounds.")
            rounds = 2
    
    else:  # format_choice == 3
        # Interview format - one interviewer, multiple interviewees
        # This mode has one persona asking questions and others responding
        print("\nSelect the interviewer:")
        for i, (name, perspective) in enumerate(bot_personalities.items(), 1):
            print(f"{i}. {name}")
        
        # TODO: Add input validation for interviewer selection
        try:
            interviewer_idx = int(input("\nSelect interviewer (1-8, recommend #8 'Interviewer'): ")) - 1
            if interviewer_idx < 0 or interviewer_idx >= len(bot_personalities):
                print("Invalid selection. Using 'Interviewer' persona.")
                # Find the Interviewer in the list
                interviewer_idx = list(bot_personalities.keys()).index("Interviewer") if "Interviewer" in bot_personalities else 0
        except ValueError:
            print("Invalid input. Using 'Interviewer' persona.")
            interviewer_idx = list(bot_personalities.keys()).index("Interviewer") if "Interviewer" in bot_personalities else 0
        
        print("\nSelect interviewees:")
        personalities = list(bot_personalities.items())
        interviewees = list(range(len(personalities)))
        interviewees.remove(interviewer_idx)  # Remove interviewer from potential interviewees
        
        for i, idx in enumerate(interviewees, 1):
            name, perspective = personalities[idx]
            print(f"{i}. {name}: {perspective[:60]}...")
        
        # TODO: Add input validation for interviewee selections
        selections = input("\nSelect interviewees (comma-separated numbers): ")
        try:
            selected = [int(idx.strip()) - 1 for idx in selections.split(",")]
            # Convert selected indices to actual personality indices
            selected_indices = [interviewees[idx] for idx in selected if 0 <= idx < len(interviewees)]
            if not selected_indices:
                print("No valid selections. Using first two personalities.")
                selected_indices = interviewees[:2]
        except ValueError:
            print("Invalid input. Using first two personalities.")
            selected_indices = interviewees[:2]
        
        # Add interviewer and interviewees to participants
        participants = {personalities[interviewer_idx][0]: personalities[interviewer_idx][1]}
        for idx in selected_indices:
            participants[personalities[idx][0]] = personalities[idx][1]
        
        # Set number of interview questions
        try:
            rounds = int(input("\nHow many interview questions? (1-5): "))
            rounds = min(max(1, rounds), 5)  # Ensure rounds is between 1 and 5
        except ValueError:
            print("Invalid input. Using 3 questions.")
            rounds = 3
    
    # Function to get response from a bot
    def get_bot_response(prompt, perspective, name):
        """Generate a response from a persona based on their perspective."""
        system_prompt = f"You are {name}. {perspective} Keep responses under 100 words to keep the dialogue flowing."
        return get_response(prompt, system=system_prompt)
    
    # Start the dialogue
    participant_names = list(participants.keys())
    print(f"\n=== Dialogue on: {dialogue_topic} ===\n")
    time.sleep(1)
    
    # Opening statements (except for interview format)
    if format_choice != 3:  # Not interview format
        print("=== Opening Statements ===\n")
        statements = {}
        
        for name, perspective in participants.items():
            print(f"{name}'s opening statement:")
            statement = get_bot_response(
                f"Give an opening statement on the topic of {dialogue_topic}",
                perspective,
                name
            )
            statements[name] = statement
            print(statement)
            print()
            time.sleep(1)
    
    # Discussion rounds based on format
    if format_choice == 1:
        # Panel discussion - each persona responds to the previous speaker
        # This creates a chain of responses where each builds on the last
        print("\n=== Panel Discussion ===\n")
        
        previous_statement = statements[participant_names[-1]]
        previous_name = participant_names[-1]
        
        for round_num in range(rounds):
            print(f"--- Round {round_num + 1} ---\n")
            
            for name in participant_names:
                time.sleep(1)
                print(f"{name} responds to {previous_name}:")
                response = get_bot_response(
                    f"The topic is: {dialogue_topic}\n{previous_name} said: '{previous_statement}'\n\nRespond to {previous_name}'s perspective with your own viewpoint.",
                    participants[name],
                    name
                )
                print(response)
                print()
                
                previous_statement = response
                previous_name = name
    
    elif format_choice == 2:
        # One-on-one debate - alternating responses with structured format
        # This simulates a formal debate with clear turns and direct responses
        print("\n=== Debate Rounds ===\n")
        
        debater1 = participant_names[0]
        debater2 = participant_names[1]
        current_statement = statements[debater2]
        
        for round_num in range(rounds):
            print(f"--- Round {round_num + 1} ---\n")
            
            # First debater responds
            time.sleep(1)
            print(f"{debater1} responds:")
            response = get_bot_response(
                f"Respond to this statement on {dialogue_topic}: '{current_statement}'",
                participants[debater1],
                debater1
            )
            print(response)
            print()
            current_statement = response
            
            # Second debater responds
            time.sleep(1)
            print(f"{debater2} responds:")
            response = get_bot_response(
                f"Respond to this statement on {dialogue_topic}: '{current_statement}'",
                participants[debater2],
                debater2
            )
            print(response)
            print()
            current_statement = response
    
    else:  # format_choice == 3
        # Interview format - interviewer asks questions, interviewees respond
        # This simulates a talk show or interview panel with one host
        print("\n=== Interview Session ===\n")
        
        interviewer = participant_names[0]
        interviewees = participant_names[1:]
        
        # Opening question about the topic
        print(f"{interviewer} asks about {dialogue_topic}:")
        question = get_bot_response(
            f"As an interviewer, ask an insightful opening question about {dialogue_topic}",
            participants[interviewer],
            interviewer
        )
        print(question)
        print()
        
        # Each interviewee responds to the opening question
        for interviewee in interviewees:
            time.sleep(1)
            print(f"{interviewee} responds:")
            response = get_bot_response(
                f"You're being interviewed. The interviewer asked: '{question}' regarding {dialogue_topic}. Respond with your perspective.",
                participants[interviewee],
                interviewee
            )
            print(response)
            print()
        
        # Additional rounds of questions
        for round_num in range(1, rounds):
            time.sleep(1)
            print(f"--- Question {round_num + 1} ---\n")
            
            # Interviewer asks a follow-up question
            print(f"{interviewer} asks:")
            question = get_bot_response(
                f"Based on the previous responses about {dialogue_topic}, ask a follow-up question that explores a different angle or aspect of the topic.",
                participants[interviewer],
                interviewer
            )
            print(question)
            print()
            
            # Each interviewee responds to the new question
            for interviewee in interviewees:
                time.sleep(1)
                print(f"{interviewee} responds:")
                response = get_bot_response(
                    f"You're being interviewed. The interviewer asked: '{question}' regarding {dialogue_topic}. Respond with your perspective.",
                    participants[interviewee],
                    interviewee
                )
                print(response)
                print()
    
    # Closing statements (except for interview format which has a special closing)
    if format_choice != 3:
        print("=== Closing Statements ===\n")
        closing_statements = {}
        
        for name, perspective in participants.items():
            time.sleep(1)
            print(f"{name}'s closing remarks:")
            closing = get_bot_response(
                f"Give a brief closing statement summarizing your position on {dialogue_topic}",
                perspective,
                name
            )
            closing_statements[name] = closing
            print(closing)
            print()
    else:
        # Special closing for interview format
        print("=== Interview Wrap-up ===\n")
        closing_statements = {}
        
        # Interviewer provides a wrap-up
        time.sleep(1)
        print(f"{interviewer}'s wrap-up:")
        interviewer_closing = get_bot_response(
            f"Provide a thoughtful wrap-up to the interview about {dialogue_topic}, thanking your guests and highlighting key insights.",
            participants[interviewer],
            interviewer
        )
        closing_statements[interviewer] = interviewer_closing
        print(interviewer_closing)
        print()
        
        # Each interviewee gives a brief final thought
        for interviewee in interviewees:
            time.sleep(1)
            print(f"{interviewee}'s final thought:")
            closing = get_bot_response(
                f"The interview about {dialogue_topic} is ending. Share a brief, impactful final thought in 1-2 sentences.",
                participants[interviewee],
                interviewee
            )
            closing_statements[interviewee] = closing
            print(closing)
            print()
    
    # Moderator summary
    print("\n=== Summary ===\n")
    
    summary_prompt = f"Summarize the dialogue on '{dialogue_topic}' between the following participants:\n\n"
    
    for name, perspective in participants.items():
        summary_prompt += f"{name}'s perspective: {perspective}\n"
        if name in closing_statements:
            summary_prompt += f"{name}'s closing: {closing_statements[name]}\n\n"
    
    if format_choice == 1:
        summary_type = "panel discussion"
    elif format_choice == 2:
        summary_type = "debate"
    else:
        summary_type = "interview"
    
    summary_prompt += f"Provide a neutral, balanced summary of this {summary_type}, highlighting the key differences in their approaches and the strengths of each perspective."
    
    moderator = get_response(
        summary_prompt,
        system="You are a neutral, insightful moderator who can identify the merits of different viewpoints. Provide a balanced summary."
    )
    
    print(moderator)

# Run the dialogue simulator
if __name__ == "__main__":
    ai_persona_dialogue_simulator()
```

### Using the Simulator for Interviews

To use this simulator specifically for interview scenarios:

1. **Select Format #3 (Interview)** - This configures one persona to act as the interviewer and others as interviewees

2. **Choose the Interviewer** - Select the "Interviewer" persona (option #8) for best results, though any persona can serve as an interviewer

3. **Select Interviewees** - Choose which personas will be interviewed on the selected topic

4. **Set Number of Questions** - Determine how many rounds of questions the interviewer will ask

5. **Interview Structure:**
   - The interviewer begins with an opening question about the topic
   - Each interviewee responds from their unique perspective
   - The interviewer asks follow-up questions in subsequent rounds
   - The session concludes with a wrap-up from the interviewer and final thoughts from interviewees

This interview format is particularly useful for:
- Exploring multiple perspectives on controversial topics
- Demonstrating how different personality types respond to the same questions
- Simulating talk show or panel interview dynamics
- Teaching questioning techniques and response patterns

### Extension Ideas

- Add a feature for the user to join as an additional participant
- Create specialized formats for specific topics (ethics, technology, etc.)
- Implement a scoring system where users rate which perspective they found most compelling
- Add follow-up questions that challenge each persona's perspective
- Create a "change my mind" feature where personas try to persuade on a controversial topic
- Allow students to create their own custom persona profiles
- Add a feature to visualize the dialogue flow and connections between arguments
- Implement a fact-checker persona that evaluates claims made during discussions
- Create a mode where personas can switch perspectives mid-dialogue to show flexibility in thinking
- Add the ability to save transcripts for later analysis or comparison

---

---

## Emotional Support Bot

**Difficulty**: Beginner-Intermediate  
**Time**: 30-45 minutes  
**Learning Focus**: Selection, text analysis, branching logic

### Overview

Create a bot that responds differently based on the user's emotional state, providing tailored support, advice, or encouragement depending on the mood expressed.

### Instructions

```python
from chatcraft import get_response

def emotional_support_bot():
    print("=== Emotional Support Bot ===")
    print("This bot will respond differently based on how you're feeling.")
    print("Type 'exit' at any time to quit.\n")
    
    # Define different bot personalities for different moods
    def therapist_bot(prompt):
        return get_response(
            prompt,
            system="You are a compassionate and empathetic therapist. Provide supportive, thoughtful responses that validate the user's feelings. Offer gentle guidance and perspective without being pushy. Keep responses brief and focused on emotional support."
        )
    
    def coach_bot(prompt):
        return get_response(
            prompt,
            system="You are an energetic and motivational coach. Be enthusiastic, positive, and encouraging. Help channel the user's good energy into productive actions or goals. Keep responses upbeat and action-oriented."
        )
    
    def chill_bot(prompt):
        return get_response(
            prompt,
            system="You are a calm, relaxed friend. Your responses are low-pressure and soothing. Suggest restful activities and ways to recharge. Keep responses brief and gentle."
        )
    
    # Main interaction loop
    while True:
        # Ask how the user is feeling
        mood = input("\nHow are you feeling today? (happy, sad, tired, anxious, exit): ").lower()
        
        # Exit condition
        if mood == "exit":
            print("Take care! Remember I'm here whenever you need to talk.")
            break
        
        # Get more details about their state
        if mood in ["happy", "sad", "tired", "anxious"]:
            details = input(f"Tell me more about why you're feeling {mood}: ")
            
            # Select appropriate bot based on mood
            if mood == "sad" or mood == "anxious":
                response = therapist_bot(f"I'm feeling {mood}. {details}")
            elif mood == "happy":
                response = coach_bot(f"I'm feeling {mood}! {details}")
            elif mood == "tired":
                response = chill_bot(f"I'm feeling {mood}. {details}")
            
            print("\nBot's response:")
            print(response)
            
            # Follow-up question based on mood
            if mood in ["sad", "anxious"]:
                follow_up = input("\nWould you like some suggestions to help you feel better? (yes/no): ")
                if follow_up.lower() == "yes":
                    suggestions = get_response(
                        f"The user is feeling {mood} because: {details}. Provide 3 specific, helpful suggestions to improve their mood.",
                        system="You are a supportive counselor offering practical, actionable advice. Format your response as a numbered list."
                    )
                    print("\nHere are some suggestions:")
                    print(suggestions)
            elif mood == "happy":
                follow_up = input("\nWould you like ideas to make the most of your good mood? (yes/no): ")
                if follow_up.lower() == "yes":
                    ideas = get_response(
                        f"The user is feeling {mood} because: {details}. Suggest 3 ways to channel this positive energy productively.",
                        system="You are an enthusiastic coach offering creative ways to use positive energy. Format your response as a numbered list."
                    )
                    print("\nHere are some ideas:")
                    print(ideas)
            elif mood == "tired":
                follow_up = input("\nWould you like some relaxation or energy tips? (relax/energy): ")
                if follow_up.lower() == "relax":
                    tips = get_response(
                        "Suggest 3 calming activities for someone who is tired and wants to relax.",
                        system="You are a wellness coach specializing in restful activities. Format your response as a numbered list."
                    )
                    print("\nRelaxation suggestions:")
                    print(tips)
                elif follow_up.lower() == "energy":
                    tips = get_response(
                        "Suggest 3 gentle ways to boost energy when feeling tired without causing stress.",
                        system="You are a wellness coach specializing in natural energy boosters. Format your response as a numbered list."
                    )
                    print("\nEnergy-boosting suggestions:")
                    print(tips)
        else:
            print("I don't recognize that mood. Please try again with happy, sad, tired, or anxious.")

# Run the emotional support bot
if __name__ == "__main__":
    emotional_support_bot()
```

### Extension Ideas

- Add more emotional states and corresponding bot personalities
- Create a mood tracking feature that remembers past interactions
- Implement sentiment analysis to detect mood from user's free text input
- Create a guided meditation or breathing exercise option
- Allow users to rate how helpful the responses were to improve the bot

---

---

## Historical Figure Chat

**Difficulty**: Beginner-Intermediate  
**Time**: 30-45 minutes  
**Learning Focus**: Historical research, character perspective, dialogue

### Overview

Chat with simulated historical figures to learn about their lives, achievements, and time periods.

### Instructions

```python
from chatcraft import get_response
import random

def historical_figure_chat():
    """Chat with simulated historical figures"""
    # Available historical figures
    figures = {
        "Albert Einstein": "physicist who developed the theory of relativity",
        "Marie Curie": "physicist and chemist who conducted pioneering research on radioactivity",
        "Leonardo da Vinci": "Renaissance polymath known for art and inventions",
        "Ada Lovelace": "mathematician and writer, known for work on Babbage's Analytical Engine",
        "Martin Luther King Jr.": "civil rights leader and advocate for nonviolent resistance",
        "Cleopatra": "last active ruler of the Ptolemaic Kingdom of Egypt",
        "Mahatma Gandhi": "leader of India's nonviolent independence movement",
        "Confucius": "Chinese philosopher and politician of the Spring and Autumn period",
        "Frida Kahlo": "Mexican painter known for her portraits and works inspired by nature",
        "Nelson Mandela": "revolutionary and political leader who served as President of South Africa"
    }
    
    print("=== Historical Figure Chat ===")
    print("Available historical figures:")
    
    figure_list = list(figures.keys())
    for i, figure in enumerate(figure_list):
        print(f"{i+1}. {figure} - {figures[figure]}")
    
    figure_choice = int(input("\nSelect a figure (1-10): ")) - 1
    figure = figure_list[figure_choice]
    
    system_prompt = f"""
    You are {figure}, {figures[figure]}.
    Respond as if you are this historical figure, with appropriate knowledge, perspective, and speaking style.
    Your knowledge is limited to what was known during your lifetime and your own experiences.
    If asked about events after your lifetime, you should acknowledge you wouldn't know about them.
    Maintain the personality, values, and worldview of {figure} based on historical accounts.
    """
    
    print(f"\n=== Conversation with {figure} ===")
    print(f"You are now chatting with {figure}. Type 'exit' to end.")
    
    # Welcome message
    greetings = [
        f"Greetings! I am {figure}. What would you like to discuss?",
        f"Hello there! {figure} at your service. How may I assist you?",
        f"Welcome! You're speaking with {figure}. What's on your mind?",
        f"Ah, a visitor! I am {figure}. What would you like to know?",
        f"Good day! It's {figure} here. What shall we talk about?"
    ]
    
    print("\n" + random.choice(greetings))
    
    # Chat loop
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == "exit":
            print(f"\n{figure}: Farewell! It was a pleasure speaking with you.")
            break
            
        response = get_response(user_input, system=system_prompt)
        print(f"\n{figure}: {response}")

# Run the historical figure chat
if __name__ == "__main__":
    historical_figure_chat()
```

### Extension Ideas

Add a "time travel interview" mode where students can interview multiple figures about the same topic or event.

---

---

## Image Gallery Creator

**Difficulty**: Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: File handling, HTML generation, metadata management, API integration

### Overview

Create a tool that generates an HTML gallery from a collection of images. The tool manages image metadata, generates descriptions (optionally with AI assistance), and creates a responsive web gallery to showcase the images.

### Instructions

```python
import os
import json
from chatcraft import get_response
from datetime import datetime

def create_image_gallery():
    """
    Creates an HTML image gallery from a collection of images.
    Students can add their own images to the 'gallery_images' folder.
    """
    
    print("=== Image Gallery Creator ===")
    
    # Create necessary directories
    image_dir = "gallery_images"
    output_dir = "gallery_output"
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if there are images to process
    image_files = [f for f in os.listdir(image_dir) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    
    if not image_files:
        print(f"No images found in '{image_dir}' folder.")
        print(f"Please add some image files (JPG, PNG, GIF) to the '{image_dir}' folder.")
        return
    
    print(f"Found {len(image_files)} images.")
    
    # Load existing metadata or create new
    metadata_file = os.path.join(output_dir, "gallery_metadata.json")
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            try:
                gallery_data = json.load(f)
            except json.JSONDecodeError:
                gallery_data = {"title": "My Image Gallery", "images": []}
    else:
        gallery_data = {"title": "My Image Gallery", "images": []}
    
    # Update gallery title
    gallery_title = input(f"Gallery title [{gallery_data['title']}]: ")
    if gallery_title:
        gallery_data["title"] = gallery_title
    
    # Process each image
    existing_images = {img["filename"]: img for img in gallery_data["images"]}
    
    for image_file in image_files:
        if image_file in existing_images:
            # Image already has metadata
            print(f"\nImage {image_file} already has metadata:")
            print(f"Title: {existing_images[image_file]['title']}")
            print(f"Description: {existing_images[image_file]['description']}")
            
            update = input("Update this image's information? (y/n): ").lower() == 'y'
            if not update:
                continue
        
        print(f"\nProcessing: {image_file}")
        
        # Get metadata for this image
        default_title = os.path.splitext(image_file)[0].replace('_', ' ').title()
        title = input(f"Image title [{default_title}]: ") or default_title
        
        description = input("Image description: ")
        
        # Optionally generate description using AI
        if not description:
            generate_ai = input("Generate description with AI? (y/n): ").lower() == 'y'
            if generate_ai:
                try:
                    prompt = f"Generate a brief, interesting description for an image named '{image_file}'. Create something imaginative based on the filename, without stating that you're guessing or that you haven't seen the image."
                    description = get_response(prompt)
                    print(f"AI-generated description: {description}")
                    use_desc = input("Use this description? (y/n): ").lower() == 'y'
                    if not use_desc:
                        description = input("Enter alternative description: ")
                except Exception as e:
                    print(f"Error generating AI description: {e}")
                    description = input("Enter description manually: ")
        
        # Add or update metadata
        image_data = {
            "filename": image_file,
            "title": title,
            "description": description,
            "date_added": datetime.now().strftime("%Y-%m-%d")
        }
        
        if image_file in existing_images:
            # Update existing entry
            for i, img in enumerate(gallery_data["images"]):
                if img["filename"] == image_file:
                    gallery_data["images"][i] = image_data
                    break
        else:
            # Add new entry
            gallery_data["images"].append(image_data)
    
    # Save updated metadata
    with open(metadata_file, 'w') as f:
        json.dump(gallery_data, f, indent=2)
    
    print("\nGenerating HTML gallery...")
    
    # Generate HTML gallery
    html_output = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{gallery_data['title']}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            text-align: center;
            color: #333;
        }}
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            grid-gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .gallery-item {{
            border-radius: 5px;
            overflow: hidden;
            box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16);
            background-color: white;
            transition: transform 0.3s;
        }}
        .gallery-item:hover {{
            transform: translateY(-5px);
        }}
        .gallery-image {{
            width: 100%;
            height: 200px;
            object-fit: cover;
        }}
        .gallery-content {{
            padding: 15px;
        }}
        .gallery-title {{
            margin-top: 0;
            color: #333;
        }}
        .gallery-description {{
            color: #666;
            font-size: 0.9em;
        }}
        .gallery-date {{
            color: #999;
            font-size: 0.8em;
            text-align: right;
            margin-top: 10px;
        }}
        footer {{
            text-align: center;
            margin-top: 30px;
            color: #999;
            font-size: 0.8em;
        }}
    </style>
</head>
<body>
    <h1>{gallery_data['title']}</h1>
    
    <div class="gallery">
"""
    
    # Add each image to the gallery
    for img in gallery_data["images"]:
        html_output += f"""        <div class="gallery-item">
            <img src="../{image_dir}/{img['filename']}" alt="{img['title']}" class="gallery-image">
            <div class="gallery-content">
                <h3 class="gallery-title">{img['title']}</h3>
                <p class="gallery-description">{img['description']}</p>
                <p class="gallery-date">Added: {img['date_added']}</p>
            </div>
        </div>
"""
    
    # Complete the HTML
    html_output += """    </div>
    
    <footer>
        <p>Created with Image Gallery Creator</p>
    </footer>
</body>
</html>
"""
    
    # Save the HTML file
    html_file = os.path.join(output_dir, "index.html")
    with open(html_file, 'w') as f:
        f.write(html_output)
    
    print(f"\nGallery created successfully!")
    print(f"HTML file saved to: {html_file}")
    print(f"Open this file in a web browser to view your gallery.")
    
    # Optional: Open the gallery in the default browser
    try_open = input("\nOpen gallery in browser? (y/n): ").lower() == 'y'
    if try_open:
        try:
            import webbrowser
            webbrowser.open('file://' + os.path.abspath(html_file))
        except Exception as e:
            print(f"Could not open browser: {e}")

# Run the gallery creator
if __name__ == "__main__":
    create_image_gallery()
```

### Extension Ideas

- Add image filtering by tags or categories
- Implement image resizing and thumbnail generation
- Create a lightbox effect for viewing full-size images
- Add EXIF data extraction to display camera information
- Implement a theme selector with different gallery styles
- Create a server-side component to host the gallery online

---

---

## Journal or Reflection Bot

**Difficulty**: Beginner-Intermediate  
**Time**: 30-45 minutes  
**Learning Focus**: Lists, memory, summarization

### Overview

Create a digital journaling assistant that helps users reflect on their experiences, identify patterns in their thoughts, and provide meaningful insights or feedback on their entries.

### Instructions

```python
from chatcraft import get_response
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

### Extension Ideas

- Add mood tracking to each entry
- Create visualizations of common themes or topics over time
- Add a guided meditation option based on journal content
- Implement a goal-setting feature that references past entries
- Create specialized journaling templates for different purposes (gratitude, productivity, etc.)

---

---

## Knowledge Quiz Bot

**Difficulty**: Beginner-Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: Lists, loops, conditionals, scoring systems

### Overview

Build a bot that quizzes the user on a topic and tracks their score.

### Instructions

```python
from chatcraft import get_response
import random

def generate_questions(topic, number_of_questions=5):
    """Generate quiz questions about a specific topic"""
    system_prompt = f"""
    Create {number_of_questions} multiple-choice quiz questions about {topic}.
    For each question, provide:
    1. The question
    2. Four possible answers labeled A, B, C, D
    3. The correct answer letter
    Format exactly as follows for each question:
    QUESTION: (the question)
    A. (option A)
    B. (option B)
    C. (option C)
    D. (option D)
    CORRECT: (correct letter)
    """
    
    response = get_response(f"Generate quiz questions about {topic}", system=system_prompt)
    questions = []
    
    # Parse the response into a structured format
    sections = response.split("QUESTION: ")
    for section in sections[1:]:  # Skip first empty section
        question_parts = section.strip().split("CORRECT: ")
        options_text = question_parts[0]
        correct_answer = question_parts[1].strip()[0]  # Just take the letter
        
        # Split the question from options
        question_lines = options_text.split("\n")
        question = question_lines[0].strip()
        options = question_lines[1:5]
        
        questions.append({
            "question": question,
            "options": options,
            "correct": correct_answer
        })
    
    return questions

def run_quiz():
    """Run an interactive quiz"""
    print("Welcome to the Quiz Bot!")
    topic = input("What topic would you like to be quizzed on? ")
    
    print(f"\nGenerating quiz questions about {topic}...")
    questions = generate_questions(topic)
    
    score = 0
    
    for i, q in enumerate(questions):
        print(f"\nQuestion {i+1}: {q['question']}")
        for option in q['options']:
            print(option)
        
        user_answer = input("\nYour answer (A, B, C, or D): ").strip().upper()
        
        if user_answer == q['correct']:
            print("Correct! ✅")
            score += 1
        else:
            print(f"Incorrect. The correct answer was {q['correct']}. ❌")
    
    print(f"\nQuiz complete! Your score: {score}/{len(questions)}")
    percentage = (score / len(questions)) * 100
    
    # Get feedback based on score
    feedback_prompt = f"The user scored {percentage}% on a quiz about {topic}. Give them a short, encouraging message based on their score."
    feedback = get_response(feedback_prompt)
    print(f"\n{feedback}")

# Run the quiz
if __name__ == "__main__":
    run_quiz()
```

### Extension Ideas

Add difficulty levels, timing, or topic categories.

---

---

## Language Translation Helper

**Difficulty**: Beginner  
**Time**: 30-45 minutes  
**Learning Focus**: Multilingual communication, cultural context

### Overview

Create a tool that helps translate text between languages and explains cultural context.

### Instructions

```python
from chatcraft import get_response

def translation_helper():
    """Tool to translate text and explain cultural context"""
    # Available languages
    languages = [
        "Spanish", "French", "German", "Italian", "Portuguese", 
        "Japanese", "Chinese", "Russian", "Arabic", "Hindi"
    ]
    
    print("=== Language Translation Helper ===")
    print("1. Translate text")
    print("2. Learn useful phrases")
    print("3. Understand cultural context")
    
    choice = input("\nWhat would you like to do? ")
    
    if choice == "1":
        # Translate text
        print("\nAvailable languages:")
        for i, lang in enumerate(languages):
            print(f"{i+1}. {lang}")
        
        source_lang = input("\nFrom which language (or English)? ")
        target_idx = int(input("Translate to which language (number)? ")) - 1
        target_lang = languages[target_idx]
        
        text = input("\nEnter the text to translate: ")
        
        system_prompt = f"""
        You are a helpful translator between {source_lang} and {target_lang}.
        Provide accurate translations while preserving meaning and tone.
        For longer texts, include both a translation and a brief summary of the content.
        """
        
        translate_prompt = f"""
        Translate this {source_lang} text to {target_lang}:
        
        "{text}"
        
        Provide:
        1. The translation
        2. Pronunciation help (if applicable)
        3. Any idiomatic expressions or culturally specific references explained
        """
        
        print(f"\nTranslating from {source_lang} to {target_lang}...")
        translation = get_response(translate_prompt, system=system_prompt)
        
        print("\n=== Translation Results ===")
        print(translation)
        
    elif choice == "2":
        # Learn useful phrases
        print("\nAvailable languages:")
        for i, lang in enumerate(languages):
            print(f"{i+1}. {lang}")
        
        lang_idx = int(input("\nWhich language (number)? ")) - 1
        language = languages[lang_idx]
        
        situation = input("\nWhat situation do you need phrases for (e.g., restaurant, shopping, emergency)? ")
        
        system_prompt = f"""
        You are a helpful language guide who provides useful {language} phrases for travelers.
        You provide accurate phrases, pronunciation guides, and cultural context.
        """
        
        phrases_prompt = f"""
        Provide useful {language} phrases for {situation} situations.
        
        Include:
        1. At least 5 essential phrases with English translations
        2. Pronunciation guide for each phrase
        3. Any cultural considerations to be aware of
        4. When and how to use each phrase appropriately
        """
        
        print(f"\nFinding useful {language} phrases for {situation}...")
        phrases = get_response(phrases_prompt, system=system_prompt)
        
        print(f"\n=== Useful {language} Phrases for {situation.title()} ===")
        print(phrases)
        
    elif choice == "3":
        # Cultural context
        print("\nAvailable cultures/regions:")
        cultures = [lang + "-speaking regions" for lang in languages]
        cultures.extend(["Latin America", "Middle East", "Southeast Asia", "Nordic countries"])
        
        for i, culture in enumerate(cultures):
            print(f"{i+1}. {culture}")
        
        culture_idx = int(input("\nWhich culture/region (number)? ")) - 1
        culture = cultures[culture_idx]
        
        aspect = input("\nWhat cultural aspect are you interested in (e.g., greetings, dining, business, gestures)? ")
        
        system_prompt = """
        You are a cultural consultant who helps people understand and respect different cultures.
        You provide accurate, nuanced information about cultural practices, values, and etiquette.
        """
        
        culture_prompt = f"""
        Explain important aspects of {aspect} in {culture}.
        
        Include:
        1. Key cultural norms and expectations
        2. Do's and don'ts to be aware of
        3. How practices might differ from Western/American norms
        4. Any regional variations to be aware of
        5. Historical or social context that helps explain these practices
        """
        
        print(f"\nResearching {aspect} in {culture}...")
        cultural_info = get_response(culture_prompt, system=system_prompt)
        
        print(f"\n=== {aspect.title()} in {culture} ===")
        print(cultural_info)
    
    else:
        print("Invalid choice.")

# Run the translation helper
if __name__ == "__main__":
    translation_helper()
```

### Extension Ideas

Add a conversation practice mode where students can simulate dialogues in another language.

---

---

## Mood Journal Assistant

**Difficulty**: Beginner-Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: File I/O, date handling, text analysis

### Overview

Create a journaling assistant that helps users track moods and reflect on patterns.

### Instructions

```python
from chatcraft import get_response
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

### Extension Ideas

Add mood tracking visualizations or goal-setting features.

---

---

## PDF Question Answering Chatbot

**Difficulty**: Intermediate-Advanced  
**Time**: 60-90 minutes  
**Learning Focus**: Document processing, natural language understanding, information retrieval

### Overview

Create a chatbot that can answer questions from a PDF document. This project teaches students how to extract and process text from PDFs and use AI to retrieve relevant information based on user queries.

### Instructions

```python
import os
import sys
import fitz  # PyMuPDF
from chatcraft import get_response

class PDFChatbot:
    """A chatbot that can answer questions about PDF documents."""
    
    def __init__(self):
        self.pdf_file = None
        self.pdf_text = ""
        self.context_size = 5000  # Max context size to send to the AI
    
    def load_pdf(self, file_path):
        """Load and extract text from a PDF file."""
        try:
            if not os.path.exists(file_path):
                print(f"Error: File '{file_path}' not found.")
                return False
            
            self.pdf_file = file_path
            
            # Open the PDF
            doc = fitz.open(file_path)
            
            # Extract text from all pages
            full_text = []
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                full_text.append(page.get_text())
            
            self.pdf_text = "\n".join(full_text)
            
            # Print document stats
            print(f"\nDocument loaded: {os.path.basename(file_path)}")
            print(f"Number of pages: {len(doc)}")
            print(f"Total characters: {len(self.pdf_text)}")
            
            # Print a preview
            preview_length = min(200, len(self.pdf_text))
            print(f"\nPreview:\n{self.pdf_text[:preview_length]}...")
            
            return True
            
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return False
    
    def summarize_document(self):
        """Generate a summary of the document."""
        if not self.pdf_text:
            print("Error: No document loaded. Please load a PDF first.")
            return
        
        print("\nGenerating document summary...")
        
        # Create a prompt for the AI
        prompt = f"""
        Please provide a concise summary of the following document:
        
        {self.pdf_text[:5000]}  # Send only the first part if the document is large
        
        Include:
        1. Main topics and themes
        2. Key points or arguments
        3. Important entities mentioned
        4. Document structure overview
        
        Keep the summary under 300 words.
        """
        
        try:
            summary = get_response(prompt)
            print("\n=== Document Summary ===")
            print(summary)
        except Exception as e:
            print(f"Error generating summary: {e}")
    
    def answer_question(self, question):
        """Answer a question about the document."""
        if not self.pdf_text:
            print("Error: No document loaded. Please load a PDF first.")
            return
        
        if not question:
            print("Error: No question provided.")
            return
        
        print(f"\nAnswering: {question}")
        
        # Create a prompt for the AI
        prompt = f"""
        Document text:
        {self.pdf_text[:self.context_size]}
        
        Question: {question}
        
        Please answer the question based only on the information provided in the document.
        If the answer cannot be found in the document, state that clearly.
        Provide page numbers or sections if you can determine them from the context.
        """
        
        try:
            answer = get_response(prompt)
            print("\n=== Answer ===")
            print(answer)
        except Exception as e:
            print(f"Error generating answer: {e}")
    
    def extract_key_information(self):
        """Extract key information from the document."""
        if not self.pdf_text:
            print("Error: No document loaded. Please load a PDF first.")
            return
        
        print("\nExtracting key information...")
        
        # Create a prompt for the AI
        prompt = f"""
        Please extract and organize key information from this document:
        
        {self.pdf_text[:self.context_size]}
        
        Extract the following (if present):
        1. Dates and deadlines
        2. Names and organizations
        3. Numerical data or statistics
        4. Definitions or technical terms
        5. Action items or requirements
        
        Format the information in clear categories with brief explanations.
        """
        
        try:
            key_info = get_response(prompt)
            print("\n=== Key Information ===")
            print(key_info)
        except Exception as e:
            print(f"Error extracting information: {e}")
    
    def find_related_topics(self, topic):
        """Find information related to a specific topic in the document."""
        if not self.pdf_text:
            print("Error: No document loaded. Please load a PDF first.")
            return
        
        if not topic:
            print("Error: No topic provided.")
            return
        
        print(f"\nFinding information related to: {topic}")
        
        # Create a prompt for the AI
        prompt = f"""
        Document text:
        {self.pdf_text[:self.context_size]}
        
        Please find and extract all information related to the topic "{topic}" from the document.
        Include any definitions, explanations, examples, or references related to this topic.
        Organize the information in a structured way and indicate where in the document it appears if possible.
        If the topic is not mentioned in the document, please state that clearly.
        """
        
        try:
            related_info = get_response(prompt)
            print(f"\n=== Information Related to '{topic}' ===")
            print(related_info)
        except Exception as e:
            print(f"Error finding related information: {e}")
    
    def run(self):
        """Run the PDF chatbot interface."""
        print("=== PDF Question Answering Chatbot ===")
        print("This chatbot can answer questions about PDF documents.")
        
        while True:
            print("\nOptions:")
            print("1. Load a PDF document")
            print("2. Get document summary")
            print("3. Ask a question")
            print("4. Extract key information")
            print("5. Find related topics")
            print("6. Exit")
            
            choice = input("\nSelect an option (1-6): ")
            
            if choice == '1':
                # Load PDF
                file_path = input("\nEnter the path to a PDF file: ")
                self.load_pdf(file_path)
                
            elif choice == '2':
                # Summarize document
                self.summarize_document()
                
            elif choice == '3':
                # Ask a question
                if not self.pdf_text:
                    print("Please load a PDF document first (option 1).")
                    continue
                    
                question = input("\nEnter your question about the document: ")
                self.answer_question(question)
                
            elif choice == '4':
                # Extract key information
                self.extract_key_information()
                
            elif choice == '5':
                # Find related topics
                if not self.pdf_text:
                    print("Please load a PDF document first (option 1).")
                    continue
                    
                topic = input("\nEnter a topic to find in the document: ")
                self.find_related_topics(topic)
                
            elif choice == '6':
                # Exit
                print("\nExiting PDF Chatbot. Goodbye!")
                break
                
            else:
                print("Invalid choice. Please select a number between 1 and 6.")

# Run the chatbot
if __name__ == "__main__":
    chatbot = PDFChatbot()
    chatbot.run()
```

### Extension Ideas

- Add support for multiple document formats (DOCX, TXT, etc.)
- Implement semantic search to find specific information more efficiently
- Create a feature to compare information across multiple documents
- Add a citation generator for referencing document content
- Build a web interface using Flask or Streamlit
- Implement document chunking for handling very large documents

---

## Implementation Tips

When using these advanced mini-projects in a classroom setting:

1. **Scaffold appropriately**: Start with simpler projects for beginners, then progress to more complex ones.
2. **Modify complexity**: Adjust project requirements based on student skill level and available time.
3. **Pair programming**: Have students work in pairs to encourage collaboration.
4. **Challenge extensions**: Provide additional challenges for students who finish early.
5. **Focus on concepts**: Emphasize the programming concepts being used rather than just creating a functioning application.
6. **Ethical discussions**: Use these projects as opportunities to discuss AI ethics, bias, and limitations.

## Assessment Ideas

- Have students document their process in a digital portfolio
- Create a "project showcase" where students present their creations
- Ask students to write reflections on what they learned
- Evaluate code structure, comments, and organization
- Have students peer-review each other's projects

---

*These examples are designed to be flexible starting points. Adjust and expand them to suit your specific educational needs and student skill levels.*

---

## Personality Bot Creator

**Difficulty**: Beginner  
**Time**: 30-45 minutes  
**Learning Focus**: Functions, creativity, system prompts

### Overview

Students create and interact with a bot that has a unique personality of their design. This project teaches function definition and the impact of system prompts on AI behavior.

### Instructions

```python
from chatcraft import get_response

# Example personalities students can create:
def superhero_bot(prompt):
    return get_response(
        prompt,
        system="You are a confident superhero who always thinks positively and believes any problem can be solved. You occasionally reference your superpowers and heroic deeds.",
        personality="superhero"
    )

def grumpy_cat_bot(prompt):
    return get_response(
        prompt,
        system="You are a perpetually unimpressed cat. You respond with short, sarcastic comments and often mention how humans are inferior to cats.",
        personality="grumpy"
    )

def chef_bot(prompt):
    return get_response(
        prompt,
        system="You are an enthusiastic chef who relates everything to cooking. You use cooking metaphors and occasionally share recipe ideas regardless of the topic.",
        personality="chef"
    )

# Test your bot with various prompts
test_prompts = [
    "How's the weather today?",
    "Can you help me with my homework?",
    "What's the meaning of life?",
    "Tell me about yourself."
]

# Choose which bot to use
my_bot = superhero_bot  # Change to your custom bot

# Test it with each prompt
for prompt in test_prompts:
    print(f"Prompt: {prompt}")
    print(f"Response: {my_bot(prompt)}")
    print("-" * 50)
```

### Extension Ideas

Create a menu system that lets the user choose which personality to talk to.

---

---

## Smart To-Do List

**Difficulty**: Intermediate  
**Time**: 60-75 minutes  
**Learning Focus**: Data structures, file I/O, date handling, AI assistance

### Overview

Build a smart to-do list application that helps users organize tasks with categories, priorities, and due dates. The application provides AI-assisted recommendations for task management and organization.

### Instructions

```python
import os
import json
from datetime import datetime, timedelta
from chatcraft import get_response

class SmartTodoList:
    """
    A smart to-do list that can categorize tasks, set priorities, 
    track due dates, and provide AI-assisted task management.
    """
    
    def __init__(self):
        self.tasks = []
        self.categories = ["Work", "School", "Personal", "Shopping", "Health", "Other"]
        self.priorities = ["High", "Medium", "Low"]
        self.data_dir = "todo_data"
        self.data_file = os.path.join(self.data_dir, "tasks.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Load existing tasks if available
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from the data file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.tasks = json.load(f)
                print(f"Loaded {len(self.tasks)} tasks from {self.data_file}")
            except json.JSONDecodeError:
                print("Error reading tasks file. Starting with empty task list.")
                self.tasks = []
        else:
            print("No existing tasks file found. Starting with empty task list.")
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to the data file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)
        print(f"Saved {len(self.tasks)} tasks to {self.data_file}")
    
    def add_task(self):
        """Add a new task to the list."""
        print("\n=== Add New Task ===")
        
        # Get task details
        title = input("Task title: ")
        
        # Select category
        print("\nCategories:")
        for i, category in enumerate(self.categories, 1):
            print(f"{i}. {category}")
        
        category_choice = input(f"Select category (1-{len(self.categories)}): ")
        try:
            category_idx = int(category_choice) - 1
            category = self.categories[category_idx]
        except (ValueError, IndexError):
            print("Invalid category selection. Using 'Other'.")
            category = "Other"
        
        # Select priority
        print("\nPriorities:")
        for i, priority in enumerate(self.priorities, 1):
            print(f"{i}. {priority}")
        
        priority_choice = input(f"Select priority (1-{len(self.priorities)}): ")
        try:
            priority_idx = int(priority_choice) - 1
            priority = self.priorities[priority_idx]
        except (ValueError, IndexError):
            print("Invalid priority selection. Using 'Medium'.")
            priority = "Medium"
        
        # Set due date
        due_date = None
        has_due_date = input("\nDoes this task have a due date? (y/n): ").lower() == 'y'
        
        if has_due_date:
            date_format = "%Y-%m-%d"
            date_input = input("Enter due date (YYYY-MM-DD) or relative (e.g., 'tomorrow', '3 days'): ")
            
            try:
                # Parse relative dates
                if date_input.lower() == 'today':
                    due_date = datetime.now().strftime(date_format)
                elif date_input.lower() == 'tomorrow':
                    due_date = (datetime.now() + timedelta(days=1)).strftime(date_format)
                elif 'days' in date_input.lower():
                    # Parse "X days" format
                    try:
                        days = int(date_input.split()[0])
                        due_date = (datetime.now() + timedelta(days=days)).strftime(date_format)
                    except (ValueError, IndexError):
                        print("Could not parse relative date. Please enter a specific date.")
                else:
                    # Try to parse as YYYY-MM-DD
                    due_date = datetime.strptime(date_input, date_format).strftime(date_format)
            except ValueError:
                print("Invalid date format. Due date will not be set.")
        
        # Add notes
        notes = input("\nAdd any notes (optional): ")
        
        # Create task object
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "category": category,
            "priority": priority,
            "due_date": due_date,
            "notes": notes,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Add to task list
        self.tasks.append(task)
        print(f"\nTask '{title}' added successfully!")
        
        # Save updated tasks
        self.save_tasks()
    
    def view_tasks(self, show_completed=False):
        """Display tasks based on filters."""
        if not self.tasks:
            print("\nNo tasks found.")
            return
        
        filtered_tasks = [t for t in self.tasks if t["completed"] == show_completed]
        
        if not filtered_tasks:
            status = "completed" if show_completed else "pending"
            print(f"\nNo {status} tasks found.")
            return
        
        # Sort tasks: first by due date (None at the end), then by priority
        def sort_key(task):
            # Priority order: High, Medium, Low
            priority_order = {"High": 0, "Medium": 1, "Low": 2}
            
            # Sort by due date first (None/null dates come last)
            if task["due_date"]:
                return (0, task["due_date"], priority_order.get(task["priority"], 1))
            else:
                return (1, "9999-99-99", priority_order.get(task["priority"], 1))
        
        sorted_tasks = sorted(filtered_tasks, key=sort_key)
        
        # Display tasks
        status = "Completed" if show_completed else "Pending"
        print(f"\n=== {status} Tasks ===")
        
        for i, task in enumerate(sorted_tasks, 1):
            due_str = f"Due: {task['due_date']}" if task['due_date'] else "No due date"
            
            # Add warning for tasks due today or overdue
            warning = ""
            if task['due_date']:
                try:
                    due_date = datetime.strptime(task['due_date'], "%Y-%m-%d").date()
                    today = datetime.now().date()
                    
                    if due_date < today and not task['completed']:
                        warning = " [OVERDUE!]"
                    elif due_date == today and not task['completed']:
                        warning = " [DUE TODAY!]"
                except ValueError:
                    pass
            
            print(f"{i}. [{task['priority']}] {task['title']}{warning} - {due_str} ({task['category']})")
        
        # Return the sorted tasks for selection
        return sorted_tasks
    
    def toggle_task_status(self):
        """Mark a task as completed or pending."""
        print("\n=== Toggle Task Status ===")
        
        # Show pending tasks first
        pending_tasks = self.view_tasks(show_completed=False)
        
        if pending_tasks:
            # Show completed tasks
            print("\n=== Completed Tasks ===")
            completed_tasks = self.view_tasks(show_completed=True)
            
            # Ask which list to toggle from
            toggle_from = input("\nToggle task from (p)ending or (c)ompleted list? ").lower()
            
            if toggle_from == 'p' and pending_tasks:
                task_list = pending_tasks
                current_status = False
            elif toggle_from == 'c' and completed_tasks:
                task_list = completed_tasks
                current_status = True
            else:
                print("Invalid selection or no tasks in that category.")
                return
            
            # Get task number
            task_num = input(f"Enter task number to toggle (1-{len(task_list)}): ")
            try:
                idx = int(task_num) - 1
                selected_task = task_list[idx]
                
                # Find this task in the main task list and toggle its status
                for task in self.tasks:
                    if task["id"] == selected_task["id"]:
                        task["completed"] = not current_status
                        status = "completed" if task["completed"] else "pending"
                        print(f"\nTask '{task['title']}' marked as {status}.")
                        break
                
                # Save updated tasks
                self.save_tasks()
                
            except (ValueError, IndexError):
                print("Invalid task number.")
    
    def edit_task(self):
        """Edit an existing task."""
        print("\n=== Edit Task ===")
        
        # Show all tasks for selection
        print("\nAll Tasks:")
        all_tasks = self.tasks.copy()
        
        # Sort tasks by completion status, then by other criteria
        def sort_key(task):
            return (task["completed"], task.get("due_date", "9999-99-99"), task["priority"])
        
        sorted_tasks = sorted(all_tasks, key=sort_key)
        
        for i, task in enumerate(sorted_tasks, 1):
            status = "✓" if task["completed"] else "☐"
            due_str = f"Due: {task['due_date']}" if task['due_date'] else "No due date"
            print(f"{i}. {status} [{task['priority']}] {task['title']} - {due_str} ({task['category']})")
        
        # Get task to edit
        task_num = input(f"\nEnter task number to edit (1-{len(sorted_tasks)}): ")
        try:
            idx = int(task_num) - 1
            selected_task = sorted_tasks[idx]
            
            print(f"\nEditing task: {selected_task['title']}")
            
            # Get updated values
            title = input(f"Title [{selected_task['title']}]: ") or selected_task['title']
            
            # Select category
            print("\nCategories:")
            for i, category in enumerate(self.categories, 1):
                print(f"{i}. {category}")
            
            category_choice = input(f"Select category [current: {selected_task['category']}]: ")
            if category_choice:
                try:
                    category_idx = int(category_choice) - 1
                    category = self.categories[category_idx]
                except (ValueError, IndexError):
                    print("Invalid category selection. Keeping current category.")
                    category = selected_task['category']
            else:
                category = selected_task['category']
            
            # Select priority
            print("\nPriorities:")
            for i, priority in enumerate(self.priorities, 1):
                print(f"{i}. {priority}")
            
            priority_choice = input(f"Select priority [current: {selected_task['priority']}]: ")
            if priority_choice:
                try:
                    priority_idx = int(priority_choice) - 1
                    priority = self.priorities[priority_idx]
                except (ValueError, IndexError):
                    print("Invalid priority selection. Keeping current priority.")
                    priority = selected_task['priority']
            else:
                priority = selected_task['priority']
            
            # Update due date
            current_due = selected_task['due_date'] or "None"
            due_choice = input(f"Update due date? Current: {current_due} (y/n): ").lower()
            
            if due_choice == 'y':
                date_format = "%Y-%m-%d"
                date_input = input("Enter due date (YYYY-MM-DD) or relative (e.g., 'tomorrow', '3 days'): ")
                
                try:
                    # Parse relative dates
                    if date_input.lower() == 'today':
                        due_date = datetime.now().strftime(date_format)
                    elif date_input.lower() == 'tomorrow':
                        due_date = (datetime.now() + timedelta(days=1)).strftime(date_format)
                    elif 'days' in date_input.lower():
                        # Parse "X days" format
                        try:
                            days = int(date_input.split()[0])
                            due_date = (datetime.now() + timedelta(days=days)).strftime(date_format)
                        except (ValueError, IndexError):
                            print("Could not parse relative date. Keeping current due date.")
                            due_date = selected_task['due_date']
                    elif date_input.lower() in ('none', 'remove', 'clear'):
                        due_date = None
                    else:
                        # Try to parse as YYYY-MM-DD
                        due_date = datetime.strptime(date_input, date_format).strftime(date_format)
                except ValueError:
                    print("Invalid date format. Keeping current due date.")
                    due_date = selected_task['due_date']
            else:
                due_date = selected_task['due_date']
            
            # Update notes
            current_notes = selected_task['notes'] or "None"
            notes_choice = input(f"Update notes? Current: {current_notes} (y/n): ").lower()
            
            if notes_choice == 'y':
                notes = input("Enter new notes: ")
            else:
                notes = selected_task['notes']
            
            # Find this task in the main task list and update it
            for task in self.tasks:
                if task["id"] == selected_task["id"]:
                    task["title"] = title
                    task["category"] = category
                    task["priority"] = priority
                    task["due_date"] = due_date
                    task["notes"] = notes
                    print(f"\nTask '{title}' updated successfully!")
                    break
            
            # Save updated tasks
            self.save_tasks()
            
        except (ValueError, IndexError):
            print("Invalid task number.")
    
    def delete_task(self):
        """Delete a task from the list."""
        print("\n=== Delete Task ===")
        
        # Show all tasks for selection
        print("\nAll Tasks:")
        all_tasks = self.tasks.copy()
        
        # Sort tasks by completion status, then by other criteria
        def sort_key(task):
            return (task["completed"], task.get("due_date", "9999-99-99"), task["priority"])
        
        sorted_tasks = sorted(all_tasks, key=sort_key)
        
        for i, task in enumerate(sorted_tasks, 1):
            status = "✓" if task["completed"] else "☐"
            due_str = f"Due: {task['due_date']}" if task['due_date'] else "No due date"
            print(f"{i}. {status} [{task['priority']}] {task['title']} - {due_str} ({task['category']})")
        
        # Get task to delete
        task_num = input(f"\nEnter task number to delete (1-{len(sorted_tasks)}): ")
        try:
            idx = int(task_num) - 1
            selected_task = sorted_tasks[idx]
            
            # Confirm deletion
            confirm = input(f"Are you sure you want to delete '{selected_task['title']}'? (y/n): ").lower()
            
            if confirm == 'y':
                # Remove task from list
                self.tasks = [t for t in self.tasks if t["id"] != selected_task["id"]]
                print(f"\nTask '{selected_task['title']}' deleted successfully!")
                
                # Save updated tasks
                self.save_tasks()
            else:
                print("Deletion cancelled.")
            
        except (ValueError, IndexError):
            print("Invalid task number.")
    
    def get_ai_recommendations(self):
        """Get AI-assisted recommendations for task management."""
        if not self.tasks:
            print("\nNo tasks found. Please add some tasks first.")
            return
        
        print("\n=== AI Task Management Recommendations ===")
        print("Analyzing your tasks...")
        
        try:
            # Prepare task data for AI
            today = datetime.now().date()
            
            # Count tasks by category
            category_counts = {}
            for task in self.tasks:
                cat = task["category"]
                if cat in category_counts:
                    category_counts[cat] += 1
                else:
                    category_counts[cat] = 1
            
            # Count overdue tasks
            overdue_tasks = []
            for task in self.tasks:
                if task["due_date"] and not task["completed"]:
                    try:
                        due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                        if due_date < today:
                            overdue_tasks.append({
                                "title": task["title"],
                                "due_date": task["due_date"],
                                "days_overdue": (today - due_date).days,
                                "priority": task["priority"]
                            })
                    except ValueError:
                        pass
            
            # Get tasks due today
            today_tasks = []
            for task in self.tasks:
                if task["due_date"] and not task["completed"]:
                    try:
                        due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                        if due_date == today:
                            today_tasks.append({
                                "title": task["title"],
                                "priority": task["priority"],
                                "category": task["category"]
                            })
                    except ValueError:
                        pass
            
            # Get high priority tasks
            high_priority = []
            for task in self.tasks:
                if task["priority"] == "High" and not task["completed"]:
                    high_priority.append({
                        "title": task["title"],
                        "due_date": task["due_date"],
                        "category": task["category"]
                    })
            
            # Create prompt for AI
            prompt = f"""
            Based on the following task data, please provide helpful task management recommendations:
            
            Task summary:
            - Total tasks: {len(self.tasks)}
            - Completed tasks: {sum(1 for t in self.tasks if t["completed"])}
            - Pending tasks: {sum(1 for t in self.tasks if not t["completed"])}
            
            Category breakdown: {category_counts}
            
            Overdue tasks ({len(overdue_tasks)}):
            {overdue_tasks if overdue_tasks else "None"}
            
            Tasks due today ({len(today_tasks)}):
            {today_tasks if today_tasks else "None"}
            
            High priority pending tasks ({len(high_priority)}):
            {high_priority if high_priority else "None"}
            
            Please provide:
            1. A prioritized action plan for the next 24 hours
            2. Task management tips based on the current workload
            3. Suggestions for which tasks to focus on first
            
            Keep your response friendly, practical and under 300 words.
            """
            
            # Get AI recommendations
            recommendations = get_response(prompt)
            print("\n" + recommendations)
            
        except Exception as e:
            print(f"Error getting AI recommendations: {e}")
            print("Unable to generate AI recommendations at this time.")
    
    def run(self):
        """Run the main to-do list interface."""
        print("=== Smart To-Do List ===")
        
        while True:
            print("\nOptions:")
            print("1. Add new task")
            print("2. View pending tasks")
            print("3. View completed tasks")
            print("4. Toggle task status")
            print("5. Edit task")
            print("6. Delete task")
            print("7. Get AI recommendations")
            print("8. Exit")
            
            choice = input("\nSelect an option (1-8): ")
            
            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.view_tasks(show_completed=False)
            elif choice == '3':
                self.view_tasks(show_completed=True)
            elif choice == '4':
                self.toggle_task_status()
            elif choice == '5':
                self.edit_task()
            elif choice == '6':
                self.delete_task()
            elif choice == '7':
                self.get_ai_recommendations()
            elif choice == '8':
                print("\nExiting Smart To-Do List. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a number between 1 and 8.")

# Run the to-do list
if __name__ == "__main__":
    todo_list = SmartTodoList()
    todo_list.run()
```

### Extension Ideas

- Add recurring tasks (daily, weekly, monthly)
- Implement task dependencies (tasks that require other tasks to be completed first)
- Create a calendar view to visualize task distribution
- Add a Pomodoro timer feature for focused work sessions
- Implement task sharing or collaboration features
- Create a mobile-friendly web interface using a framework like Flask

---

---

## Subject Expert Tutor

**Difficulty**: Beginner-Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: Domain-specific prompting, educational dialogue

### Overview

Create a specialized tutor bot for a specific subject area that can explain concepts and quiz the user.

### Instructions

```python
from chatcraft import get_response
import time

def tutor_bot():
    """Interactive subject tutor that explains concepts and offers practice questions"""
    # Available subjects
    subjects = {
        "math": "You are a patient math tutor who explains concepts step-by-step. You use analogies to make abstract ideas concrete.",
        "science": "You are an enthusiastic science educator who relates scientific concepts to everyday experiences. You're excited about discovery and experimentation.",
        "history": "You are a storytelling history tutor who makes historical events come alive through narrative. You emphasize cause and effect in historical developments.",
        "literature": "You are a thoughtful literature guide who helps students analyze texts. You ask probing questions that deepen understanding of themes and characters.",
        "programming": "You are a coding mentor who explains programming concepts with clear examples. You break down problems into manageable steps."
    }
    
    print("=== Subject Expert Tutor ===")
    print("Available subjects:")
    for i, subject in enumerate(subjects.keys()):
        print(f"{i+1}. {subject.title()}")
    
    subject_choice = int(input("\nSelect a subject (1-5): ")) - 1
    subject = list(subjects.keys())[subject_choice]
    system_prompt = subjects[subject]
    
    print(f"\n=== {subject.title()} Tutor ===")
    print("1. Ask a specific question")
    print("2. Learn a new concept")
    print("3. Take a practice quiz")
    
    mode = input("\nWhat would you like to do? ")
    
    if mode == "1":
        # Ask specific question
        question = input("\nWhat's your question about " + subject + "? ")
        
        print("\nThinking...")
        answer = get_response(question, system=system_prompt)
        
        print("\n" + answer)
        
    elif mode == "2":
        # Learn new concept
        topic = input(f"\nWhat {subject} concept would you like to learn about? ")
        
        learn_prompt = f"""
        Explain the concept of {topic} in {subject} in a way that's easy to understand.
        Include:
        1. A simple definition
        2. Why it's important
        3. A real-world example or application
        4. Any key formulas or principles (if applicable)
        """
        
        print("\nResearching this topic...")
        explanation = get_response(learn_prompt, system=system_prompt)
        
        print("\n" + explanation)
        
        # Check understanding
        check_prompt = f"Create a quick check-for-understanding question about {topic} in {subject}."
        check_question = get_response(check_prompt, system=system_prompt)
        
        print("\n=== Check Your Understanding ===")
        print(check_question)
        
        user_answer = input("\nYour answer: ")
        
        feedback_prompt = f"""
        The user is learning about {topic} in {subject}.
        I asked them: {check_question}
        They answered: {user_answer}
        
        Provide constructive feedback on their answer. If they're on the right track,
        acknowledge that while adding any missing information. If they're incorrect, 
        gently correct them and re-explain the concept briefly.
        """
        
        feedback = get_response(feedback_prompt, system=system_prompt)
        print("\n" + feedback)
        
    elif mode == "3":
        # Practice quiz
        difficulty = input("\nChoose difficulty (easy/medium/hard): ").lower()
        num_questions = 3
        
        quiz_prompt = f"""
        Create a {difficulty} {subject} quiz with {num_questions} questions.
        For each question:
        1. Ask a {difficulty}-level question about {subject}
        2. Provide 4 possible answers labeled A, B, C, D
        3. Indicate the correct answer
        
        Format each question exactly like this:
        Q: (question text)
        A: (option A)
        B: (option B)
        C: (option C)
        D: (option D)
        Correct: (correct letter)
        """
        
        print(f"\nGenerating a {difficulty} {subject} quiz...")
        quiz = get_response(quiz_prompt, system=system_prompt)
        
        # Parse and present quiz
        questions = []
        sections = quiz.split("Q: ")
        
        for section in sections[1:]:
            question_parts = section.split("Correct: ")
            question_text = question_parts[0].strip()
            correct_answer = question_parts[1].strip()[0]  # Just take the first letter
            
            questions.append({
                "text": question_text,
                "correct": correct_answer
            })
        
        # Administer quiz
        score = 0
        for i, q in enumerate(questions):
            print(f"\nQuestion {i+1}:")
            print(q["text"])
            
            user_answer = input("\nYour answer (A/B/C/D): ").strip().upper()
            
            if user_answer == q["correct"]:
                print("✓ Correct!")
                score += 1
            else:
                print(f"✗ Incorrect. The correct answer was {q['correct']}.")
                
                # Get explanation
                explain_prompt = f"""
                The question was: {q['text']}
                The correct answer is {q['correct']}.
                Explain why this is the correct answer in a helpful way.
                """
                
                explanation = get_response(explain_prompt, system=system_prompt)
                print("\nExplanation:")
                print(explanation)
            
            # Small pause between questions
            if i < len(questions) - 1:
                time.sleep(1)
        
        # Final score and feedback
        print(f"\nQuiz complete! You scored {score}/{len(questions)}.")
        
        feedback_prompt = f"""
        The user just completed a {difficulty} {subject} quiz and scored {score}/{len(questions)}.
        Provide some encouraging feedback and suggest what they might want to study next.
        """
        
        feedback = get_response(feedback_prompt, system=system_prompt)
        print("\n" + feedback)
    
    else:
        print("Invalid choice.")

# Run the tutor bot
if __name__ == "__main__":
    tutor_bot()
```

### Extension Ideas

Add a spaced repetition system that tracks concepts users struggle with and revisits them.

---

---

## Text Adventure Game Engine

**Difficulty**: Advanced  
**Time**: 90-120 minutes  
**Learning Focus**: Object-oriented programming, game design, file I/O, AI interaction

### Overview

Create a text adventure game engine that allows students to build interactive stories with rooms, items, and characters. The engine supports saving/loading games and provides AI-powered hints to guide players.

### Instructions

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

### Extension Ideas

- Add more room types with special properties (e.g., dark rooms that require a light source)
- Implement NPCs (non-player characters) that the player can talk to
- Add simple puzzles that require specific items to solve
- Create a quest system with objectives and rewards
- Design a combat system for encounters with enemies
- Build a web-based interface using a framework like Flask

---

---

## Trivia or Quiz Bot

**Difficulty**: Beginner-Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: Loops, conditionals, lists

### Overview

Build an interactive quiz bot that asks questions, tracks the user's score, provides feedback, and offers hints when needed.

### Instructions

```python
from chatcraft import get_response
import random

def create_quiz_bot():
    # Define your quiz questions as (question, answer) tuples
    questions = [
        ("What's 2 + 2?", "4"),
        ("What is the capital of France?", "paris"),
        ("What's the keyword for loops in Python?", "for"),
        ("What year did the first iPhone release?", "2007"),
        ("Who wrote 'Romeo and Juliet'?", "shakespeare"),
    ]
    
    # Randomize questions
    random.shuffle(questions)
    
    # Initialize score
    score = 0
    total = len(questions)
    
    # Introduction
    print("Welcome to the Quiz Bot!")
    print(f"I'll ask you {total} questions. Let's see how you do!\n")
    
    # Loop through questions
    for i, (question, answer) in enumerate(questions):
        print(f"Question {i+1}/{total}: {question}")
        
        # Get user's answer
        user_answer = input("Your answer: ").strip().lower()
        
        # Check if correct
        if user_answer == answer.lower():
            score += 1
            print("Correct! ✅")
            
            # Get enthusiastic feedback from the bot
            feedback = get_response(
                f"The user correctly answered '{question}' with '{answer}'. Give a short, enthusiastic response.",
                system="You are an encouraging quiz host who keeps responses to one short sentence."
            )
            print(feedback)
        else:
            print(f"Sorry, that's incorrect. ❌ The answer is: {answer}")
            
            # Get encouraging feedback from the bot
            feedback = get_response(
                f"The user incorrectly answered '{question}' with '{user_answer}' instead of '{answer}'. Give a short, encouraging response.",
                system="You are a supportive quiz host who gives gentle encouragement in one sentence."
            )
            print(feedback)
        
        print("-" * 50)
    
    # Calculate percentage
    percentage = (score / total) * 100
    
    # Final results
    print(f"\nQuiz complete! Your score: {score}/{total} ({percentage:.1f}%)")
    
    # Get final feedback based on score
    if percentage >= 80:
        result = "excellent"
    elif percentage >= 60:
        result = "good"
    else:
        result = "needs improvement"
        
    final_feedback = get_response(
        f"The user scored {percentage:.1f}% ({score}/{total}) on the quiz, which is {result}. Give them feedback and encouragement.",
        system="You are a supportive teacher giving a short, personalized assessment."
    )
    
    print("\nBot's feedback:")
    print(final_feedback)

# Run the quiz
if __name__ == "__main__":
    create_quiz_bot()
```

### Extension Ideas

- Add difficulty levels where harder questions are worth more points
- Include a hint system where users can ask for clues but lose points
- Make a specialized quiz for a specific subject the students are studying
- Add a timer element where users have to answer within a time limit
- Let students create their own question banks to quiz each other

---

---

## Weather Dashboard

**Difficulty**: Intermediate-Advanced  
**Time**: 60-90 minutes  
**Learning Focus**: API integration, data visualization, environmental data analysis

### Overview

Create a weather dashboard that fetches real-time weather data and forecasts from an API, then visualizes it with charts and provides AI-powered weather advice based on conditions.

### Instructions

```python
import requests
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
from chatcraft import get_response

class WeatherDashboard:
    """
    A simple weather dashboard that retrieves and displays weather data.
    Students will need to sign up for a free API key from OpenWeatherMap.
    """
    
    def __init__(self):
        self.api_key = None
        self.base_url = "https://api.openweathermap.org/data/2.5/"
        self.output_dir = "weather_dashboard"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def setup(self):
        """Set up the dashboard with the API key."""
        print("=== Weather Dashboard Setup ===")
        
        # Check for existing API key
        key_file = os.path.join(self.output_dir, "api_key.txt")
        if os.path.exists(key_file):
            with open(key_file, 'r') as f:
                self.api_key = f.read().strip()
            print("API key loaded from file.")
        
        # If no API key, prompt for one
        if not self.api_key:
            print("\nYou need an OpenWeatherMap API key to use this dashboard.")
            print("Get a free API key at: https://openweathermap.org/api")
            self.api_key = input("Enter your API key: ").strip()
            
            # Save API key for future use
            save_key = input("Save this API key for future use? (y/n): ").lower() == 'y'
            if save_key:
                with open(key_file, 'w') as f:
                    f.write(self.api_key)
                print("API key saved.")
    
    def get_current_weather(self, location):
        """Get current weather for a location."""
        url = f"{self.base_url}weather"
        params = {
            'q': location,
            'appid': self.api_key,
            'units': 'metric'  # Use metric by default
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                print(f"Location '{location}' not found. Please check the spelling.")
            else:
                print(f"HTTP error: {http_err}")
            return None
        except Exception as err:
            print(f"Error: {err}")
            return None
    
    def get_forecast(self, location, days=5):
        """Get weather forecast for a location."""
        url = f"{self.base_url}forecast"
        params = {
            'q': location,
            'appid': self.api_key,
            'units': 'metric',
            'cnt': days * 8  # API returns data in 3-hour steps, 8 per day
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                print(f"Location '{location}' not found. Please check the spelling.")
            else:
                print(f"HTTP error: {http_err}")
            return None
        except Exception as err:
            print(f"Error: {err}")
            return None
    
    def display_current_weather(self, data):
        """Display current weather conditions."""
        if not data:
            return
        
        try:
            city = data['name']
            country = data['sys']['country']
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            weather_desc = data['weather'][0]['description']
            wind_speed = data['wind']['speed']
            clouds = data['clouds']['all']
            
            # Convert Unix timestamp to readable format
            sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
            sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
            
            print("\n=== Current Weather Conditions ===")
            print(f"Location: {city}, {country}")
            print(f"Weather: {weather_desc.title()}")
            print(f"Temperature: {temp}°C (Feels like: {feels_like}°C)")
            print(f"Humidity: {humidity}%")
            print(f"Pressure: {pressure} hPa")
            print(f"Wind Speed: {wind_speed} m/s")
            print(f"Cloud Cover: {clouds}%")
            print(f"Sunrise: {sunrise}")
            print(f"Sunset: {sunset}")
            
        except KeyError as e:
            print(f"Error parsing weather data: {e}")
    
    def plot_forecast(self, data, location):
        """Create forecast plots and save them."""
        if not data:
            return
        
        try:
            # Extract forecast data
            timestamps = []
            temps = []
            humidity = []
            descriptions = []
            
            for item in data['list']:
                dt = datetime.fromtimestamp(item['dt'])
                timestamps.append(dt)
                temps.append(item['main']['temp'])
                humidity.append(item['main']['humidity'])
                descriptions.append(item['weather'][0]['description'])
            
            # Create temperature forecast plot
            plt.figure(figsize=(12, 6))
            plt.plot(timestamps, temps, marker='o', color='#FF5733', linewidth=2)
            plt.xlabel('Date & Time')
            plt.ylabel('Temperature (°C)')
            plt.title(f'Temperature Forecast for {location}')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Save the plot
            temp_plot_file = os.path.join(self.output_dir, f"{location.replace(',', '_')}_temp_forecast.png")
            plt.savefig(temp_plot_file)
            plt.close()
            
            # Create humidity forecast plot
            plt.figure(figsize=(12, 6))
            plt.plot(timestamps, humidity, marker='s', color='#3498DB', linewidth=2)
            plt.xlabel('Date & Time')
            plt.ylabel('Humidity (%)')
            plt.title(f'Humidity Forecast for {location}')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Save the plot
            humidity_plot_file = os.path.join(self.output_dir, f"{location.replace(',', '_')}_humidity_forecast.png")
            plt.savefig(humidity_plot_file)
            plt.close()
            
            print(f"\nForecast plots saved to:\n- {temp_plot_file}\n- {humidity_plot_file}")
            
            return temp_plot_file, humidity_plot_file
            
        except KeyError as e:
            print(f"Error parsing forecast data: {e}")
            return None, None
    
    def get_weather_summary(self, current_data, forecast_data, location):
        """Generate a summary of the weather conditions and forecast."""
        if not current_data or not forecast_data:
            return "Unable to generate weather summary due to missing data."
        
        try:
            # Extract key information
            current_temp = current_data['main']['temp']
            current_desc = current_data['weather'][0]['description']
            
            # Get min/max for the next few days
            daily_temps = {}
            for item in forecast_data['list']:
                dt = datetime.fromtimestamp(item['dt'])
                date_str = dt.strftime('%Y-%m-%d')
                
                if date_str not in daily_temps:
                    daily_temps[date_str] = {'temps': [], 'descs': []}
                
                daily_temps[date_str]['temps'].append(item['main']['temp'])
                daily_temps[date_str]['descs'].append(item['weather'][0]['description'])
            
            # Create summary with key info
            summary = f"Weather Summary for {location}:\n\n"
            summary += f"Current Conditions: {current_desc.title()} at {current_temp}°C\n\n"
            summary += "Forecast:\n"
            
            for date_str, data in daily_temps.items():
                if data['temps']:  # Make sure we have data
                    min_temp = min(data['temps'])
                    max_temp = max(data['temps'])
                    
                    # Get most common description
                    from collections import Counter
                    desc_counter = Counter(data['descs'])
                    most_common_desc = desc_counter.most_common(1)[0][0]
                    
                    # Format date nicely (e.g., "Monday, Jan 15")
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    formatted_date = date_obj.strftime('%A, %b %d')
                    
                    summary += f"- {formatted_date}: {most_common_desc.title()}, {min_temp}°C to {max_temp}°C\n"
            
            return summary
            
        except KeyError as e:
            print(f"Error generating weather summary: {e}")
            return "Unable to generate weather summary."
    
    def get_ai_weather_advice(self, current_data, forecast_data, location):
        """Get AI-generated weather advice based on conditions."""
        if not current_data or not forecast_data:
            return "Unable to generate weather advice due to missing data."
        
        try:
            # Prepare weather information for the AI
            current_temp = current_data['main']['temp']
            current_desc = current_data['weather'][0]['description']
            current_humidity = current_data['main']['humidity']
            current_wind = current_data['wind']['speed']
            
            # Extract forecast information
            tomorrow_data = forecast_data['list'][:8]  # First 8 entries (24 hours)
            tomorrow_descs = [item['weather'][0]['description'] for item in tomorrow_data]
            tomorrow_temps = [item['main']['temp'] for item in tomorrow_data]
            
            avg_tomorrow_temp = sum(tomorrow_temps) / len(tomorrow_temps)
            min_tomorrow_temp = min(tomorrow_temps)
            max_tomorrow_temp = max(tomorrow_temps)
            
            # Create prompt for AI
            prompt = f"""
            Based on the following weather data for {location}:
            
            Current conditions:
            - Temperature: {current_temp}°C
            - Description: {current_desc}
            - Humidity: {current_humidity}%
            - Wind speed: {current_wind} m/s
            
            Tomorrow's forecast:
            - Average temperature: {avg_tomorrow_temp:.1f}°C
            - Range: {min_tomorrow_temp:.1f}°C to {max_tomorrow_temp:.1f}°C
            - Conditions: {', '.join(set(tomorrow_descs))}
            
            Please provide:
            1. Practical advice for what to wear or prepare for today
            2. Any weather warnings or precautions to be aware of
            3. Suggested activities that would be appropriate for this weather
            
            Keep your response conversational and under 150 words.
            """
            
            try:
                advice = get_response(prompt)
                return advice
            except Exception as e:
                print(f"Error getting AI weather advice: {e}")
                return "Unable to generate AI weather advice at this time."
                
        except KeyError as e:
            print(f"Error preparing data for AI advice: {e}")
            return "Unable to generate weather advice due to missing data."
    
    def run(self):
        """Run the main dashboard interface."""
        self.setup()
        
        if not self.api_key:
            print("No API key provided. Exiting.")
            return
        
        print("\n=== Weather Dashboard ===")
        location = input("Enter a city name (e.g., 'London' or 'London,UK'): ")
        
        print(f"\nFetching weather data for {location}...")
        current_data = self.get_current_weather(location)
        
        if current_data:
            self.display_current_weather(current_data)
            
            # Get forecast data
            print("\nFetching forecast data...")
            forecast_data = self.get_forecast(location)
            
            if forecast_data:
                # Plot forecast
                temp_plot, humidity_plot = self.plot_forecast(forecast_data, location)
                
                # Generate weather summary
                summary = self.get_weather_summary(current_data, forecast_data, location)
                print("\n=== Weather Summary ===")
                print(summary)
                
                # Get AI advice if requested
                get_advice = input("\nWould you like personalized weather advice? (y/n): ").lower() == 'y'
                if get_advice:
                    print("\nGenerating advice...")
                    advice = self.get_ai_weather_advice(current_data, forecast_data, location)
                    print("\n=== Weather Advice ===")
                    print(advice)
                
                # Save all info to a report file
                save_report = input("\nSave a weather report file? (y/n): ").lower() == 'y'
                if save_report:
                    try:
                        report_file = os.path.join(self.output_dir, f"{location.replace(',', '_')}_weather_report.txt")
                        with open(report_file, 'w') as f:
                            f.write(f"Weather Report for {location}\n")
                            f.write(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                            f.write("=== Current Conditions ===\n")
                            
                            # Extract current conditions
                            f.write(f"Temperature: {current_data['main']['temp']}°C\n")
                            f.write(f"Feels like: {current_data['main']['feels_like']}°C\n")
                            f.write(f"Weather: {current_data['weather'][0]['description'].title()}\n")
                            f.write(f"Humidity: {current_data['main']['humidity']}%\n")
                            f.write(f"Wind speed: {current_data['wind']['speed']} m/s\n")
                            f.write(f"Pressure: {current_data['main']['pressure']} hPa\n\n")
                            
                            # Add summary
                            f.write("=== Forecast Summary ===\n")
                            f.write(summary + "\n\n")
                            
                            # Add advice if it was generated
                            if get_advice:
                                f.write("=== Weather Advice ===\n")
                                f.write(advice + "\n")
                            
                            # Add note about plot files
                            if temp_plot and humidity_plot:
                                f.write("\nForecast plots saved as:\n")
                                f.write(f"- {os.path.basename(temp_plot)}\n")
                                f.write(f"- {os.path.basename(humidity_plot)}\n")
                        
                        print(f"\nWeather report saved to: {report_file}")
                    except Exception as e:
                        print(f"Error saving weather report: {e}")
            
        print("\nThank you for using the Weather Dashboard!")

# Run the dashboard
if __name__ == "__main__":
    dashboard = WeatherDashboard()
    dashboard.run()
```

### Extension Ideas

- Add support for multiple locations and comparison views
- Implement unit conversion between metric and imperial
- Create a historical weather data retrieval and analysis feature
- Add precipitation and wind forecasts with appropriate visualizations
- Implement a daily weather notification system
- Create a map-based visualization of weather data

---

---

# YouTube to Blog Converter

**Difficulty**: Beginner-Intermediate  
**Time**: 30-45 minutes  
**Learning Focus**: API integration, text processing, content repurposing

### Overview

Create a tool that converts YouTube video transcripts into well-formatted blog posts using AI. This project helps students understand how to extract data from one format and transform it into another valuable piece of content.

### Instructions

```python
import re
import argparse
from youtube_transcript_api import YouTubeTranscriptApi
from chatcraft import get_response

def youtube_to_blog():
    """Convert YouTube video transcripts into blog post content using AI."""
    print("=== YouTube to Blog Converter ===")
    print("This tool extracts a transcript from a YouTube video and converts it to a blog post.")
    
    # Get video URL or ID
    video_input = input("Enter YouTube video URL or video ID: ")
    
    # Extract video ID from URL if needed
    video_id = extract_video_id(video_input)
    
    if not video_id:
        print("Error: Could not extract a valid YouTube video ID.")
        return
    
    print(f"Processing video ID: {video_id}")
    
    # Get transcript
    try:
        transcript = get_transcript(video_id)
        if not transcript:
            return
    except Exception as e:
        print(f"Error getting transcript: {e}")
        return
    
    # Get video metadata if needed
    video_title = input("Enter video title (or press Enter to skip): ")
    video_author = input("Enter video creator/channel name (or press Enter to skip): ")
    
    # Get blog style preferences
    print("\nBlog Style Options:")
    print("1. Informational/Educational")
    print("2. Conversational/Casual")
    print("3. Professional/Formal")
    print("4. Tutorial/How-To")
    
    style_choice = input("Select a style (1-4): ")
    
    if style_choice == "1":
        blog_style = "informational"
    elif style_choice == "2":
        blog_style = "conversational"
    elif style_choice == "3":
        blog_style = "professional"
    elif style_choice == "4":
        blog_style = "tutorial"
    else:
        print("Invalid choice. Using informational style.")
        blog_style = "informational"
    
    # Get additional context
    topic_keywords = input("Enter 3-5 keywords related to the video (comma separated): ")
    
    # Get intended audience
    audience = input("Who is the target audience for this blog post? ")
    
    # Generate blog post with AI
    generate_blog_post(transcript, video_title, video_author, blog_style, topic_keywords, audience)

def extract_video_id(video_input):
    """Extract the YouTube video ID from a URL or return the ID if already provided."""
    # Check if it's already a video ID (simple 11-character string)
    if re.match(r'^[a-zA-Z0-9_-]{11}, video_input):
        return video_input
        
    # Try to extract from URL
    youtube_regex = r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(youtube_regex, video_input)
    
    if match:
        return match.group(1)
    
    return None

def get_transcript(video_id):
    """Get the transcript from a YouTube video."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine all transcript segments
        full_transcript = " ".join([item['text'] for item in transcript_list])
        
        # Print a preview
        preview_length = min(150, len(full_transcript))
        print(f"\nTranscript preview ({len(full_transcript)} characters):")
        print(f"{full_transcript[:preview_length]}...")
        
        return full_transcript
    
    except Exception as e:
        print(f"Error: Could not retrieve transcript. {str(e)}")
        print("Possible reasons:")
        print("- The video might not have closed captions/subtitles")
        print("- The video ID might be incorrect")
        print("- The video owner may have disabled transcript access")
        return None

def generate_blog_post(transcript, title, author, style, keywords, audience):
    """Generate a blog post from the transcript using AI."""
    print("\nGenerating blog post...")
    
    # Create a prompt for the AI
    prompt = f"""
    Convert this YouTube video transcript into a well-structured blog post:
    
    VIDEO INFORMATION:
    Title: {title if title else "Not provided"}
    Creator: {author if author else "Not provided"}
    Style: {style}
    Keywords: {keywords}
    Target Audience: {audience}
    
    TRANSCRIPT:
    {transcript[:4000]}  # Limit transcript length if needed
    
    Please create a complete blog post with:
    1. An engaging headline/title
    2. Introduction that hooks the reader
    3. Well-structured sections with subheadings
    4. Conclusion or call-to-action
    5. Add relevant statistics or examples where appropriate
    
    Format the post using markdown syntax for headings, lists, etc.
    The tone should be {style} and appropriate for the specified audience.
    Expand on any concepts from the video that need more explanation.
    Add 3-5 relevant tags at the end of the post.
    
    Length: Aim for ~1000-1500 words.
    """
    
    try:
        # Generate blog post using the prompt
        blog_post = get_response(prompt)
        
        # Save the blog post to a file
        filename = f"blog_post_{title.replace(' ', '_')[:30] if title else 'from_youtube'}.md"
        with open(filename, 'w') as f:
            f.write(blog_post)
        
        print(f"\nBlog post successfully generated and saved to: {filename}")
        
        # Print a preview of the blog post
        preview_lines = blog_post.split('\n')[:10]
        print("\nBlog Post Preview:")
        print("\n".join(preview_lines) + "\n...")
        
    except Exception as e:
        print(f"Error generating blog post: {e}")

if __name__ == "__main__":
    youtube_to_blog()
```

### Extension Ideas

- Add support for multiple languages and translation
- Implement a social media post generator from the same content
- Create a scheduler to process videos in batch
- Add image extraction from video thumbnails or frames
- Build a web interface with Flask or Streamlit
- Implement SEO optimization suggestions for the generated content

---

---

<!-- All mini-projects are now included and conform to the standard format.
For additions or edits, update the corresponding files in docs/projects/ and regenerate this document. -->

_For implementation strategies and assessment ideas, see the [ChatCraft Education Guide](education-guide.md)._
