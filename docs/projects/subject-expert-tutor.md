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