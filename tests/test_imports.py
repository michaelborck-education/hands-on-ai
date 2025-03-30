"""
Basic test script for the ailabkit package.
"""

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    # Test main package
    import ailabkit
    print("✅ Successfully imported ailabkit")
    
    # Test chat module
    from ailabkit import chat
    print("✅ Successfully imported ailabkit.chat")
    
    # Test RAG module
    from ailabkit import rag
    print("✅ Successfully imported ailabkit.rag")
    
    # Test agent module
    from ailabkit import agent
    print("✅ Successfully imported ailabkit.agent")
    
    print("All imports successful!")


def test_chat():
    """Test chat module functionality."""
    print("\nTesting chat module...")
    
    # Import bot functions
    from ailabkit.chat import friendly_bot
    print("✅ Successfully imported friendly_bot")
    
    # Test importing from categories
    from ailabkit.chat.personalities.creative import pirate_bot
    print("✅ Successfully imported pirate_bot from creative module")
    
    # Test importing directly from bot file
    from ailabkit.chat.personalities.bots.teacher_bot import teacher_bot
    print("✅ Successfully imported teacher_bot directly from bot file")
    
    print("Chat module tests passed!")


def test_config():
    """Test configuration functionality."""
    print("\nTesting configuration...")
    
    from ailabkit.config import (
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
    print("Running basic tests for ailabkit package...\n")
    test_imports()
    test_chat()
    test_config()
    print("\nAll tests passed! The package is working correctly.")