"""
Menu system for strategy selection.
Follows Single Responsibility Principle for menu handling.
"""

from typing import List

from ..models.flashcard import Flashcard
from ..quiz.quiz_context import QuizContext
from ..quiz.strategies.flashcard_quiz_strategy import FlashcardQuizStrategy
from ..quiz.strategies.random_quiz_strategy import RandomQuizStrategy
from ..quiz.strategies.adaptive_quiz_strategy import AdaptiveQuizStrategy
from .cli_interface import CLIInterface


class MenuSystem:
    """
    Handles menu display and strategy selection.
    Orchestrates the quiz flow based on user menu choices.
    """
    
    def __init__(self, cli_interface: CLIInterface):
        """
        Initialize the menu system with CLI interface.
        
        Args:
            cli_interface: Interface for user interaction
        """
        self.cli_interface = cli_interface
        self.quiz_context = QuizContext(FlashcardQuizStrategy())
        self.missed_cards = []
    
    def run_quiz_menu(self, flashcards: List[Flashcard]) -> None:
        """
        Display menu and execute selected quiz strategies.
        
        Args:
            flashcards: List of flashcard objects for quizzing
        """
        while True:
            self._display_menu()
            choice = self._get_menu_choice()
            
            if choice == '1':
                self._run_sequential_quiz(flashcards)
            elif choice == '2':
                self._run_random_quiz(flashcards)
            elif choice == '3':
                self._run_adaptive_quiz(flashcards)
            elif choice == '4':
                self.cli_interface.display_message("Goodbye!")
                break
            else:
                self.cli_interface.display_error("Invalid choice. Please try again.")
    
    def _display_menu(self) -> None:
        """Display the main menu options."""
        self.cli_interface.display_message("\n" + "="*40)
        self.cli_interface.display_message("FLASHCARD QUIZ MENU")
        self.cli_interface.display_message("="*40)
        self.cli_interface.display_message("1. Sequential")
        self.cli_interface.display_message("2. Random") 
        self.cli_interface.display_message("3. Adaptive")
        self.cli_interface.display_message("4. Exit")
        self.cli_interface.display_message("="*40)
    
    def _get_menu_choice(self) -> str:
        """
        Get and validate user menu choice.
        
        Returns:
            User's menu choice as string
        """
        return self.cli_interface.get_user_input("Enter your choice (1-4): ")
    
    def _run_sequential_quiz(self, flashcards: List[Flashcard]) -> None:
        """
        Run sequential quiz strategy.
        
        Args:
            flashcards: List of flashcards to quiz on
        """
        strategy = FlashcardQuizStrategy()
        self.quiz_context.set_strategy(strategy)
        
        self.cli_interface.display_message("\nStarting Sequential Quiz...")
        missed_cards = self.quiz_context.execute_quiz(flashcards, self.cli_interface)
        
        # Update missed cards for adaptive mode
        if missed_cards:
            self.missed_cards = missed_cards
    
    def _run_random_quiz(self, flashcards: List[Flashcard]) -> None:
        """
        Run random quiz strategy.
        
        Args:
            flashcards: List of flashcards to quiz on
        """
        strategy = RandomQuizStrategy()
        self.quiz_context.set_strategy(strategy)
        
        self.cli_interface.display_message("\nStarting Random Quiz...")
        missed_cards = self.quiz_context.execute_quiz(flashcards, self.cli_interface)
        
        # Update missed cards for adaptive mode
        if missed_cards:
            self.missed_cards = missed_cards
    
    def _run_adaptive_quiz(self, flashcards: List[Flashcard]) -> None:
        """
        Run adaptive quiz strategy.
        
        Args:
            flashcards: List of flashcards to quiz on
        """
        strategy = AdaptiveQuizStrategy()
        self.quiz_context.set_strategy(strategy)
        
        self.cli_interface.display_message("\nStarting Adaptive Quiz...")
        
        # Pass existing missed cards to adaptive strategy
        if hasattr(strategy, 'set_initial_missed_cards'):
            strategy.set_initial_missed_cards(self.missed_cards)
        
        missed_cards = self.quiz_context.execute_quiz(flashcards, self.cli_interface)
        
        # Update missed cards for next round
        if missed_cards:
            self.missed_cards = missed_cards