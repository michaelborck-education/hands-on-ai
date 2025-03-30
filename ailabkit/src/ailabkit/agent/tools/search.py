"""
Search tool for retrieving information (simulated).
"""

from ..core import register_tool


def search(query: str):
    """
    Perform a web search (SIMULATED).
    
    Args:
        query: Search query
        
    Returns:
        str: Search results
    """
    # This is a simulated search tool for educational purposes
    searches = {
        "python programming": """
Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation. Python is dynamically-typed and garbage-collected. It supports multiple programming paradigms, including structured, object-oriented, and functional programming. It is often described as a "batteries included" language due to its comprehensive standard library.

Key features:
- Easy to learn and use
- Interpreted language
- Extensive standard library
- Dynamic typing
- Object-oriented
""",

        "artificial intelligence": """
Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any system that perceives its environment and takes actions that maximize its chance of achieving its goals.

Major AI applications include:
- Machine learning
- Natural language processing
- Computer vision
- Robotics
- Expert systems
""",

        "climate change": """
Climate change refers to long-term shifts in temperatures and weather patterns. These shifts may be natural, but since the 1800s, human activities have been the main driver of climate change, primarily due to burning fossil fuels like coal, oil and gas, which produces heat-trapping gases.

Key effects include:
- Rising global temperatures
- Sea level rise
- Increased frequency of extreme weather events
- Changes in wildlife populations and habitats
- Ocean acidification
"""
    }
    
    # Try to match the query to our predefined searches
    for key, result in searches.items():
        if key in query.lower():
            return f"Search results for '{query}':\n{result}"
    
    # Default response for queries we don't have predefined results for
    return f"""
Search results for '{query}' (SIMULATED):

This is a simulated search response for educational purposes. In a real implementation, this would connect to a search API to provide actual results.

For this demo, we have predefined results for: "Python programming", "artificial intelligence", and "climate change".
"""


def register_search_tool():
    """Register the search tool with the agent."""
    register_tool(
        name="search",
        description="Search the web for information (simulated). Example input: {'query': 'Python programming'}",
        function=search
    )