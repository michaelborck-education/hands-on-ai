# build_zip.py - Create offline zip bundle of project browser + docs

import zipfile
from pathlib import Path

ZIP_NAME = "ChatCraft_Offline_Bundle.zip"
OUTPUT_DIRS = [
    Path("docs/projects"),
    Path("tools/project_browser.html")
]

with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as zipf:
    for path in OUTPUT_DIRS:
        if path.is_dir():
            for file in path.rglob("*.*"):
                zipf.write(file, arcname=file.relative_to("."))
        elif path.is_file():
            zipf.write(path, arcname=path.relative_to("."))

print(f"✅ Created: {ZIP_NAME}")
