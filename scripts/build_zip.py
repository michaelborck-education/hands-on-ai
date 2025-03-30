#!/usr/bin/env python3

# build_zip.py - Create offline zip bundle of project browser + docs

import zipfile
from pathlib import Path
import subprocess

ZIP_NAME = "AiLabKit_Offline_Bundle.zip"
PROJECT_BROWSER = Path("tools/project_browser.html")
PROJECT_DIR = Path("docs/projects")

# Step 1: Generate project_browser.html if not present
if not PROJECT_BROWSER.exists():
    print("⚙️  Generating project_browser.html...")
    subprocess.run(["python", "tools/split_and_overview.py", "--build-browser"], check=True)

# Step 2: Create ZIP bundle
with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as zipf:
    if PROJECT_DIR.exists():
        for file in PROJECT_DIR.rglob("*.*"):
            zipf.write(file, arcname=file.relative_to("."))
    if PROJECT_BROWSER.exists():
        zipf.write(PROJECT_BROWSER, arcname=PROJECT_BROWSER.relative_to("."))

print(f"✅ Created: {ZIP_NAME}")
