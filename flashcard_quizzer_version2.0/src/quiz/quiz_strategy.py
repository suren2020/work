"""
Abstract base class for quiz strategies.
Implements Strategy pattern following Open/Closed Principle.
"""

from abc import ABC, abstractmethod
from typing import List

from ..models.flashcard import Flashcard


class QuizStrategy(ABC):
    """
    Abstract base class defining the interface for quiz strategies.
    
    This allows for different quiz algorithms to be implemented
    without modifying existing code (Open/Closed Principle).
    """
    
    @abstractmethod
    def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
        """
        Execute the quiz using the specific strategy algorithm.
        
        Args:
            flashcards: List of flashcard objects to quiz on
            cli_interface: Interface for user interaction and display
            
        Returns:
            List of flashcards that were answered incorrectly
        """
        pass