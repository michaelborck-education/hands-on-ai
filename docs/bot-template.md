# Here is the template of a new personality chat bot

```python
def your_bot_name(prompt):
    """
    🤖 Your Bot Title

    One-line summary of your bot's personality.

    ```python
    from hands_on_ai.chat import your_bot_name
    response = your_bot_name("Ask me anything")
    print(response)
    ```

    **Example Output:**
    ```
    Your awesome response goes here.
    ```

    **Educational Uses:**
    - Example usage 1
    - Example usage 2

    Args:
        prompt (str): The user's input text or question.

    Returns:
        str: The bot's response in its unique personality style.
    """
    return get_response(prompt, system="Describe your bot's behavior here.", personality="yourpersonality")
```