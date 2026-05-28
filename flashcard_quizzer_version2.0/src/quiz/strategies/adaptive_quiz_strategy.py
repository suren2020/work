"""
Adaptive quiz strategy implementation.
Implements the Strategy pattern for adaptive flashcard quizzing focusing on missed cards.
"""

from typing import List

from ..quiz_strategy import QuizStrategy
from ...models.flashcard import Flashcard


class AdaptiveQuizStrategy(QuizStrategy):
    """
    Adaptive flashcard quiz implementation.
    
    First reviews previously missed cards, then goes through all cards.
    Continuously tracks and prioritizes cards that need more practice.
    """
    
    def __init__(self):
        """Initialize adaptive quiz strategy with empty missed cards list."""
        self.initial_missed_cards = []
    
    def set_initial_missed_cards(self, missed_cards: List[Flashcard]) -> None:
        """
        Set the initial list of missed cards for adaptive review.
        
        Args:
            missed_cards: List of cards that were previously answered incorrectly
        """
        self.initial_missed_cards = missed_cards
    
    def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
        """
        Execute the adaptive flashcard quiz.
        Reviews missed cards first, then all cards, tracking new misses.
        
        Args:
            flashcards: List of flashcard objects to quiz on
            cli_interface: Interface for user interaction and display
            
        Returns:
            List of flashcards that were answered incorrectly
        """
        total_correct = 0
        total_attempted = 0
        current_missed_cards = []
        
        # Phase 1: Review previously missed cards if any exist
        if self.initial_missed_cards:
            cli_interface.display_message(
                f"Adaptive Quiz - Reviewing {len(self.initial_missed_cards)} "
                f"previously missed cards first.\n"
            )
            
            correct, attempted = self._quiz_card_set(
                self.initial_missed_cards, 
                cli_interface, 
                current_missed_cards,
                "Review Phase"
            )
            total_correct += correct
            total_attempted += attempted
            
            cli_interface.display_message("\nReview phase completed. Starting full quiz...\n")
        else:
            cli_interface.display_message("Adaptive Quiz - No previous missed cards. Starting full quiz.\n")
        
        # Phase 2: Quiz on all cards
        correct, attempted = self._quiz_card_set(
            flashcards, 
            cli_interface, 
            current_missed_cards,
            "Main Quiz"
        )
        total_correct += correct
        total_attempted += attempted
        
        self._display_quiz_summary(
            cli_interface, 
            total_correct, 
            total_attempted, 
            current_missed_cards
        )
        
        return current_missed_cards
    
    def _quiz_card_set(self, cards: List[Flashcard], cli_interface, 
                      missed_cards: List[Flashcard], phase_name: str) -> tuple:
        """
        Quiz on a specific set of cards and track results.
        
        Args:
            cards: List of flashcards to quiz on
            cli_interface: Interface for user interaction
            missed_cards: List to append missed cards to
            phase_name: Name of the current quiz phase
            
        Returns:
            Tuple of (correct_answers, total_attempted)
        """
        correct_answers = 0
        total_cards = len(cards)
        
        for index, flashcard in enumerate(cards, 1):
            cli_interface.display_card_front(
                flashcard.front, 
                index, 
                total_cards, 
                phase_name
            )
            
            user_answer = cli_interface.get_user_input()
            
            if flashcard.matches_answer(user_answer):
                cli_interface.display_correct_feedback()
                correct_answers += 1
            else:
                cli_interface.display_incorrect_feedback(flashcard.back)
                # Only add to missed cards if not already present
                if flashcard not in missed_cards:
                    missed_cards.append(flashcard)
            
            cli_interface.display_separator()
        
        return correct_answers, total_cards
    
    def _display_quiz_summary(self, cli_interface, correct_answers: int, 
                            total_cards: int, missed_cards: List[Flashcard]) -> None:
        """
        Display comprehensive adaptive quiz results summary.
        
        Args:
            cli_interface: Interface for displaying results
            correct_answers: Total number of correct answers across all phases
            total_cards: Total number of cards attempted
            missed_cards: List of incorrectly answered flashcards
        """
        percentage = (correct_answers / total_cards) * 100 if total_cards > 0 else 0
        
        cli_interface.display_quiz_summary(
            strategy_name="Adaptive Quiz",
            correct_answers=correct_answers,
            total_cards=total_cards,
            accuracy_percentage=percentage,
            missed_cards=missed_cards
        )