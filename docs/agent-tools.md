# Agent Tools Reference

The Agent module in AiLabKit provides a collection of tools that enable LLMs to perform specific tasks in a tool-using, reasoning framework. These tools are organized into different categories based on their functionality.

## Core Tools

These are the basic tools that come with the agent module for fundamental tasks.

### Calculator Tool

The calculator tool allows the agent to perform mathematical calculations safely.

- **Name**: `calculator`
- **Description**: Evaluate a mathematical expression
- **Example Input**: `2 + 2 * 10`
- **Example Output**: `Result: 22`
- **Functionality**: Supports basic arithmetic operations and math functions in a secure evaluation environment

### Weather Tool

The weather tool provides simulated weather data for educational purposes.

- **Name**: `weather`
- **Description**: Get the current weather for a location (simulated)
- **Example Input**: `New York`
- **Example Output**: Simulated weather data including temperature, humidity, and conditions
- **Note**: This is a simulated tool and does not fetch real weather data

### Search Tool

The search tool provides simulated search results for educational purposes.

- **Name**: `search`
- **Description**: Search the web for information (simulated)
- **Example Input**: `Python programming`
- **Example Output**: Simulated search results with information about the query
- **Note**: This is a simulated tool with predefined results for topics like "Python programming", "artificial intelligence", and "climate change"

## Text Analysis Tools

Tools for analyzing and manipulating text content.

### Word Count

Analyzes text to provide word, character, and sentence statistics.

- **Name**: `word_count`
- **Description**: Count words, characters, sentences, and paragraphs in a text
- **Example Input**: Any text content
- **Output**: Statistics including word count, character count, sentence count, paragraph count, unique words, and average word length

### Readability Score

Calculates readability metrics to determine text complexity.

- **Name**: `readability`
- **Description**: Calculate readability scores for text
- **Example Input**: Any text content
- **Output**: 
  - Flesch Reading Ease score and interpretation
  - Flesch-Kincaid Grade Level
  - SMOG Index
  - Text statistics (sentences, words, syllables, etc.)

### Text Summarizer

Creates concise summaries of longer text.

- **Name**: `summarize`
- **Description**: Create a summary of text
- **Example Input**: Long text content
- **Parameters**: `ratio` (0.1-0.5) controls summary length
- **Output**: Extractive summary highlighting the most important sentences

## Educational Tools

Tools designed for educational content and calculations.

### Periodic Table

Provides information about chemical elements.

- **Name**: `periodic_table`
- **Description**: Look up information about an element in the periodic table
- **Example Input**: Element name (e.g., "oxygen") or symbol (e.g., "O")
- **Output**: Element details including symbol, atomic number, atomic weight, category, group, and period

### Multiplication Table

Generates a formatted multiplication table.

- **Name**: `multiplication_table`
- **Description**: Generate a multiplication table for a given number
- **Example Input**: Base number (e.g., "7") and size (e.g., "12")
- **Output**: Formatted multiplication table showing products

### Prime Number Checker

Determines if a number is prime and provides related information.

- **Name**: `prime_check`
- **Description**: Check if a number is prime and get related information
- **Example Input**: Any integer
- **Output**: Prime status, factors (if not prime), and nearest prime numbers

## Date and Time Tools

Tools for working with dates and time calculations.

### Date Difference Calculator

Calculates the time span between two dates.

- **Name**: `date_diff`
- **Description**: Calculate the difference between two dates
- **Example Input**: Two dates in YYYY-MM-DD format
- **Output**: Time span in years, months, days, and total days

### Date Formatter

Converts dates to different formats.

- **Name**: `format_date`
- **Description**: Format a date in different styles
- **Example Input**: Date in YYYY-MM-DD format
- **Parameters**: Format code (iso, short, medium, long, full)
- **Output**: Date in the requested format

### Days Until Calculator

Calculates days until a future date.

- **Name**: `days_until`
- **Description**: Calculate days until a specific date
- **Example Input**: Target date in YYYY-MM-DD format
- **Output**: Time remaining until the target date

## Dictionary Tools

Tools for language and vocabulary assistance.

### Word Lookup

Provides definitions and examples for words.

- **Name**: `define`
- **Description**: Look up the definition of a word
- **Example Input**: Any English word
- **Output**: Word definitions, part of speech, and usage examples

### Synonym Finder

Finds synonyms for a given word.

- **Name**: `synonyms`
- **Description**: Find synonyms for a word
- **Example Input**: Any English word
- **Output**: List of synonyms with similar meanings

## Unit Conversion Tools

Tools for converting between different units of measurement.

### Temperature Converter

Converts between temperature units.

- **Name**: `convert_temperature`
- **Description**: Convert between Celsius, Fahrenheit, and Kelvin
- **Example Input**: Value and source/target units
- **Output**: Converted temperature value

### Length Converter

Converts between length/distance units.

- **Name**: `convert_length`
- **Description**: Convert between units like meters, feet, inches, kilometers, miles
- **Example Input**: Value and source/target units
- **Output**: Converted length value

### Weight Converter

Converts between weight/mass units.

- **Name**: `convert_weight`
- **Description**: Convert between units like grams, kilograms, pounds, ounces
- **Example Input**: Value and source/target units
- **Output**: Converted weight value

## Using Tools in AiLabKit

Agents can use these tools to assist with tasks by following a reasoning process:

1. The agent receives a question or task from the user
2. The agent thinks about what tools might help solve the problem
3. The agent calls one or more tools with appropriate inputs
4. The agent uses the tool results to formulate a response

### Example Usage

```python
from ailabkit.agent import run_agent

# Ask a question that requires tool use
response = run_agent("What is the atomic weight of oxygen and what is 25 × 16?")

# The agent might use the periodic_table tool for the element info
# and the calculator tool for the multiplication
print(response)
```

### Command Line Usage

Tools can also be accessed via the command line:

```bash
# List all available tools
agent tools

# Ask the agent a question that requires tool use
agent ask "How many days until December 25, 2023?"
```
