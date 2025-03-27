# Mini Project Examples

This document contains ready-to-use mini-projects and activities for using ChatCraft in educational settings. Each project includes learning objectives, difficulty level, estimated time, and complete code examples.

## Table of Contents

1. [Personality Bot Creator](#1-personality-bot-creator)
2. [Knowledge Quiz Bot](#2-knowledge-quiz-bot)
3. [Bot Debate Simulator](#3-bot-debate-simulator)
4. [Mood Journal Assistant](#4-mood-journal-assistant)
5. [Choose Your Own Adventure](#5-choose-your-own-adventure)
6. [Subject Expert Tutor](#6-subject-expert-tutor)
7. [Code Explainer Tool](#7-code-explainer-tool)
8. [Historical Figure Chat](#8-historical-figure-chat)
9. [Language Translation Helper](#9-language-translation-helper)
10. [Creative Writing Partner](#10-creative-writing-partner)

---

## 1. Personality Bot Creator

**Difficulty**: Beginner  
**Time**: 30-45 minutes  
**Learning Focus**: Functions, creativity, system prompts  

**Description**: Students create and interact with a bot that has a unique personality of their design. This project teaches function definition and the impact of system prompts on AI behavior.

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

**Extension**: Create a menu system that lets the user choose which personality to talk to.

---

## 2. Knowledge Quiz Bot

**Difficulty**: Beginner-Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: Lists, loops, conditionals, scoring systems  

**Description**: Build a bot that quizzes the user on a topic and tracks their score.

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

**Extension**: Add difficulty levels, timing, or topic categories.

---

## 3. Bot Debate Simulator

**Difficulty**: Intermediate  
**Time**: 60-90 minutes  
**Learning Focus**: Function calls, text parsing, dialogue simulation  

**Description**: Simulate a debate or conversation between two or more bots with different personalities or viewpoints.

```python
from chatcraft import get_response
import time

def debate_bot(prompt, perspective, name, personality="debate"):
    """Create a bot with a specific debate perspective"""
    system_prompt = f"""
    You are {name}, a debater with the following perspective: {perspective}
    You speak in a clear, persuasive manner presenting your viewpoint.
    Keep responses under 100 words to keep the debate flowing.
    """
    return get_response(prompt, system=system_prompt, personality=personality)

def run_debate():
    """Run a simulated debate between bots"""
    print("=== Bot Debate Simulator ===")
    
    topic = input("What topic should the bots debate? ")
    rounds = int(input("How many response rounds? (1-5): "))
    
    # Create debaters
    debaters = [
        {
            "name": "Dr. Logic", 
            "perspective": "You value logical reasoning and empirical evidence above all. You cite studies and statistics to support your points."
        },
        {
            "name": "Empathetic Emma", 
            "perspective": "You believe emotional impact and human stories are most important. You consider how policies and ideas affect real people."
        },
        {
            "name": "Traditional Tom", 
            "perspective": "You value tradition, stability, and time-tested approaches. You're skeptical of rapid change and new untested ideas."
        }
    ]
    
    # Allow user to select two debaters
    print("\nChoose two debaters:")
    for i, debater in enumerate(debaters):
        print(f"{i+1}. {debater['name']}: {debater['perspective'][:50]}...")
    
    choice1 = int(input("\nSelect first debater (1-3): ")) - 1
    choice2 = int(input("Select second debater (1-3): ")) - 1
    
    debater1 = debaters[choice1]
    debater2 = debaters[choice2]
    
    # Start the debate
    print(f"\n=== {debater1['name']} vs. {debater2['name']} on {topic} ===\n")
    
    # Initial statements
    print(f"{debater1['name']}'s opening statement:")
    statement1 = debate_bot(f"Give an opening statement on the topic of {topic}", 
                           debater1['perspective'], debater1['name'])
    print(statement1)
    print()
    
    time.sleep(1)
    
    print(f"{debater2['name']}'s opening statement:")
    statement2 = debate_bot(f"Give an opening statement on the topic of {topic}", 
                           debater2['perspective'], debater2['name'])
    print(statement2)
    print()
    
    # Back and forth rounds
    current_statement = statement2
    for round_num in range(rounds):
        print(f"--- Round {round_num + 1} ---")
        
        # First debater responds
        time.sleep(1)
        print(f"{debater1['name']} responds:")
        response = debate_bot(
            f"Respond to this statement on {topic}: '{current_statement}'", 
            debater1['perspective'], debater1['name']
        )
        print(response)
        print()
        current_statement = response
        
        # Second debater responds
        time.sleep(1)
        print(f"{debater2['name']} responds:")
        response = debate_bot(
            f"Respond to this statement on {topic}: '{current_statement}'", 
            debater2['perspective'], debater2['name']
        )
        print(response)
        print()
        current_statement = response
    
    # Closing statements
    print("=== Closing Statements ===")
    
    time.sleep(1)
    print(f"{debater1['name']}'s closing remarks:")
    closing1 = debate_bot(f"Give a brief closing statement summarizing your position on {topic}", 
                         debater1['perspective'], debater1['name'])
    print(closing1)
    print()
    
    time.sleep(1)
    print(f"{debater2['name']}'s closing remarks:")
    closing2 = debate_bot(f"Give a brief closing statement summarizing your position on {topic}", 
                         debater2['perspective'], debater2['name'])
    print(closing2)
    
    # Moderator summary
    print("\n=== Moderator Summary ===")
    
    summary_prompt = f"""
    Summarize the debate between {debater1['name']} and {debater2['name']} on {topic}.
    {debater1['name']}'s perspective: {debater1['perspective']}
    {debater1['name']}'s closing: {closing1}
    
    {debater2['name']}'s perspective: {debater2['perspective']}
    {debater2['name']}'s closing: {closing2}
    
    Provide a neutral, balanced summary of both positions.
    """
    
    moderator = get_response(summary_prompt, system="You are a neutral debate moderator.")
    print(moderator)

# Run the debate simulator
if __name__ == "__main__":
    run_debate()
```

**Extension**: Allow students to create their own debater profiles with unique perspectives.

---

## 4. Mood Journal Assistant

**Difficulty**: Beginner-Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: File I/O, date handling, text analysis  

**Description**: Create a journaling assistant that helps users track moods and reflect on patterns.

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

**Extension**: Add mood tracking visualizations or goal-setting features.

---

## 5. Choose Your Own Adventure

**Difficulty**: Intermediate  
**Time**: 60-90 minutes  
**Learning Focus**: State management, narrative design, user input handling  

**Description**: Create an interactive story where the bot generates narrative segments based on user choices.

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

**Extension**: Add inventory management, character stats, or multiple endings based on decisions.

---

## 6. Subject Expert Tutor

**Difficulty**: Beginner-Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: Domain-specific prompting, educational dialogue  

**Description**: Create a specialized tutor bot for a specific subject area that can explain concepts and quiz the user.

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

**Extension**: Add a spaced repetition system that tracks concepts users struggle with and revisits them.

---

## 7. Code Explainer Tool

**Difficulty**: Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: Code analysis, documentation  

**Description**: Create a tool that explains code snippets and helps users understand programming concepts.

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

**Extension**: Add functionality to generate test cases or convert code between languages.

---

## 8. Historical Figure Chat

**Difficulty**: Beginner-Intermediate  
**Time**: 30-45 minutes  
**Learning Focus**: Historical research, character perspective, dialogue  

**Description**: Chat with simulated historical figures to learn about their lives, achievements, and time periods.

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

**Extension**: Add a "time travel interview" mode where students can interview multiple figures about the same topic or event.

---

## 9. Language Translation Helper

**Difficulty**: Beginner  
**Time**: 30-45 minutes  
**Learning Focus**: Multilingual communication, cultural context  

**Description**: Create a tool that helps translate text between languages and explains cultural context.

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

**Extension**: Add a conversation practice mode where students can simulate dialogues in another language.

---

## 10. Creative Writing Partner

**Difficulty**: Beginner-Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: Narrative development, creative collaboration, editing  

**Description**: A collaborative writing tool that helps students develop stories, poems, or essays.

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

**Extension**: Add a collaborative storytelling mode where student and bot take turns adding to a story.

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
        