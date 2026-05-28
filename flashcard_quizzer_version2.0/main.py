#!/usr/bin/env python3
"""
Flashcard Quizzer CLI Application
Entry point with data validation and graceful error handling
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from src.data.json_loader import JSONLoader
from src.quiz.quiz_context import QuizContext
from src.ui.cli_interface import CLIInterface
from src.ui.menu_system import MenuSystem


class FlashcardQuizzerApp:
    """Main application class orchestrating the quiz flow."""
    
    def __init__(self):
        self.json_loader = JSONLoader()
        self.cli_interface = CLIInterface()
        self.menu_system = MenuSystem(self.cli_interface)
        
    def run(self, json_file_path: str) -> None:
        """
        Run the flashcard quiz application.
        
        Args:
            json_file_path: Path to the JSON file containing flashcard data
        """
        try:
            # Data ingestion and validation
            flashcards = self._load_and_validate_data(json_file_path)
            if not flashcards:
                return
            
            # Run the menu-driven quiz system
            self.menu_system.run_quiz_menu(flashcards)
            
        except KeyboardInterrupt:
            self.cli_interface.display_message("\nQuiz interrupted by user.")
            sys.exit(0)
        except Exception as e:
            self.cli_interface.display_error(f"Unexpected error: {e}")
            sys.exit(1)
    
    def _load_and_validate_data(self, json_file_path: str) -> Optional[list]:
        """Load and validate JSON data, handling errors gracefully."""
        try:
            if not Path(json_file_path).exists():
                self.cli_interface.display_error(f"File not found: {json_file_path}")
                sys.exit(1)
            
            flashcards = self.json_loader.load_flashcards(json_file_path)
            self.cli_interface.display_message(f"Successfully loaded {len(flashcards)} flashcards.")
            return flashcards
            
        except Exception as e:
            self.cli_interface.display_error(f"Failed to load flashcards: {e}")
            sys.exit(1)


def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        description="Flashcard Quizzer - CLI application for studying flashcards"
    )
    parser.add_argument(
        '-f', '--file',
        required=True,
        help='Path to JSON file containing flashcard data'
    )
    
    args = parser.parse_args()
    
    app = FlashcardQuizzerApp()
    app.run(args.file)


if __name__ == "__main__":
    main()