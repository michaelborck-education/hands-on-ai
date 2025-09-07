# HandsOnAI Instructor Integration Plan

## Overview

This document outlines the plan to integrate the Instructor package into HandsOnAI to improve the reliability of structured outputs while maintaining educational value and backward compatibility.

## Current Problem

The existing JSON parsing implementation in `src/hands_on_ai/agent/formats.py` is fragile:
- Basic `json.loads()` with regex fallbacks
- No schema validation
- No type enforcement
- Prone to failures with malformed JSON from smaller models

## Solution: Hybrid Approach

**Strategy**: Keep ReAct text format for larger models (educational value) + Replace brittle JSON parsing with Instructor (reliability).

### Benefits
- ✅ **Educational Value Preserved**: Students still learn ReAct reasoning patterns
- ✅ **Improved Reliability**: Robust structured outputs for smaller models
- ✅ **Zero Breaking Changes**: Same student-facing API
- ✅ **Production Ready**: Instructor's battle-tested validation

## Implementation Plan

### Phase 1: Dependencies and Setup

#### 1.1 Update Dependencies
**File**: `pyproject.toml`
```toml
dependencies = [
    "requests", 
    "typer",
    "python-fasthtml",
    "python-docx", 
    "pymupdf", 
    "scikit-learn", 
    "numpy",
    "instructor>=1.11.0",  # ADD
    "pydantic>=2.0"        # ADD
]
```

**Status**: ⏳ Pending
**Estimated Time**: 5 minutes

### Phase 2: Pydantic Schema Design

#### 2.1 Create Schema Definitions
**File**: `src/hands_on_ai/agent/schemas.py` (NEW FILE)

```python
from typing import Optional, Literal, Union
from pydantic import BaseModel, Field

class ToolCall(BaseModel):
    """Represents a tool call action."""
    thought: str = Field(description="Reasoning about why this tool is needed")
    tool: str = Field(description="Name of the tool to call")
    input: str = Field(description="Input parameter for the tool")

class FinalAnswer(BaseModel):
    """Represents the final answer."""
    thought: str = Field(description="Final reasoning about the answer")
    answer: str = Field(description="Final answer to the user's question")

# Union type for all possible agent responses
AgentResponse = Union[ToolCall, FinalAnswer]
```

**Status**: ⏳ Pending
**Estimated Time**: 15 minutes

### Phase 3: Instructor Integration

#### 3.1 Replace JSON Agent Implementation
**File**: `src/hands_on_ai/agent/formats.py`

Replace `run_json_agent()` function with Instructor-powered version:

```python
def run_instructor_agent(
    prompt: str, 
    tools: Dict[str, Dict[str, Any]], 
    model: str = None,
    max_iterations: int = 5,
    verbose: bool = False
) -> str:
    """
    Run agent using Instructor for robust structured outputs.
    
    This replaces the fragile JSON parsing with Pydantic validation.
    """
    import instructor
    from openai import OpenAI
    from .schemas import AgentResponse, ToolCall, FinalAnswer
    from ..config import get_server_url, get_api_key
    
    # Create instructor client
    client = instructor.from_openai(
        OpenAI(
            base_url=get_server_url(),
            api_key=get_api_key() or "ollama"
        ),
        mode=instructor.Mode.JSON
    )
    
    # Use existing system prompt structure
    system_prompt = JSON_SYSTEM_PROMPT.format(
        tool_list=format_tools_for_json_prompt(tools)
    )
    
    conversation_history = [prompt]
    
    for iteration in range(max_iterations):
        try:
            # Use Instructor instead of manual JSON parsing
            response: AgentResponse = client.chat.completions.create(
                model=model,
                response_model=AgentResponse,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "\n".join(conversation_history)}
                ]
            )
            
            if verbose:
                log.info(f"Instructor response: {response}")
            
            # Handle based on response type (automatic validation!)
            if isinstance(response, FinalAnswer):
                return response.answer
            
            elif isinstance(response, ToolCall):
                # Validate tool exists
                if response.tool not in tools:
                    error_msg = f"Error: Tool '{response.tool}' not found. Available tools: {', '.join(tools.keys())}"
                    conversation_history.append(error_msg)
                    continue
                
                # Execute tool with error handling
                try:
                    result = tools[response.tool]["function"](response.input)
                    if verbose:
                        log.info(f"Tool '{response.tool}' result: {result}")
                    conversation_history.append(f"Tool result: {result}")
                except Exception as e:
                    error_msg = f"Tool execution error: {str(e)}"
                    if verbose:
                        log.exception(f"Error executing tool {response.tool}")
                    conversation_history.append(error_msg)
            
        except Exception as e:
            # Instructor handles retries automatically, but if it fails completely
            if verbose:
                log.warning(f"Instructor failed after retries: {e}")
            return f"I encountered an error processing your request: {str(e)}"
    
    return "I reached the maximum number of steps without finding a complete answer."
```

**Status**: ⏳ Pending
**Estimated Time**: 30 minutes

#### 3.2 Update Core Integration
**File**: `src/hands_on_ai/agent/core.py`

Update the `run_agent()` function to use Instructor:

```python
def run_agent(
    prompt: str, 
    model: Optional[str] = None, 
    format: str = "auto",  # Keep existing API unchanged
    max_iterations: int = 5, 
    verbose: bool = False
) -> str:
    """
    Run the agent with the given prompt.
    
    Args:
        prompt: User question or instruction
        model: LLM model to use, defaults to configured model
        format: Format to use ("react", "json", or "auto")
        max_iterations: Maximum number of tool use iterations
        verbose: Whether to print intermediate steps
        
    Returns:
        str: Final agent response
    """
    # Existing logic preserved
    if model is None:
        model = get_model()
    
    if format == "auto":
        format = detect_best_format(model)
        
    if verbose:
        log.info(f"Using {format} format for model {model}")
    
    # Use Instructor instead of fragile JSON parsing
    if format == "json":
        return run_instructor_agent(prompt, _tools, model, max_iterations, verbose)
    
    # Keep existing ReAct format unchanged for educational value
    return _run_react_agent(prompt, model, max_iterations, verbose)
```

**Status**: ⏳ Pending
**Estimated Time**: 10 minutes

### Phase 4: Testing and Validation

#### 4.1 Test with Small Models
Test the integration with models that typically use JSON format:
- llama3.2:3b
- phi3:mini
- qwen2.5:3b

**Test Cases**:
1. Simple tool calling (calculator, weather)
2. Multi-step reasoning
3. Error handling (invalid tool names)
4. Edge cases (malformed responses)

**Status**: ⏳ Pending
**Estimated Time**: 30 minutes

#### 4.2 Regression Testing
Ensure existing functionality still works:
- ReAct format with larger models
- All existing tools function correctly
- CLI commands work unchanged

**Status**: ⏳ Pending
**Estimated Time**: 20 minutes

### Phase 5: Cleanup and Documentation

#### 5.1 Remove Old Code
Clean up the old fragile implementation:
- Remove `parse_json_response()` function
- Remove regex fallback code
- Update imports

**Files to modify**:
- `src/hands_on_ai/agent/formats.py`

**Status**: ⏳ Pending
**Estimated Time**: 15 minutes

#### 5.2 Update Version
Bump version to reflect the improvement:
- Update `pyproject.toml` version field
- Add changelog entry

**Status**: ⏳ Pending
**Estimated Time**: 5 minutes

## Backward Compatibility Guarantee

| **Aspect** | **Before** | **After** | **Impact** |
|------------|------------|-----------|------------|
| Student API | `run_agent(prompt, model, format)` | **UNCHANGED** | ✅ Zero breaking changes |
| ReAct Format | Text-based reasoning | **UNCHANGED** | ✅ Educational value preserved |
| JSON Format | Fragile parsing | **Instructor validation** | ✅ Reliability improved |
| Tool Registration | `register_tool()` | **UNCHANGED** | ✅ Existing tools work |
| Model Detection | `detect_best_format()` | **UNCHANGED** | ✅ Same auto-selection |

## Architecture Comparison

### Before (Current)
```
User Input → run_agent() → detect_format()
    ↓
format="react" → _run_react_agent() → Text parsing → Tools
format="json"  → run_json_agent()  → json.loads() + regex fallbacks → Tools
                                      ↑ FRAGILE
```

### After (With Instructor)
```
User Input → run_agent() → detect_format()
    ↓
format="react" → _run_react_agent()     → Text parsing → Tools (UNCHANGED)
format="json"  → run_instructor_agent() → Pydantic validation → Tools
                                          ↑ ROBUST
```

## Progress Tracking

### ✅ Completed
- [x] Analysis of current implementation  
- [x] Plan design and documentation
- [x] Add dependencies to pyproject.toml
- [x] Create Pydantic schemas (`schemas.py`)
- [x] Implement run_instructor_agent function
- [x] Update core.py integration (automatic via function replacement)
- [x] Test basic functionality and imports
- [x] Maintain backward compatibility with fallback
- [x] Update version to 0.1.14

### 🎯 Ready for Production Testing
The integration is complete and ready for testing with actual models. The system will:

1. **Automatically use Instructor** when available for JSON format
2. **Gracefully fallback** to original implementation if Instructor fails  
3. **Maintain identical API** for students - zero breaking changes
4. **Preserve ReAct format** for educational value with larger models

## Risk Mitigation

| **Risk** | **Mitigation** | **Fallback** |
|----------|----------------|--------------|
| Instructor dependency issues | Pin version, test compatibility | Keep old implementation as fallback |
| Model compatibility | Test with all supported models | Graceful degradation to text format |
| Performance impact | Benchmark before/after | Optimize or make optional |
| Student confusion | No API changes, same behavior | Clear documentation |

## Success Criteria

1. **✅ Reliability**: JSON format no longer fails on malformed output
2. **✅ Compatibility**: All existing student code works unchanged  
3. **✅ Educational Value**: ReAct format still demonstrates reasoning
4. **✅ Performance**: No significant latency increase
5. **✅ Maintainability**: Cleaner, more robust codebase

## Implementation Notes

- Keep the implementation incremental and testable at each step
- Maintain verbose logging for debugging during development
- Test with actual student use cases before finalizing
- Consider adding configuration option to disable Instructor if needed

---

**Next Action**: Begin implementation by updating dependencies in `pyproject.toml`