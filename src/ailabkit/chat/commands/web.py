"""
Web command for the chat CLI - provides a web interface.
"""

import typer
from ..bots import list_available_bots, get_bot_description

app = typer.Typer(help="Launch web interface for Chat")


@app.callback(invoke_without_command=True)
def web(
    port: int = typer.Option(8000, help="Port to run the web server on"),
    host: str = typer.Option("127.0.0.1", "--host", help="Host to bind to"),
    public: bool = typer.Option(False, "--public", help="Make the interface accessible from other devices (binds to 0.0.0.0)"),
):
    """Launch web interface for Chat."""
    try:
        from fasthtml.common import (fast_app, Titled, Article, Form, Div, 
                                    Label, Select, Option, Input, Button, 
                                    Style, Script, serve)
    except ImportError:
        try:
            # Alternative import path if the package is installed as python-fasthtml
            from python_fasthtml.common import (fast_app, Titled, Article, Form, Div, 
                                              Label, Select, Option, Input, Button, 
                                              Style, Script, serve)
        except ImportError:
            print("❌ FastHTML is required for the web interface.")
            print("Please install it with: pip install python-fasthtml")
            raise typer.Exit(1)
    
    # Override host if public flag is set
    if public:
        host = "0.0.0.0"
        print("\n⚠️ PUBLIC MODE: Interface will be accessible from other devices on your network.")
    
    # Create FastHTML app
    app, rt = fast_app()
    
    # Get all available bots
    all_bots = list_available_bots()
    bot_options = {name: get_bot_description(bot) for name, bot in all_bots.items()}
    
    @rt("/")
    def get():
        # Generate bot options for the dropdown
        options = []
        for name, description in bot_options.items():
            display_name = name.replace("_bot", "").replace("_", " ").title()
            options.append(Option(f"{display_name} - {description}", value=name))
        
        return Titled("Chat Web Interface",
            Article(
                Form(
                    # Bot selector
                    Div(
                        Label("Select Bot Personality:"),
                        Select(*options, id="bot-select", name="bot"),
                    ),
                    # Chat history
                    Div(id="chat-history", cls="chat-container"),
                    # User input
                    Div(
                        Input(type="text", id="prompt", name="prompt", placeholder="Type your message here..."),
                        Button("Send", type="submit"),
                        cls="user-input"
                    ),
                    hx_post="/chat",
                    hx_target="#chat-history",
                    hx_swap="beforeend"
                ),
                Style("""
                    .chat-container {
                        height: 400px;
                        overflow-y: auto;
                        border: 1px solid #ddd;
                        padding: 10px;
                        margin-bottom: 10px;
                        display: flex;
                        flex-direction: column;
                    }
                    .message {
                        margin-bottom: 10px;
                        padding: 8px;
                        border-radius: 5px;
                        max-width: 80%;
                    }
                    .user-message {
                        background-color: #e3f2fd;
                        align-self: flex-end;
                        margin-left: auto;
                    }
                    .bot-message {
                        background-color: #f1f1f1;
                        align-self: flex-start;
                    }
                    .user-input {
                        display: flex;
                        gap: 10px;
                    }
                    #prompt {
                        flex-grow: 1;
                    }
                """),
                Script("""
                    document.querySelector('form').addEventListener('submit', function(e) {
                        // Prevent the default form submission
                        e.preventDefault();
                        
                        // Get the prompt value
                        const prompt = document.getElementById('prompt').value;
                        if (!prompt) return;
                        
                        // Create user message
                        const userMessage = document.createElement('div');
                        userMessage.classList.add('message', 'user-message');
                        userMessage.textContent = prompt;
                        document.getElementById('chat-history').appendChild(userMessage);
                        
                        // Get the bot selection
                        const bot = document.getElementById('bot-select').value;
                        
                        // Make the AJAX request
                        fetch('/chat', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                            body: `prompt=${encodeURIComponent(prompt)}&bot=${encodeURIComponent(bot)}`
                        })
                        .then(response => response.text())
                        .then(html => {
                            // Add the response to the chat history
                            const parser = new DOMParser();
                            const doc = parser.parseFromString(html, 'text/html');
                            const botMessage = doc.body.firstChild;
                            document.getElementById('chat-history').appendChild(botMessage);
                            
                            // Scroll to bottom
                            document.getElementById('chat-history').scrollTop = 
                                document.getElementById('chat-history').scrollHeight;
                            
                            // Clear the input
                            document.getElementById('prompt').value = '';
                            document.getElementById('prompt').focus();
                        });
                    });
                    
                    // Scroll to bottom when new content is added
                    const observer = new MutationObserver(function(mutations) {
                        const chatHistory = document.getElementById('chat-history');
                        chatHistory.scrollTop = chatHistory.scrollHeight;
                    });
                    
                    observer.observe(document.getElementById('chat-history'), { 
                        childList: true 
                    });
                """)
            )
        )
    
    @rt("/chat")
    def post(prompt: str, bot: str):
        bot_func = all_bots.get(bot)
        if not bot_func:
            return Div("Bot not found", cls="message bot-message")
        
        response = bot_func(prompt)
        return Div(response, cls="message bot-message")
    
    # Run the server
    display_host = "localhost" if host == "127.0.0.1" else host
    print(f"🌐 Starting Chat web interface on http://{display_host}:{port}")
    print("Press Ctrl+C to stop the server")
    
    # Serve the application
    serve(app=app, host=host, port=port)