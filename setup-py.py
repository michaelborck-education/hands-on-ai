from setuptools import setup, find_packages

setup(
    name="chatcraft",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    author="Michael Borck",
    author_email="michael.borck@curtin.edu.au",
    description="LLMs made simple for students and educators",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/teaching-repositories/chatcraft", 
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="llm, education, chatbot, ai, teaching, learning, ollama",
    project_urls={
        "Bug Reports": "https://github.com/teaching-repositories/chatcraft/issues",
        "Source": "https://github.com/teaching-repositories/chatcraft",
    },
    python_requires=">=3.6",
)