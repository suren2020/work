# Flashcard Quizzer CLI Application

A command-line flashcard quiz application built with Python, implementing the Strategy pattern and following SOLID principles.

## Architecture

The application uses the **Strategy Pattern** to enable different quiz algorithms while maintaining clean separation of concerns:

### Core Components

- **QuizStrategy** (Abstract Base Class): Defines interface for quiz strategies
- **FlashcardQuizStrategy**: Sequential flashcard quiz implementation  
- **RandomQuizStrategy**: Randomized order quiz implementation
- **AdaptiveQuizStrategy**: Smart quiz focusing on missed cards
- **QuizContext**: Manages and orchestrates quiz execution
- **MenuSystem**: Handles strategy selection and quiz flow
- **Flashcard**: Immutable data model with validation
- **JSONLoader**: Handles data ingestion and validation
- **CLIInterface**: Manages user interaction and display

### SOLID Principles Applied

- **Single Responsibility**: Each class has one clear purpose
- **Open/Closed**: Easy to add new quiz strategies without modifying existing code
- **Liskov Substitution**: Quiz strategies are interchangeable
- **Interface Segregation**: Clean, focused interfaces
- **Dependency Inversion**: High-level modules depend on abstractions

## Usage

```bash
python main.py -f <json_file_path>
```

### Command Line Arguments

- `-f, --file`: Path to JSON file containing flashcard data (required)
- `-h, --help`: Show help message

### Menu Options

1. **Sequential**: Quiz through flashcards in original order
2. **Random**: Quiz through flashcards in randomized order  
3. **Adaptive**: Review previously missed cards first, then full quiz
4. **Exit**: Quit the application

### JSON File Formats

**Array Format:**
```json
[
  {
    "front": "Question text",
    "back": "Answer text"
  },
  {
    "front": "Another question",
    "back": "Another answer"
  }
]
```

**Object Format:**
```json
{
  "cards": [
    {
      "front": "Question text", 
      "back": "Answer text"
    },
    {
      "front": "Another question",
      "back": "Another answer"
    }
  ]
}
```

## Examples

```bash
python main.py -f sample_flashcards.json
python main.py --file sample_flashcards_object_format.json
```

## Features

- **Multiple Quiz Strategies**: Sequential, Random, and Adaptive modes
- **Comprehensive Reporting**: Accuracy percentage, missed terms list
- **Dual JSON Support**: Both array and object wrapper formats
- **Error Handling**: Graceful handling of malformed JSON and missing files
- **Case-insensitive Matching**: Flexible answer validation
- **Progress Tracking**: Real-time progress during quizzes
- **Adaptive Learning**: Focuses on previously missed flashcards
- **Keyboard Interrupt Support**: Ctrl+C handling

## Project Structure

```
├── main.py                                    # Application entry point
├── src/
│   ├── data/
│   │   └── json_loader.py                    # JSON data loading and validation
│   ├── models/
│   │   └── flashcard.py                      # Flashcard data model
│   ├── quiz/
│   │   ├── quiz_strategy.py                  # Abstract quiz strategy
│   │   ├── quiz_context.py                   # Strategy pattern context
│   │   └── strategies/
│   │       ├── flashcard_quiz_strategy.py    # Sequential quiz implementation
│   │       ├── random_quiz_strategy.py       # Random quiz implementation
│   │       └── adaptive_quiz_strategy.py     # Adaptive quiz implementation
│   └── ui/
│       ├── cli_interface.py                  # Command-line interface
│       └── menu_system.py                    # Menu handling and strategy selection
├── sample_flashcards.json                    # Example flashcard data (array format)
└── sample_flashcards_object_format.json     # Example flashcard data (object format)
```

## Extensibility

The architecture supports easy extension:

- **New Quiz Strategies**: Implement `QuizStrategy` interface
- **Data Formats**: Extend `JSONLoader` for CSV, XML, etc.
- **UI Interfaces**: Replace `CLIInterface` for GUI or web interfaces
- **Report Formats**: Customize summary display in `CLIInterface`