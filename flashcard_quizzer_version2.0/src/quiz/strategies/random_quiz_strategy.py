"""
Random quiz strategy implementation.
Implements the Strategy pattern for randomized flashcard quizzing.
"""

import random
from typing import List

from ..quiz_strategy import QuizStrategy
from ...models.flashcard import Flashcard


class RandomQuizStrategy(QuizStrategy):
    """
    Randomized flashcard quiz implementation.
    
    Shuffles flashcards and presents them in random order,
    providing immediate feedback on correctness and tracking missed cards.
    """
    
    def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
        """
        Execute the random flashcard quiz by shuffling and iterating through all cards.
        
        Args:
            flashcards: List of flashcard objects to quiz on
            cli_interface: Interface for user interaction and display
            
        Returns:
            List of flashcards that were answered incorrectly
        """
        # Create a shuffled copy of flashcards to preserve original order
        shuffled_cards = flashcards.copy()
        random.shuffle(shuffled_cards)
        
        total_cards = len(shuffled_cards)
        correct_answers = 0
        missed_cards = []
        
        cli_interface.display_message(f"Starting random quiz with {total_cards} flashcards.\n")
        
        for index, flashcard in enumerate(shuffled_cards, 1):
            cli_interface.display_card_front(flashcard.front, index, total_cards)
            
            user_answer = cli_interface.get_user_input()
            
            if flashcard.matches_answer(user_answer):
                cli_interface.display_correct_feedback()
                correct_answers += 1
            else:
                cli_interface.display_incorrect_feedback(flashcard.back)
                missed_cards.append(flashcard)
            
            cli_interface.display_separator()
        
        self._display_quiz_summary(cli_interface, correct_answers, total_cards, missed_cards)
        return missed_cards
    
    def _display_quiz_summary(self, cli_interface, correct_answers: int, 
                            total_cards: int, missed_cards: List[Flashcard]) -> None:
        """
        Display comprehensive quiz results summary.
        
        Args:
            cli_interface: Interface for displaying results
            correct_answers: Number of correct answers
            total_cards: Total number of cards in quiz
            missed_cards: List of incorrectly answered flashcards
        """
        percentage = (correct_answers / total_cards) * 100
        
        cli_interface.display_quiz_summary(
            strategy_name="Random Quiz",
            correct_answers=correct_answers,
            total_cards=total_cards,
            accuracy_percentage=percentage,
            missed_cards=missed_cards
        )