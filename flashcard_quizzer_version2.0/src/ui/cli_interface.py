"""
Command-line interface for user interaction.
Follows Single Responsibility Principle for UI concerns.
"""

import sys
from typing import List, Optional


class CLIInterface:
    """
    Handles all command-line user interaction and display.
    
    Separates UI concerns from business logic, making the application
    easier to test and potentially adapt to different interfaces.
    """
    
    def display_message(self, message: str) -> None:
        """
        Display a general message to the user.
        
        Args:
            message: Message to display
        """
        print(message)
    
    def display_error(self, error_message: str) -> None:
        """
        Display an error message to stderr.
        
        Args:
            error_message: Error message to display
        """
        print(f"Error: {error_message}", file=sys.stderr)
    
    def display_card_front(self, front_text: str, card_number: int, 
                         total_cards: int, phase_name: str = "") -> None:
        """
        Display the front of a flashcard with progress information.
        
        Args:
            front_text: Text on the front of the flashcard
            card_number: Current card number (1-indexed)
            total_cards: Total number of cards in the quiz
            phase_name: Optional name of the current quiz phase
        """
        phase_prefix = f"[{phase_name}] " if phase_name else ""
        print(f"{phase_prefix}Card {card_number}/{total_cards}: {front_text}")
    
    def get_user_input(self, prompt: str = "Your answer: ") -> str:
        """
        Get input from the user.
        
        Args:
            prompt: Prompt to display to the user
            
        Returns:
            User's input as a string
        """
        try:
            return input(prompt).strip()
        except EOFError:
            # Handle Ctrl+D gracefully
            print("\nQuiz terminated by user.")
            sys.exit(0)
    
    def display_correct_feedback(self) -> None:
        """Display positive feedback for correct answers."""
        print("Correct")
    
    def display_incorrect_feedback(self, correct_answer: str) -> None:
        """
        Display feedback for incorrect answers with the correct answer.
        
        Args:
            correct_answer: The correct answer to display
        """
        print(f"Incorrect (correct answer: {correct_answer})")
    
    def display_separator(self) -> None:
        """Display a separator between cards for better readability."""
        print("-" * 40)
    
    def display_quiz_summary(self, strategy_name: str, correct_answers: int, 
                           total_cards: int, accuracy_percentage: float, 
                           missed_cards: List) -> None:
        """
        Display comprehensive quiz summary with missed cards.
        
        Args:
            strategy_name: Name of the quiz strategy used
            correct_answers: Number of correct answers
            total_cards: Total number of cards attempted
            accuracy_percentage: Percentage accuracy
            missed_cards: List of flashcards that were answered incorrectly
        """
        print("\n" + "="*50)
        print(f"{strategy_name.upper()} RESULTS")
        print("="*50)
        print(f"Total Questions: {total_cards}")
        print(f"Correct Answers: {correct_answers}")
        print(f"Incorrect Answers: {total_cards - correct_answers}")
        print(f"Accuracy: {accuracy_percentage:.1f}%")
        
        if missed_cards:
            print(f"\nTerms you missed ({len(missed_cards)}):")
            print("-" * 30)
            for i, card in enumerate(missed_cards, 1):
                print(f"{i}. {card.front} → {card.back}")
        else:
            print("\nPerfect score! No missed terms.")
        
        print("="*50)