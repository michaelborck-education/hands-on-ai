# Language Translation Helper

**Difficulty**: Beginner  
**Time**: 30-45 minutes  
**Learning Focus**: Multilingual communication, cultural context

## Overview

Create a tool that helps translate text between languages and explains cultural context.

## Instructions

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

## Extension Ideas

Add a conversation practice mode where students can simulate dialogues in another language.

---