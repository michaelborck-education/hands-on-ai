# Trivia or Quiz Bot

**Difficulty**: Beginner-Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: Loops, conditionals, lists  
**Module**: chat

## Overview

Build an interactive quiz bot that asks questions, tracks the user's score, provides feedback, and offers hints when needed.

## Instructions

```python
from hands_on_ai.chat import get_response
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

## Extension Ideas

- Add difficulty levels where harder questions are worth more points
- Include a hint system where users can ask for clues but lose points
- Make a specialised quiz for a specific subject the students are studying
- Add a timer element where users have to answer within a time limit
- Let students create their own question banks to quiz each other

---