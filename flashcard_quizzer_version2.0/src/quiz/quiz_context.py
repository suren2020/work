"""
Quiz context class implementing Strategy pattern.
Manages the current quiz strategy and delegates execution.
"""

from typing import List

from .quiz_strategy import QuizStrategy
from ..models.flashcard import Flashcard


class QuizContext:
    """
    Context class for the Strategy pattern.
    
    Manages the current quiz strategy and provides a unified
    interface for executing quizzes regardless of the specific algorithm.
    """
    
    def __init__(self, strategy: QuizStrategy):
        """
        Initialize the quiz context with a strategy.
        
        Args:
            strategy: The quiz strategy to use
        """
        self._strategy = strategy
    
    def set_strategy(self, strategy: QuizStrategy) -> None:
        """
        Change the quiz strategy at runtime.
        
        Args:
            strategy: New quiz strategy to use
        """
        self._strategy = strategy
    
    def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
        """
        Execute the quiz using the current strategy.
        
        Args:
            flashcards: List of flashcard objects to quiz on
            cli_interface: Interface for user interaction and display
            
        Returns:
            List of flashcards that were answered incorrectly
        """
        return self._strategy.execute_quiz(flashcards, cli_interface)