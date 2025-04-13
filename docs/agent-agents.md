# Agent Modules Reference

The Agent system in Hands-On AI includes several specialized agent modules, each focused on different domains of functionality. Each agent module registers a set of related tools that can be used together to solve specific types of problems.

## Calculator Agent

The Calculator Agent provides mathematical computation tools ranging from basic arithmetic to advanced formulas and equation solving.

### Tools Provided

1. **calc**
   - **Description**: Evaluate a basic mathematical expression
   - **Input**: Mathematical expression as text (e.g., "2 + 2 * 3")
   - **Output**: Numerical result
   - **Capabilities**: Basic arithmetic (+, -, *, /), common functions (abs, round, max, min, sum, pow)
   - **Safety**: Uses restricted evaluation environment to prevent code execution

2. **advanced_calc**
   - **Description**: Evaluate advanced mathematical expressions with scientific functions
   - **Input**: Mathematical expression including advanced functions (e.g., "sqrt(16) + sin(pi/2)")
   - **Output**: Numerical result
   - **Capabilities**: All basic arithmetic plus trigonometric functions (sin, cos, tan), logarithms (log, log10), exponentiation (exp), constants (pi, e), and more
   - **Safety**: Uses restricted evaluation environment with controlled access to math functions

3. **solve_quadratic**
   - **Description**: Solve a quadratic equation in the form ax² + bx + c = 0
   - **Input**: Three coefficients (a, b, c)
   - **Output**: Solutions to the equation
   - **Capabilities**: 
     - Finds both real and complex solutions
     - Handles special cases (discriminant = 0)
     - Provides formatted output with explanations

### Example Usage

```
> solve_quadratic(1, -3, 2)
Two real solutions: x = 2.0 or x = 1.0

> advanced_calc("sin(pi/2) + sqrt(16)")
5.0
```

## Dictionary Agent

The Dictionary Agent provides language assistance tools for looking up word meanings and relationships.

### Tools Provided

1. **define**
   - **Description**: Look up the definition of a word
   - **Input**: A single word
   - **Output**: The word's definition
   - **Note**: Uses a built-in dictionary with common words

2. **synonyms**
   - **Description**: Find synonyms (words with similar meaning)
   - **Input**: A single word
   - **Output**: List of synonyms for the word
   - **Example**: For "happy" → joyful, cheerful, delighted, pleased, content

3. **antonyms**
   - **Description**: Find antonyms (words with opposite meaning)
   - **Input**: A single word
   - **Output**: List of antonyms for the word
   - **Example**: For "happy" → sad, unhappy, miserable, depressed

4. **examples**
   - **Description**: Find example sentences using a word
   - **Input**: A single word
   - **Output**: Sample sentences demonstrating the word's usage
   - **Example**: For "happy" → "I'm happy to see you.", "They were a happy family."

### Example Usage

```
> define("happy")
Feeling or showing pleasure or contentment.

> synonyms("happy")
Synonyms for 'happy': joyful, cheerful, delighted, pleased, content
```

## Converter Agent

The Converter Agent provides tools for converting values between different units of measurement.

### Tools Provided

1. **convert**
   - **Description**: General-purpose unit conversion tool
   - **Input**: Value, source unit, and target unit
   - **Output**: Converted value
   - **Capabilities**: Automatically detects unit types and performs appropriate conversion
   - **Error Handling**: Prevents cross-category conversions (e.g., length to weight)

2. **convert_length**
   - **Description**: Convert between length units
   - **Input**: Value, source unit, and target unit
   - **Output**: Converted length value
   - **Supported Units**: m, km, cm, mm, in, ft, yd, mi

3. **convert_weight**
   - **Description**: Convert between weight units
   - **Input**: Value, source unit, and target unit
   - **Output**: Converted weight value
   - **Supported Units**: g, kg, mg, lb, oz, st, ton, tonne

4. **convert_temperature**
   - **Description**: Convert between temperature units
   - **Input**: Value, source unit, and target unit
   - **Output**: Converted temperature value
   - **Supported Units**: c (Celsius), f (Fahrenheit), k (Kelvin)

### Example Usage

```
> convert_length(5, "m", "ft")
5 m = 16.4 ft

> convert_temperature(32, "f", "c")
32 °F = 0 °C
```

## Text Tools Agent

The Text Tools Agent provides tools for analyzing and manipulating text content.

### Tools Provided

1. **word_count**
   - **Description**: Count words, characters, sentences, and paragraphs in text
   - **Input**: Text content
   - **Output**: Text statistics including word count, character count, sentence count, paragraph count, unique words, and average word length

2. **readability**
   - **Description**: Calculate readability scores for text
   - **Input**: Text content
   - **Output**: Readability metrics including:
     - Flesch Reading Ease score and interpretation
     - Flesch-Kincaid Grade Level
     - SMOG Index
     - Text statistics (words per sentence, syllables per word)

3. **summarize**
   - **Description**: Create a summary of text
   - **Input**: Text content and optional ratio parameter (0.1-0.5)
   - **Output**: Extractive summary highlighting key sentences
   - **Algorithm**: Uses frequency analysis and position-based weighting to select important sentences

### Example Usage

```
> word_count("This is a sample text. It has two sentences.")
Word count: 9
Character count: 45
Character count (without spaces): 37
Sentence count: 2
Paragraph count: 1
Unique words: 8
Average word length: 3.8 characters
```

## Education Tools Agent

The Education Tools Agent provides tools for educational purposes across various subjects.

### Tools Provided

1. **periodic_table**
   - **Description**: Look up element information in the periodic table
   - **Input**: Element name or symbol
   - **Output**: Element details including symbol, atomic number, atomic weight, category, group, and period
   - **Coverage**: Includes common elements with detailed properties

2. **multiplication_table**
   - **Description**: Generate a multiplication table for a number
   - **Input**: Base number and optional size parameter
   - **Output**: Formatted multiplication table
   - **Example**: For input 7, generates a table of 7×1 through 7×10

3. **prime_check**
   - **Description**: Check if a number is prime
   - **Input**: Integer number
   - **Output**: Prime status, factors (if not prime), and nearest prime numbers
   - **Capabilities**: Efficiently determines primality and provides educational context

### Example Usage

```
> periodic_table("oxygen")
Element: Oxygen
Symbol: O
Atomic Number: 8
Atomic Weight: 15.999
Category: Nonmetal
Group: 16
Period: 2

> prime_check(17)
17 is a prime number.
The next prime number is 19.
The previous prime number is 13.
```

## Date and Time Tools Agent

The Date and Time Tools Agent provides tools for working with dates and time calculations.

### Tools Provided

1. **date_diff**
   - **Description**: Calculate the difference between two dates
   - **Input**: Two dates in YYYY-MM-DD format
   - **Output**: Time span in years, months, days, and total days
   - **Features**: Handles date ordering automatically, provides human-readable output

2. **format_date**
   - **Description**: Format a date in different styles
   - **Input**: Date in YYYY-MM-DD format and optional format code
   - **Output**: Date in the requested format
   - **Format Options**: iso, short, medium, long, full

3. **days_until**
   - **Description**: Calculate days until a future date
   - **Input**: Target date in YYYY-MM-DD format
   - **Output**: Time remaining until the target date
   - **Features**: Different output formats based on timeframe (days, weeks, months)

### Example Usage

```
> date_diff("2023-01-01", "2023-12-31")
Difference between 2023-01-01 and 2023-12-31:
0 years, 11 months, 30 days
Total: 364 days

> days_until("2023-12-25")
There are 85 days until 2023-12-25 (about 12 weeks)
```

## Using Agents in Hands-On AI

Agents are collections of related tools designed to work together. When you run the Hands-On AI agent system, it has access to all these specialized agents and can choose the appropriate tools based on the task.

### Via Python API

```python
from hands_on_ai.agent import run_agent

response = run_agent("Convert 25 degrees Celsius to Fahrenheit and tell me if it's hot or cold.")
print(response)
```

### Via Command Line

```bash
agent ask "What's the atomic weight of oxygen, and can you convert 5 miles to kilometers?"
```

In both cases, the agent system will:
1. Analyze the task
2. Select the appropriate tools (periodic_table from Education Tools Agent and convert_length from Converter Agent)
3. Execute the tools with the correct parameters
4. Combine the results into a coherent response

This modular agent system allows Hands-On AI to handle a wide range of tasks with specialized, purpose-built tools that can work together seamlessly.
