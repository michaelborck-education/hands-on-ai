#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="hands-on-ai",
    version="0.1.0",
    description="Hands-on AI Toolkit for classrooms",
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
            "handsonai=hands_on_ai.cli:app",
            "chat=hands_on_ai.chat.cli:app",
            "rag=hands_on_ai.rag.cli:app",
            "agent=hands_on_ai.agent.cli:app",
        ],
    },
    python_requires=">=3.8",
)