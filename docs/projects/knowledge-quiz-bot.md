# Knowledge Quiz Bot

**Difficulty**: Beginner-Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: Lists, loops, conditionals, scoring systems

## Overview

Build a bot that quizzes the user on a topic and tracks their score.

## Instructions

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

## Extension Ideas

Add difficulty levels, timing, or topic categories.

---