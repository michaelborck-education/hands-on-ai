#!/usr/bin/env python3
import os
import shutil
import subprocess
import tempfile

# Create a temporary directory
temp_dir = tempfile.mkdtemp()
print(f"Created temporary directory: {temp_dir}")

try:
    # Copy source files
    shutil.copytree("src/ailabkit", os.path.join(temp_dir, "ailabkit"))
    shutil.copy("README.md", temp_dir)
    
    # Create setup.py
    setup_py = """
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="ailabkit",
    version="0.1.0",
    description="AI Learning Lab Toolkit for classrooms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Michael Borck",
    author_email="michael@borck.me",
    url="https://github.com/teaching-repositories/ailabkit",
    packages=find_packages(),
    install_requires=[
        "typer",
        "requests",
        "python-fasthtml",
        "python-docx", 
        "pymupdf", 
        "scikit-learn", 
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
"""
    
    with open(os.path.join(temp_dir, "setup.py"), "w") as f:
        f.write(setup_py)
    
    # Build the package
    print("Building the package...")
    subprocess.run(["python", "setup.py", "sdist"], cwd=temp_dir, check=True)
    
    # Upload to PyPI
    print("Uploading to PyPI...")
    try:
        # For real PyPI only
        subprocess.run(["twine", "upload", "dist/*"], cwd=temp_dir, check=True)
        print("✅ Package uploaded to PyPI successfully!")
    except Exception as e:
        print(f"Upload failed: {e}")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    # Clean up
    print(f"Cleaning up temporary directory: {temp_dir}")
    shutil.rmtree(temp_dir)