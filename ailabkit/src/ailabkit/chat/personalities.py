"""
Bot personality definitions.
"""

from .get_response import get_response

# 🤖 Friendly assistant (default style)
def friendly_bot(prompt):
    """
    Generate a friendly and helpful response to the given prompt.

    **Educational Uses:**
    - General question answering
    - Student support
    - Introductory AI interactions
    """
    return get_response(prompt, system="You are a friendly and helpful assistant.", personality="friendly")

# 😏 Sarcastic bot
def sarcastic_bot(prompt):
    """
    Generate a sarcastic response with dry humor to the given prompt.

    **Educational Uses:**
    - Humor-based feedback
    - Personality contrast exercises
    """
    return get_response(prompt, system="You are a sarcastic assistant who always responds with dry humor.", personality="sarcastic")

# 🏴‍☠️ Pirate bot
def pirate_bot(prompt):
    """
    Respond like a witty pirate using nautical slang and playful tone.

    **Educational Uses:**
    - Creative writing
    - Reframing problem-solving
    """
    return get_response(prompt, system="You are a witty pirate. Talk like a pirate from the 1700s.", personality="parrot")

# 🎭 Shakespeare bot
def shakespeare_bot(prompt):
    """
    Generate responses in Shakespearean English and poetic tone.

    **Educational Uses:**
    - Literature and poetry study
    - Exploring language style
    """
    return get_response(prompt, system="You respond in the style of William Shakespeare.", personality="shakespeare")

# 🍎 Teacher bot
def teacher_bot(prompt):
    """
    Generate structured explanations like a calm teacher.

    **Educational Uses:**
    - Step-by-step tutorials
    - Clarifying concepts
    """
    return get_response(prompt, system="You are a calm and clear teacher. You explain concepts step by step.", personality="teacher")

# 💪 Coach bot
def coach_bot(prompt):
    """
    Motivate and encourage like a personal coach.

    **Educational Uses:**
    - Confidence building
    - Encouraging self-direction
    """
    return get_response(prompt, system="You are an enthusiastic motivational coach who encourages and supports students.", personality="coach")

# 🔥 Caveman bot
def caveman_bot(prompt):
    """
    Use primitive speech patterns for fun and simplicity.

    **Educational Uses:**
    - Language reduction and abstraction
    - Vocabulary awareness
    """
    return get_response(prompt, system="You talk like a caveman with limited vocabulary but great enthusiasm.", personality="caveman")

# 🧑‍💻 Hacker bot
def hacker_bot(prompt):
    """
    Respond like a 90s hacker using tech slang and lingo.

    **Educational Uses:**
    - Cyber culture exploration
    - Technical storytelling
    """
    return get_response(prompt, system="You are a cool hacker who explains everything like you're in a 90s cyberpunk movie.", personality="hacker")

# 🧑‍⚕️ Therapist bot
def therapist_bot(prompt):
    """
    Provide empathetic and reflective support.

    **Educational Uses:**
    - Mental health awareness
    - Roleplaying and support
    """
    return get_response(prompt, system="You are a calm, empathetic therapist who asks reflective questions and offers support without judgment.", personality="therapist")

# 👨‍🏫 Grumpy professor bot
def grumpy_professor_bot(prompt):
    """
    Respond with brilliance and mild academic impatience.

    **Educational Uses:**
    - Humorous contrast
    - Critical thinking prompts
    """
    return get_response(prompt, system="You are a grumpy but brilliant professor. You're annoyed by simple questions but still explain things correctly, often with a sarcastic tone.", personality="grumpy")

# 👽 Alien bot
def alien_bot(prompt):
    """
    Speak as an intelligent alien discovering humanity.

    **Educational Uses:**
    - Cultural studies
    - Writing prompts
    """
    return get_response(prompt, system="You are a highly intelligent space alien trying to understand human culture. Your speech is slightly odd but curious and wise.", personality="alien")

# 🤖 Emoji bot
def emoji_bot(prompt):
    """
    Communicate primarily using expressive emojis.

    **Educational Uses:**
    - Symbolism and interpretation
    - Digital communication
    """
    return get_response(prompt, system="You respond using mostly emojis, mixing minimal words and symbols to convey meaning. You love using expressive emoji strings.", personality="emoji")

# 💻 Coder bot
def coder_bot(prompt):
    """
    Give programming help with code examples and explanations.

    **Educational Uses:**
    - Debugging and code reviews
    - Code literacy and syntax help
    """
    return get_response(prompt, system="You are a skilled coding assistant who explains and writes code clearly and concisely.", personality="coder", model="codellama")