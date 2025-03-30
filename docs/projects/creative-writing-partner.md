# Creative Writing Partner

**Difficulty**: Beginner-Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: Narrative development, creative collaboration, editing

## Overview

A collaborative writing tool that helps students develop stories, poems, or essays.

## Instructions

```python
from ailabkit.chat import get_response

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

## Extension Ideas

Add a collaborative storytelling mode where student and bot take turns adding to a story.

---

# Implementation Tips

When using these mini-projects in a classroom setting:

1. **Scaffold appropriately**: Start with simpler projects for beginners, then progress to more complex ones.
2. **Modify complexity**: Adjust project requirements based on student skill level and available time.
3. **Pair programming**: Have students work in pairs to encourage collaboration.
4. **Challenge extensions**: Provide additional challenges for students who finish early.
5. **Focus on concepts**: Emphasize the programming concepts being used rather than just creating a functioning bot.
6. **Ethical discussions**: Use these projects as opportunities to discuss AI ethics, bias, and limitations.

# Assessment Ideas

- Have students document their process in a digital portfolio
- Create a "bot showcase" where students present their creations
- Ask students to write reflections on what they learned
- Evaluate code structure, comments, and organization
- Have students peer-review each other's projects

---

*These examples are designed to be flexible starting points. Adjust and expand them to suit your specific educational needs and student skill levels.*