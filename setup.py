#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="ailabkit",
    version="0.1.0",
    description="AI Learning Lab Toolkit for classrooms",
    author="Michael Borck",
    author_email="michael@borck.me",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "requests", 
        "typer",
        "python-fasthtml",
        "python-docx", 
        "pymupdf", 
        "scikit-learn", 
        "numpy"
    ],
    entry_points={
        "console_scripts": [
            "ailabkit=ailabkit.cli:app",
            "chat=ailabkit.chat.cli:app",
            "rag=ailabkit.rag.cli:app",
            "agent=ailabkit.agent.cli:app",
        ],
    },
    python_requires=">=3.8",
)