import typer
from rich import print
import requests
from chatcraft import get_response
from chatcraft.config import get_server_url, load_fallbacks
from chatcraft.bots import list_available_bots, get_bot, get_bot_description

app = typer.Typer()

# Default state for REPL
current_bot_name = "friendly_bot"

def check_server():
    """Check if Ollama server is running."""
    url = get_server_url()
    try:
        r = requests.get(f"{url}/api/tags", timeout=2)
        if r.status_code == 200:
            return True
    except Exception:
        pass
    return False

@app.command()
def ask(
    prompt: str = typer.Argument(..., help="Prompt to send to the chatbot."),
    personality: str = typer.Option("friendly_bot", help="Bot personality to use")
):
    "Send a single prompt to a bot."
    bot = get_bot(personality)
    if not bot:
        print(f"[red]❌ Bot '{personality}' not found. Try /bots for options.[/red]")
        raise typer.Exit(1)
    print(bot(prompt))


@app.command()
def bots():
    "List available bots."
    for name, func in list_available_bots().items():
        doc = get_bot_description(func)
        print(f"[bold cyan]{name}[/bold cyan]: {doc}")



@app.command()
def doctor():
    "Run diagnostics to check Ollama server and model availability."
    print("🩺 Running ChatCraft environment check...\n")
    if check_server():
        print("✅ Ollama server is reachable.")
    else:
        print("[red]❌ Ollama server not reachable. Make sure it's running on localhost.[/red]")
        raise typer.Exit(1)

@app.command()
def interactive():
    "Start interactive REPL (no memory)."
    global current_bot_name

    if not check_server():
        print("[red]❌ Ollama server is not reachable. Run `chatcraft doctor` for help.[/red]")
        raise typer.Exit(1)

    print("\n🤖 [bold]ChatCraft CLI[/bold] — stateless REPL, no memory between prompts.")
    print("Type /help for commands.\n")

    bot = get_bot(current_bot_name)
    if not bot:
        print(f"[red]❌ Default bot '{current_bot_name}' not found.[/red]")
        return

    while True:
        try:
            user_input = input("💬 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Exiting ChatCraft.")
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            command, *args = user_input[1:].split()
            if command == "exit":
                print("👋 Goodbye!")
                break
            elif command == "help":
                print("""
🤖 [bold]ChatCraft CLI[/bold] — stateless REPL, no memory between prompts.
📖 [bold]Available commands:[/bold]
  /help              Show this help message
  /exit              Exit the REPL
  /bots              List all available bot personalities
  /personality NAME  Switch to another bot personality (e.g., /personality pirate)
  /doctor            Check Ollama server status
                """)
            elif command == "bots":
                bots()
            elif command == "doctor":
                doctor()
            elif command == "personality":
                if not args:
                    print("[red]⚠️ Usage: /personality NAME[/red]")
                else:
                    name = args[0]
                    new_bot = get_bot(name)
                    if new_bot:
                        current_bot_name = name
                        bot = new_bot
                        print(f"✅ Switched to bot: [cyan]{name}[/cyan]")
                    else:
                        print(f"[red]❌ No bot named '{name}'. Try /bots[/red]")
            else:
                print(f"[red]⚠️ Unknown command: /{command}[/red]")
        else:
            response = bot(user_input)
            print(f"🤖 {response}\n")

if __name__ == "__main__":
    app()
