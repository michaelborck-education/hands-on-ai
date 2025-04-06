"""
Basic test script for the hands_on_ai package.
"""

import os
import sys

# Add the package to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    # Test main package
    import hands_on_ai
    print(f"✅ Successfully imported hands_on_ai {hands_on_ai.__name__}")
    
    # Test chat module
    from hands_on_ai import chat
    print(f"✅ Successfully imported hands_on_ai.chat {chat.__name__}")
    
    # Test RAG module
    from hands_on_ai import rag
    print(f"✅ Successfully imported hands_on_ai.rag {rag.__name__}")
    
    # Test agent module
    from hands_on_ai import agent
    print(f"✅ Successfully imported hands_on_ai.agent {agent.__name__}")
    
    print("All imports successful!")


def test_chat():
    """Test chat module functionality."""
    print("\nTesting chat module...")
    
    # Import bot functions
    from hands_on_ai.chat import friendly_bot
    print(f"✅ Successfully imported friendly_bot {friendly_bot.__name__}")
    
    # Test importing from categories
    from hands_on_ai.chat.personalities.creative import pirate_bot
    print(f"✅ Successfully imported pirate_bot {pirate_bot.__name__}")
    
    # Test importing directly from bot file
    from hands_on_ai.chat.personalities.bots.teacher_bot import teacher_bot
    print(f"✅ Successfully imported teacher_bot {teacher_bot.__name__}")
    
    print("Chat module tests passed!")


def test_config():
    """Test configuration functionality."""
    print("\nTesting configuration...")
    
    from hands_on_ai.config import (
        get_server_url,
        get_model,
        get_embedding_model,
        get_chunk_size,
    )
    
    print(f"Server URL: {get_server_url()}")
    print(f"Default model: {get_model()}")
    print(f"Embedding model: {get_embedding_model()}")
    print(f"Chunk size: {get_chunk_size()}")
    
    print("Configuration tests passed!")


if __name__ == "__main__":
    print("Running basic tests for hands-on-ai package...\n")
    test_imports()
    test_chat()
    test_config()
    print("\nAll tests passed! The package is working correctly.")