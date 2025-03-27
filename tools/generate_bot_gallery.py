import inspect
import chatcraft
import argparse
import sys
import re
import csv
from collections import defaultdict
from io import StringIO

BOT_TEMPLATE = '''def your_bot_name(prompt):
    """
    🤖 Your Bot Title

    One-line summary of your bot's personality.

    ```python
    from chatcraft import your_bot_name
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
'''

HEADER = """# 🤖 ChatCraft Bot Gallery

This gallery lists all available personality bots in ChatCraft. Each bot can be called with a prompt and will respond in its own unique style.

Below you'll find each bot's name and its docstring, which includes usage examples, educational applications, and example responses (as written in the docstring).

---
"""

def is_bot_func(obj):
    return callable(obj) and obj.__name__.endswith('_bot')

def extract_bots():
    bots = []
    for name in dir(chatcraft):
        obj = getattr(chatcraft, name)
        if is_bot_func(obj):
            doc = inspect.getdoc(obj)
            bots.append((name, doc))
    return bots

def parse_educational_tags(doc):
    if not doc:
        return []
    match = re.search(r"\*\*Educational Uses:\*\*(.*?)\n\n", doc, re.DOTALL)
    if match:
        tags = re.findall(r"- (.+)", match.group(1))
        return [t.strip() for t in tags]
    return []

def generate_markdown(bots, lint=False, include_header=True, flat=False):
    if lint:
        return "\n".join([f"⚠️ `{name}` is missing a docstring." for name, doc in bots if not doc])

    lines = [HEADER] if include_header else []

    if flat:
        for name, doc in sorted(bots):
            if doc:
                lines.append(f"### `{name}`\n{doc}\n")
    else:
        tag_sections = defaultdict(list)
        for name, doc in bots:
            if doc:
                tags = parse_educational_tags(doc)
                if not tags:
                    tag_sections["Uncategorized"].append((name, doc))
                else:
                    for tag in tags:
                        tag_sections[tag].append((name, doc))

        for tag, items in sorted(tag_sections.items()):
            lines.append(f"\n## 🏷️ {tag}\n")
            for name, doc in sorted(items):
                lines.append(f"### `{name}`\n{doc}\n")

    return "\n".join(lines)

def generate_csv(bots):
    csv_output = StringIO()
    writer = csv.writer(csv_output)
    writer.writerow(["Bot Name", "Educational Tag"])

    for name, doc in bots:
        if not doc:
            continue
        tags = parse_educational_tags(doc)
        if not tags:
            writer.writerow([name, "Uncategorized"])
        else:
            for tag in tags:
                writer.writerow([name, tag])

    return csv_output.getvalue()

def main():
    parser = argparse.ArgumentParser(description="Generate or lint ChatCraft bot gallery.")
    parser.add_argument("--lint", action="store_true", help="Check for missing docstrings only.")
    parser.add_argument("--out", type=str, help="Path to output file. If not set, prints to stdout.")
    parser.add_argument("--template", action="store_true", help="Print a template for creating a new bot.")
    parser.add_argument("--no-header", action="store_true", help="Exclude the header section from output.")
    parser.add_argument("--flat", action="store_true", help="Disable section grouping and print all bots in one list.")
    parser.add_argument("--csv", action="store_true", help="Output a CSV file instead of Markdown.")
    args = parser.parse_args()

    if args.template:
        print(BOT_TEMPLATE)
        return

    bots = extract_bots()

    if args.csv:
        output = generate_csv(bots)
    else:
        output = generate_markdown(bots, lint=args.lint, include_header=not args.no_header, flat=args.flat)

    if args.out:
        with open(args.out, "w") as f:
            f.write(output)
        print(f"✅ Bot gallery written to {args.out}")
    else:
        print(output)

if __name__ == "__main__":
    main()
