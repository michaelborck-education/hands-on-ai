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