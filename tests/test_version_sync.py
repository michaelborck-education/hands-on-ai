from pathlib import Path
import json
import re

def test_version_consistency():
    version = json.loads(Path("version.json").read_text())["version"]

    html = Path("tools/project_browser.html").read_text()
    assert f'const CURRENT_VERSION = "{version}"' in html

    toml = Path("pyproject.toml").read_text()
    assert f'version = "{version}"' in toml
