"""
Pydantic schemas for structured agent outputs.

These schemas replace the fragile JSON parsing with robust validation
while maintaining the same logical structure for educational purposes.
"""

from typing import Union
from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    """
    Represents an agent's decision to call a tool.
    
    This maintains the same structure as the original JSON format
    but with Pydantic validation for reliability.
    """
    thought: str = Field(
        description="The agent's reasoning about why this tool is needed"
    )
    tool: str = Field(
        description="Name of the tool to call (must match registered tools)"
    )
    input: str = Field(
        description="Input parameter to pass to the tool"
    )


class FinalAnswer(BaseModel):
    """
    Represents the agent's final response to the user.
    
    This indicates the agent has gathered enough information
    and is ready to provide a complete answer.
    """
    thought: str = Field(
        description="The agent's final reasoning about the answer"
    )
    answer: str = Field(
        description="The final answer to the user's question"
    )


# Union type representing all possible agent responses
# The discriminator helps Pydantic choose the correct model
AgentResponse = Union[ToolCall, FinalAnswer]


# For backward compatibility and debugging, we can also define
# more specific validation if needed in the future
class ValidatedToolCall(ToolCall):
    """
    Enhanced tool call with additional validation.
    Can be used for stricter validation in development.
    """
    
    class Config:
        # Add any additional validation rules here
        str_strip_whitespace = True  # Automatically strip whitespace
        validate_assignment = True   # Validate on assignment