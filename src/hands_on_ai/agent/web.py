"""
Web interface for the agent module using FastHTML.
"""

import asyncio
from typing import List
import json

# Handle correct import for python-fasthtml package
try:
    from fasthtml import FastHTML, Request
    from fasthtml.utils import Sockets
except ImportError:
    try:
        # Alternative import path if the package is installed as python-fasthtml
        from python_fasthtml import FastHTML, Request
        from python_fasthtml.utils import Sockets
    except ImportError:
        raise ImportError(
            "FastHTML is required for the web interface. "
            "Please install it with: pip install python-fasthtml"
        )
from ..config import log
from .core import run_agent

# Register tools from built-in agents
from .agents.calculator import register_calculator_agent
from .agents.dictionary import register_dictionary_agent
from .agents.converter import register_converter_agent
from .agents.text_tools import register_text_tools
from .agents.datetime_tools import register_datetime_tools
from .agents.education_tools import register_education_tools

# Register all agent tools
register_calculator_agent()
register_dictionary_agent()
register_converter_agent()
register_text_tools()
register_datetime_tools()
register_education_tools()

# Create FastHTML app
app = FastHTML(
    title="HandsOnAI Agent",
    description="ReAct-style reasoning agent with tool use",
    static_dir=None
)

@app.page("/")
async def index():
    """
    Render the main agent interface.
    """
    return """
    <div class="container mx-auto px-4 py-8 max-w-4xl">
        <h1 class="text-3xl font-bold mb-6">HandsOnAI Agent</h1>
        
        <div class="mb-4">
            <div class="flex items-center mb-2">
                <label class="mr-4 font-semibold">Available Tools:</label>
                <div id="tool-badges" class="flex flex-wrap gap-2">
                    {% for tool in tools %}
                    <span class="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-medium">
                        {{ tool.name }}
                    </span>
                    {% endfor %}
                </div>
            </div>
            <div class="mb-6">
                <div class="flex items-center">
                    <label for="show-trace" class="mr-2">Show reasoning:</label>
                    <input type="checkbox" id="show-trace" class="form-checkbox">
                </div>
            </div>
        </div>
        
        <!-- Chat log will be displayed here -->
        <div id="chat-log" class="mb-4 h-96 overflow-y-auto p-4 border rounded bg-gray-50">
            <div class="text-gray-500 italic">Ask the agent a question to get started...</div>
        </div>
        
        <!-- User input form -->
        <form id="prompt-form" class="flex">
            <input 
                type="text" 
                id="prompt" 
                placeholder="What would you like to ask?" 
                class="flex-grow p-2 border rounded mr-2"
                required
            >
            <button 
                type="submit" 
                class="bg-blue-600 text-white px-4 py-2 rounded"
            >
                Send
            </button>
        </form>
    </div>
    
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const chatLog = document.getElementById('chat-log');
        const promptForm = document.getElementById('prompt-form');
        const promptInput = document.getElementById('prompt');
        const showTrace = document.getElementById('show-trace');
        
        // WebSocket setup
        const socket = new WebSocket(`ws://${window.location.host}/ws`);
        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            if (data.type === 'agent_response') {
                appendAgentMessage(data.content, data.trace, showTrace.checked);
                promptInput.disabled = false;
                promptForm.querySelector('button').disabled = false;
            } else if (data.type === 'error') {
                appendErrorMessage(data.content);
                promptInput.disabled = false;
                promptForm.querySelector('button').disabled = false;
            }
        };
        
        // Handle form submission
        promptForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const prompt = promptInput.value.trim();
            if (prompt) {
                appendUserMessage(prompt);
                promptInput.value = '';
                promptInput.disabled = true;
                promptForm.querySelector('button').disabled = true;
                
                // Show "thinking" message
                appendThinkingMessage();
                
                // Send to server
                socket.send(JSON.stringify({
                    action: 'run_agent',
                    prompt: prompt,
                    show_trace: showTrace.checked
                }));
            }
        });
        
        // Helper to append user message
        function appendUserMessage(text) {
            const div = document.createElement('div');
            div.className = 'mb-3';
            div.innerHTML = `
                <div class="flex items-start">
                    <div class="bg-blue-100 p-3 rounded-lg inline-block max-w-[80%]">
                        <p class="text-sm"><strong>You:</strong> ${escapeHtml(text)}</p>
                    </div>
                </div>
            `;
            chatLog.appendChild(div);
            chatLog.scrollTop = chatLog.scrollHeight;
        }
        
        // Helper to append agent message
        function appendAgentMessage(text, trace, showTrace) {
            // Remove the thinking indicator
            const thinkingElem = document.querySelector('.thinking-indicator');
            if (thinkingElem) {
                thinkingElem.remove();
            }
            
            const div = document.createElement('div');
            div.className = 'mb-3';
            
            let traceHtml = '';
            if (showTrace && trace && trace.length > 0) {
                traceHtml = `
                    <details class="mt-2 bg-gray-100 p-2 rounded text-xs">
                        <summary class="cursor-pointer text-gray-600">View reasoning</summary>
                        <pre class="whitespace-pre-wrap mt-2 text-gray-800">${escapeHtml(trace.join('\\n\\n'))}</pre>
                    </details>
                `;
            }
            
            div.innerHTML = `
                <div class="flex items-start justify-end">
                    <div class="bg-green-100 p-3 rounded-lg inline-block max-w-[80%]">
                        <p class="text-sm"><strong>Agent:</strong> ${escapeHtml(text)}</p>
                        ${traceHtml}
                    </div>
                </div>
            `;
            chatLog.appendChild(div);
            chatLog.scrollTop = chatLog.scrollHeight;
        }
        
        // Helper to append error message
        function appendErrorMessage(text) {
            // Remove the thinking indicator
            const thinkingElem = document.querySelector('.thinking-indicator');
            if (thinkingElem) {
                thinkingElem.remove();
            }
            
            const div = document.createElement('div');
            div.className = 'mb-3';
            div.innerHTML = `
                <div class="flex items-start justify-end">
                    <div class="bg-red-100 p-3 rounded-lg inline-block max-w-[80%]">
                        <p class="text-sm"><strong>Error:</strong> ${escapeHtml(text)}</p>
                    </div>
                </div>
            `;
            chatLog.appendChild(div);
            chatLog.scrollTop = chatLog.scrollHeight;
        }
        
        // Helper to show "thinking" indicator
        function appendThinkingMessage() {
            const div = document.createElement('div');
            div.className = 'mb-3 thinking-indicator';
            div.innerHTML = `
                <div class="flex items-start justify-end">
                    <div class="bg-gray-100 p-3 rounded-lg inline-block">
                        <p class="text-sm flex items-center">
                            <strong>Agent:</strong> 
                            <span class="ml-2">Thinking</span>
                            <span class="ml-1 dots">...</span>
                        </p>
                    </div>
                </div>
            `;
            chatLog.appendChild(div);
            chatLog.scrollTop = chatLog.scrollHeight;
            
            // Animate the dots
            const dots = div.querySelector('.dots');
            let count = 0;
            const interval = setInterval(() => {
                count = (count + 1) % 4;
                dots.textContent = '.'.repeat(count || 3);
            }, 300);
            
            // Store the interval ID in the DOM element to clear it later
            div.dataset.intervalId = interval;
        }
        
        // Helper to escape HTML
        function escapeHtml(html) {
            const div = document.createElement('div');
            div.textContent = html;
            return div.innerHTML;
        }
    });
    </script>
    """

@app.websocket("/ws")
async def websocket_handler(socket: Sockets, request: Request):
    """
    Handle WebSocket connections for agent interactions.
    """
    await socket.accept()
    
    try:
        async for message in socket:
            data = json.loads(message)
            
            if data.get("action") == "run_agent":
                prompt = data.get("prompt", "")
                show_trace = data.get("show_trace", False)
                
                try:
                    # Process in a separate task to not block
                    response, trace = await asyncio.get_event_loop().run_in_executor(
                        None, 
                        lambda: process_agent_query(prompt, show_trace)
                    )
                    
                    await socket.send(json.dumps({
                        "type": "agent_response",
                        "content": response,
                        "trace": trace if show_trace else []
                    }))
                except Exception as e:
                    log.exception("Error in agent processing")
                    await socket.send(json.dumps({
                        "type": "error",
                        "content": f"An error occurred: {str(e)}"
                    }))
    except Exception:
        log.exception("WebSocket error")
    finally:
        await socket.close()

def process_agent_query(prompt: str, capture_trace: bool = False) -> tuple[str, List[str]]:
    """
    Process an agent query and optionally capture the reasoning trace.
    
    Args:
        prompt: The user's question
        capture_trace: Whether to capture and return the reasoning trace
        
    Returns:
        tuple: (final_response, trace)
    """
    # The trace is only used if capture_trace is True
    trace = []
    
    # Get the actual response
    response = run_agent(prompt, verbose=capture_trace)
    
    # In a real implementation, the trace would be captured from the agent
    # For now, we'll just return a simplified trace
    if capture_trace:
        trace = [
            f"Question: {prompt}",
            "Thinking about how to approach this...",
            "Using available tools to solve the problem."
        ]
    
    return response, trace

def run_web_server(host="127.0.0.1", port=8002):
    """Start the agent web server."""
    app.run(host=host, port=port)