# Code Explainer Tool

**Difficulty**: Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: Code analysis, documentation

## Overview

Create a tool that explains code snippets and helps users understand programming concepts.

## Instructions

```python
from ailabkit.chat import get_response
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

## Extension Ideas

Add functionality to generate test cases or convert code between languages.

---