# First element is preamble (if any), then alternating: title, body, title, body...
overview_lines = ["# 📚 Mini Projects Overview\n"]

for i in range(1, len(projects), 2):
    title = projects[i].strip()
    body = projects[i + 1].strip()

    # Generate filename from title
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", title.lower()).strip("-")
    filename = PROJECT_DIR / f"{slug}.md"

    # Write each project
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{body}\n")

    # Add to overview with link
    overview_lines.append(f"- [{title}](./{slug}.md)")

# Write index/overview
with open(OVERVIEW_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(overview_lines))

print(f"✅ Split {len(projects) // 2} projects into: {PROJECT_DIR}/")
print(f"✅ Overview written to: {OVERVIEW_FILE}")
