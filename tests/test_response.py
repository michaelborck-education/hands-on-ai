import chatcraft

def test_friendly_bot():
    response = chatcraft.friendly_bot("What is 2 + 2?")
    assert isinstance(response, str)
    assert response.strip()

def test_empty_prompt():
    result = chatcraft.friendly_bot(" ")
    assert "⚠️ Empty" in result

def test_emoji_bot_response():
    response = chatcraft.emoji_bot("How are you?")
    assert any(c in response for c in ["😀", "🤖", "💬", "🔁", "❓", "💥"]) or len(response.strip()) > 0
