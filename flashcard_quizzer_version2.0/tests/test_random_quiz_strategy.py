"""
Comprehensive test suite for RandomQuizStrategy class.
Tests randomized flashcard quiz functionality with pytest framework.
"""

import pytest
import random
from unittest.mock import Mock, MagicMock, patch, call
from typing import List

from src.quiz.strategies.random_quiz_strategy import RandomQuizStrategy
from src.models.flashcard import Flashcard


class TestRandomQuizStrategyFixtures:
    """Test fixtures for RandomQuizStrategy testing."""
    
    @pytest.fixture
    def random_quiz_strategy(self):
        """Create a RandomQuizStrategy instance for testing."""
        return RandomQuizStrategy()
    
    @pytest.fixture
    def mock_cli_interface(self):
        """Create a mock CLI interface for testing."""
        cli_mock = Mock()
        cli_mock.display_message = Mock()
        cli_mock.display_card_front = Mock()
        cli_mock.get_user_input = Mock()
        cli_mock.display_correct_feedback = Mock()
        cli_mock.display_incorrect_feedback = Mock()
        cli_mock.display_separator = Mock()
        cli_mock.display_quiz_summary = Mock()
        return cli_mock
    
    @pytest.fixture
    def normal_flashcards(self):
        """Create normal flashcard objects for testing."""
        return [
            Flashcard(front="What is 2 + 2?", back="4"),
            Flashcard(front="What is the capital of France?", back="Paris"),
            Flashcard(front="What is 5 * 3?", back="15"),
            Flashcard(front="What color is the sky?", back="Blue"),
            Flashcard(front="How many days in a week?", back="7")
        ]
    
    @pytest.fixture
    def unicode_flashcards(self):
        """Create flashcards with unicode content for testing."""
        return [
            Flashcard(front="What is 你好 in English?", back="Hello"),
            Flashcard(front="What does 🌟 represent?", back="Star"),
            Flashcard(front="Translate 'Hola'", back="Hello")
        ]
    
    @pytest.fixture
    def large_content_flashcards(self):
        """Create flashcards with large content for stress testing."""
        large_front = "A" * 5000
        large_back = "B" * 5000
        return [
            Flashcard(front=large_front, back=large_back),
            Flashcard(front="Normal question", back="Normal answer")
        ]
    
    @pytest.fixture
    def single_flashcard(self):
        """Create a single flashcard for boundary testing."""
        return [Flashcard(front="Single question", back="Single answer")]
    
    @pytest.fixture
    def empty_flashcards(self):
        """Create empty flashcard list for edge case testing."""
        return []


class TestRandomQuizStrategyHappyPath:
    """Happy path test scenarios for normal card processing."""
    
    def test_execute_quiz_with_normal_flashcards_shuffles_and_processes_correctly(
        self, random_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that normal flashcards are shuffled and processed correctly."""
        mock_cli_interface.get_user_input.side_effect = ["4", "Paris", "15", "Blue", "7"]
        
        with patch('random.shuffle') as mock_shuffle:
            result = random_quiz_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Verify random.shuffle was called
        mock_shuffle.assert_called_once()
        
        # Verify basic quiz flow
        mock_cli_interface.display_message.assert_called_once_with(
            "Starting random quiz with 5 flashcards.\n"
        )
        assert mock_cli_interface.display_card_front.call_count == 5
        assert mock_cli_interface.get_user_input.call_count == 5
        assert mock_cli_interface.display_correct_feedback.call_count == 5
        assert mock_cli_interface.display_separator.call_count == 5
        
        # All answers correct, so no missed cards
        assert result == []
    
    def test_execute_quiz_preserves_original_flashcard_order(
        self, random_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that original flashcard list order is preserved."""
        original_order = [card.front for card in normal_flashcards]
        mock_cli_interface.get_user_input.side_effect = ["4", "Paris", "15", "Blue", "7"]
        
        random_quiz_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Original list should be unchanged
        after_quiz_order = [card.front for card in normal_flashcards]
        assert original_order == after_quiz_order
    
    def test_execute_quiz_with_all_correct_answers_returns_empty_missed_list(
        self, random_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that perfect performance results in no missed cards."""
        mock_cli_interface.get_user_input.side_effect = ["4", "Paris", "15", "Blue", "7"]
        
        result = random_quiz_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        
        assert result == []
        assert mock_cli_interface.display_correct_feedback.call_count == 5
        assert mock_cli_interface.display_incorrect_feedback.call_count == 0
    
    def test_execute_quiz_with_mixed_answers_returns_correct_missed_cards(
        self, random_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that mixed answers correctly track missed cards."""
        # Provide wrong answers for 2nd and 4th cards
        mock_cli_interface.get_user_input.side_effect = ["4", "Wrong", "15", "Wrong", "7"]
        
        with patch('random.shuffle') as mock_shuffle:
            # Control shuffle to maintain predictable order
            mock_shuffle.side_effect = lambda x: None  # No shuffling
            result = random_quiz_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Should have 2 missed cards (2nd and 4th from original list)
        assert len(result) == 2
        assert result[0].front == "What is the capital of France?"
        assert result[1].front == "What color is the sky?"
        
        assert mock_cli_interface.display_correct_feedback.call_count == 3
        assert mock_cli_interface.display_incorrect_feedback.call_count == 2
    
    def test_execute_quiz_calculates_accuracy_percentage_correctly(
        self, random_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that accuracy percentage is calculated correctly."""
        # 3 correct, 2 incorrect = 60%
        mock_cli_interface.get_user_input.side_effect = ["4", "Wrong", "15", "Wrong", "7"]
        
        with patch('random.shuffle') as mock_shuffle:
            mock_shuffle.side_effect = lambda x: None  # No shuffling
            random_quiz_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Verify summary was called with correct percentage
        mock_cli_interface.display_quiz_summary.assert_called_once()
        call_args = mock_cli_interface.display_quiz_summary.call_args
        assert call_args[1]['accuracy_percentage'] == 60.0
        assert call_args[1]['correct_answers'] == 3
        assert call_args[1]['total_cards'] == 5
    
    def test_execute_quiz_displays_correct_card_index_and_total(
        self, random_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that card indices are displayed correctly during quiz."""
        mock_cli_interface.get_user_input.side_effect = ["4", "Paris", "15", "Blue", "7"]
        
        with patch('random.shuffle') as mock_shuffle:
            mock_shuffle.side_effect = lambda x: None  # No shuffling for predictable testing
            random_quiz_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Verify display_card_front called with correct indices
        expected_calls = []
        for i, card in enumerate(normal_flashcards, 1):
            expected_calls.append(call(card.front, i, 5))
        
        mock_cli_interface.display_card_front.assert_has_calls(expected_calls)
    
    def test_display_quiz_summary_called_with_correct_parameters(
        self, random_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that quiz summary is called with correct parameters."""
        mock_cli_interface.get_user_input.side_effect = ["4", "Paris", "15", "Blue", "7"]
        
        random_quiz_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        
        mock_cli_interface.display_quiz_summary.assert_called_once_with(
            strategy_name="Random Quiz",
            correct_answers=5,
            total_cards=5,
            accuracy_percentage=100.0,
            missed_cards=[]
        )


class TestRandomQuizStrategyErrorConditions:
    """Error condition test scenarios for incorrect and malformed responses."""
    
    def test_execute_quiz_with_cli_interface_get_user_input_raises_exception_propagates_error(
        self, random_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that CLI interface exceptions are properly propagated."""
        mock_cli_interface.get_user_input.side_effect = RuntimeError("Input error")
        
        with pytest.raises(RuntimeError, match="Input error"):
            random_quiz_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
    
    def test_execute_quiz_with_cli_interface_display_methods_raise_exception_propagates_error(
        self, random_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that CLI display method exceptions are properly propagated."""
        mock_cli_interface.display_card_front.side_effect = RuntimeError("Display error")
        
        with pytest.raises(RuntimeError, match="Display error"):
            random_quiz_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
    
    def test_execute_quiz_with_flashcard_matches_answer_raises_exception_propagates_error(
        self, random_quiz_strategy, mock_cli_interface
    ):
        """Test that flashcard method exceptions are properly propagated."""
        mock_flashcard = Mock()
        mock_flashcard.front = "Test question"
        mock_flashcard.matches_answer.side_effect = ValueError("Matching error")
        
        mock_cli_interface.get_user_input.return_value = "test answer"
        
        with pytest.raises(ValueError, match="Matching error"):
            random_quiz_strategy.execute_quiz([mock_flashcard], mock_cli_interface)
    
    def test_execute_quiz_with_empty_user_input_handles_correctly(
        self, random_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that empty user input is handled correctly."""
        mock_cli_interface.get_user_input.side_effect = ["", "", "", "", ""]
        
        result = random_quiz_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # All empty answers should be marked as missed
        assert len(result) == 5
        assert mock_cli_interface.display_incorrect_feedback.call_count == 5
        assert mock_cli_interface.display_correct_feedback.call_count == 0
    
    def test_execute_quiz_with_very_long_user_input_handles_correctly(
        self, random_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that very long user input is handled correctly."""
        long_answer = "A" * 10000
        mock_cli_interface.get_user_input.side_effect = [long_answer] * 5
        
        result = random_quiz_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Very long answers should be processed (likely marked as incorrect)
        assert len(result) == 5
        mock_cli_interface.display_quiz_summary.assert_called_once()
    
    def test_execute_quiz_with_unicode_user_input_handles_correctly(
        self, random_quiz_strategy, unicode_flashcards, mock_cli_interface
    ):
        """Test that unicode user input is handled correctly."""
        mock_cli_interface.get_user_input.side_effect = ["Hello", "Star", "Hello"]
        
        result = random_quiz_strategy.execute_quiz(unicode_flashcards, mock_cli_interface)
        
        # Should complete without errors
        mock_cli_interface.display_quiz_summary.assert_called_once()
        assert isinstance(result, list)
    
    def test_execute_quiz_with_special_characters_in_user_input_handles_correctly(
        self, random_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that special characters in user input are handled correctly."""
        special_chars = ["!@#$%", "^&*()", "{}[]", "<>?/", "\\|\"'"]
        mock_cli_interface.get_user_input.side_effect = special_chars
        
        result = random_quiz_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Should complete without errors
        mock_cli_interface.display_quiz_summary.assert_called_once()
        assert isinstance(result, list)


class TestRandomQuizStrategyEdgeCases:
    """Edge case test scenarios for boundary conditions and special situations."""
    
    def test_execute_quiz_with_empty_flashcard_list_handles_gracefully(
        self, random_quiz_strategy, empty_flashcards, mock_cli_interface
    ):
        """Test that empty flashcard list is handled gracefully."""
        result = random_quiz_strategy.execute_quiz(empty_flashcards, mock_cli_interface)
        
        mock_cli_interface.display_message.assert_called_once_with(
            "Starting random quiz with 0 flashcards.\n"
        )
        
        # Should display summary with 0% accuracy (handled via 0/0 = 0)
        mock_cli_interface.display_quiz_summary.assert_called_once()
        call_args = mock_cli_interface.display_quiz_summary.call_args
        assert call_args[1]['total_cards'] == 0
        assert call_args[1]['correct_answers'] == 0
        
        assert result == []
        assert mock_cli_interface.display_card_front.call_count == 0
        assert mock_cli_interface.get_user_input.call_count == 0
    
    def test_execute_quiz_with_single_flashcard_works_correctly(
        self, random_quiz_strategy, single_flashcard, mock_cli_interface
    ):
        """Test that single flashcard quiz works correctly."""
        mock_cli_interface.get_user_input.return_value = "Single answer"
        
        result = random_quiz_strategy.execute_quiz(single_flashcard, mock_cli_interface)
        
        mock_cli_interface.display_message.assert_called_once_with(
            "Starting random quiz with 1 flashcards.\n"
        )
        mock_cli_interface.display_card_front.assert_called_once_with(
            "Single question", 1, 1
        )
        mock_cli_interface.get_user_input.assert_called_once()
        mock_cli_interface.display_quiz_summary.assert_called_once()
    
    def test_execute_quiz_with_duplicate_flashcards_handles_correctly(
        self, random_quiz_strategy, mock_cli_interface
    ):
        """Test that duplicate flashcards are handled correctly."""
        duplicate_card = Flashcard(front="Same question", back="Same answer")
        duplicate_flashcards = [duplicate_card, duplicate_card, duplicate_card]
        
        mock_cli_interface.get_user_input.side_effect = ["Wrong", "Same answer", "Wrong"]
        
        with patch('random.shuffle') as mock_shuffle:
            mock_shuffle.side_effect = lambda x: None  # No shuffling
            result = random_quiz_strategy.execute_quiz(duplicate_flashcards, mock_cli_interface)
        
        # Should have 2 missed cards (duplicates of the same card)
        assert len(result) == 2
        assert all(card.front == "Same question" for card in result)
        
        mock_cli_interface.display_quiz_summary.assert_called_once()
    
    def test_execute_quiz_with_very_large_flashcard_content_handles_correctly(
        self, random_quiz_strategy, large_content_flashcards, mock_cli_interface
    ):
        """Test that large flashcard content is handled correctly."""
        mock_cli_interface.get_user_input.side_effect = ["Answer1", "Normal answer"]
        
        result = random_quiz_strategy.execute_quiz(large_content_flashcards, mock_cli_interface)
        
        # Should complete without errors
        assert mock_cli_interface.display_card_front.call_count == 2
        mock_cli_interface.display_quiz_summary.assert_called_once()
        assert isinstance(result, list)
    
    def test_execute_quiz_accuracy_calculation_with_zero_cards_handles_division_by_zero(
        self, random_quiz_strategy, empty_flashcards, mock_cli_interface
    ):
        """Test that accuracy calculation doesn't crash with zero cards."""
        result = random_quiz_strategy.execute_quiz(empty_flashcards, mock_cli_interface)
        
        # Should handle 0/0 gracefully (likely result in 0% accuracy)
        mock_cli_interface.display_quiz_summary.assert_called_once()
        call_args = mock_cli_interface.display_quiz_summary.call_args
        
        # The implementation may handle 0/0 differently, but it shouldn't crash
        assert call_args[1]['total_cards'] == 0
        assert call_args[1]['correct_answers'] == 0
        assert result == []
    
    def test_execute_quiz_with_whitespace_only_user_input_handles_correctly(
        self, random_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that whitespace-only input is handled correctly."""
        whitespace_answers = ["   ", "\t\t", "\n\n", "  \t  ", "    "]
        mock_cli_interface.get_user_input.side_effect = whitespace_answers
        
        result = random_quiz_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Whitespace answers should be processed by flashcard logic
        mock_cli_interface.display_quiz_summary.assert_called_once()
        assert isinstance(result, list)
    
    def test_execute_quiz_randomization_produces_different_orders(
        self, random_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that randomization actually produces different card orders."""
        mock_cli_interface.get_user_input.side_effect = ["4", "Paris", "15", "Blue", "7"]
        
        # Capture the order of cards displayed in multiple runs
        displayed_orders = []
        
        for _ in range(10):  # Run quiz 10 times
            mock_cli_interface.reset_mock()
            mock_cli_interface.get_user_input.side_effect = ["4", "Paris", "15", "Blue", "7"]
            
            random_quiz_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
            
            # Extract the order of displayed cards
            calls = mock_cli_interface.display_card_front.call_args_list
            order = [call[0][0] for call in calls]  # First argument is the front text
            displayed_orders.append(tuple(order))
        
        # With true randomization, we should get at least some different orders
        # (Though this is probabilistic, so we allow for some identical orders)
        unique_orders = set(displayed_orders)
        assert len(unique_orders) > 1, "Randomization should produce different orders"
    
    def test_execute_quiz_with_very_large_card_set_handles_correctly(
        self, random_quiz_strategy, mock_cli_interface
    ):
        """Test that very large card sets are processed efficiently."""
        large_card_set = []
        for i in range(100):
            large_card_set.append(Flashcard(front=f"Question {i}", back=f"Answer {i}"))
        
        mock_cli_interface.get_user_input.side_effect = [f"Answer {i}" for i in range(100)]
        
        import time
        start_time = time.time()
        
        result = random_quiz_strategy.execute_quiz(large_card_set, mock_cli_interface)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete within reasonable time (less than 2 seconds)
        assert execution_time < 2.0
        assert len(result) == 0  # All answers correct
        assert mock_cli_interface.display_card_front.call_count == 100
        mock_cli_interface.display_quiz_summary.assert_called_once()


class TestRandomQuizStrategyMocking:
    """Test scenarios using mocks to verify internal behavior and dependencies."""
    
    def test_execute_quiz_calls_random_shuffle_exactly_once(
        self, random_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that random.shuffle is called exactly once per quiz."""
        mock_cli_interface.get_user_input.side_effect = ["4", "Paris", "15", "Blue", "7"]
        
        with patch('random.shuffle') as mock_shuffle:
            random_quiz_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
            
            # Verify shuffle was called exactly once
            mock_shuffle.assert_called_once()
            # Verify it was called with a copy of flashcards
            shuffled_list = mock_shuffle.call_args[0][0]
            assert len(shuffled_list) == len(normal_flashcards)
            assert all(isinstance(card, Flashcard) for card in shuffled_list)
    
    def test_execute_quiz_calls_each_flashcard_matches_answer_exactly_once(
        self, random_quiz_strategy, mock_cli_interface
    ):
        """Test that each flashcard's matches_answer is called exactly once."""
        mock_flashcards = []
        for i in range(3):
            mock_card = Mock()
            mock_card.front = f"Question {i}"
            mock_card.back = f"Answer {i}"
            mock_card.matches_answer.return_value = True
            mock_flashcards.append(mock_card)
        
        mock_cli_interface.get_user_input.side_effect = ["ans1", "ans2", "ans3"]
        
        with patch('random.shuffle') as mock_shuffle:
            mock_shuffle.side_effect = lambda x: None  # No actual shuffling
            random_quiz_strategy.execute_quiz(mock_flashcards, mock_cli_interface)
        
        # Verify each flashcard's matches_answer was called exactly once
        for i, mock_card in enumerate(mock_flashcards):
            mock_card.matches_answer.assert_called_once_with(f"ans{i+1}")
    
    def test_execute_quiz_calls_all_required_cli_interface_methods(
        self, random_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that all required CLI interface methods are called."""
        mock_cli_interface.get_user_input.side_effect = ["4", "Paris", "15", "Blue", "7"]
        
        random_quiz_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Verify all CLI methods were called
        mock_cli_interface.display_message.assert_called()
        mock_cli_interface.display_card_front.assert_called()
        mock_cli_interface.get_user_input.assert_called()
        mock_cli_interface.display_correct_feedback.assert_called()
        mock_cli_interface.display_separator.assert_called()
        mock_cli_interface.display_quiz_summary.assert_called()
        
        # Verify call counts match number of cards
        assert mock_cli_interface.display_card_front.call_count == 5
        assert mock_cli_interface.get_user_input.call_count == 5
        assert mock_cli_interface.display_separator.call_count == 5
    
    def test_display_quiz_summary_receives_correct_missed_cards_list(
        self, random_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that summary receives the correct missed cards list."""
        # Make 2nd and 4th cards incorrect
        mock_cli_interface.get_user_input.side_effect = ["4", "Wrong", "15", "Wrong", "7"]
        
        with patch('random.shuffle') as mock_shuffle:
            mock_shuffle.side_effect = lambda x: None  # No shuffling for predictable results
            result = random_quiz_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Verify the missed cards list passed to summary matches what was returned
        call_args = mock_cli_interface.display_quiz_summary.call_args
        summary_missed_cards = call_args[1]['missed_cards']
        
        assert summary_missed_cards == result
        assert len(summary_missed_cards) == 2
        assert summary_missed_cards[0].front == "What is the capital of France?"
        assert summary_missed_cards[1].front == "What color is the sky?"


class TestRandomQuizStrategyIntegration:
    """Integration test scenarios testing strategy with realistic workflows."""
    
    def test_random_quiz_complete_workflow_with_realistic_scenario(
        self, random_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test complete random quiz workflow with realistic user interaction."""
        # Simulate realistic user responses (70% accuracy)
        user_responses = ["4", "Wrong", "15", "Blue", "Wrong"]
        mock_cli_interface.get_user_input.side_effect = user_responses
        
        result = random_quiz_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Verify complete workflow
        mock_cli_interface.display_message.assert_called_once()
        assert mock_cli_interface.display_card_front.call_count == 5
        assert mock_cli_interface.get_user_input.call_count == 5
        assert mock_cli_interface.display_correct_feedback.call_count == 3
        assert mock_cli_interface.display_incorrect_feedback.call_count == 2
        assert mock_cli_interface.display_separator.call_count == 5
        
        # Verify summary with 60% accuracy
        call_args = mock_cli_interface.display_quiz_summary.call_args
        assert call_args[1]['strategy_name'] == "Random Quiz"
        assert call_args[1]['correct_answers'] == 3
        assert call_args[1]['total_cards'] == 5
        assert call_args[1]['accuracy_percentage'] == 60.0
        assert len(result) == 2
    
    def test_random_quiz_performance_with_realistic_dataset(
        self, random_quiz_strategy, mock_cli_interface
    ):
        """Test performance with realistic flashcard deck size."""
        # Create realistic deck size (50 cards)
        realistic_deck = []
        for i in range(50):
            realistic_deck.append(
                Flashcard(front=f"Question {i+1}: What is {i*2}+1?", back=str(i*2+1))
            )
        
        # Simulate 70% accuracy
        correct_answers = ["1", "3", "5", "7", "9"] * 7  # 35 correct
        wrong_answers = ["Wrong"] * 15  # 15 incorrect
        all_answers = correct_answers + wrong_answers
        mock_cli_interface.get_user_input.side_effect = all_answers
        
        import time
        start_time = time.time()
        
        result = random_quiz_strategy.execute_quiz(realistic_deck, mock_cli_interface)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Verify performance and results
        assert execution_time < 2.0  # Should complete within 2 seconds
        assert len(result) == 15  # 15 missed cards
        
        call_args = mock_cli_interface.display_quiz_summary.call_args
        assert call_args[1]['total_cards'] == 50
        assert call_args[1]['correct_answers'] == 35
        assert call_args[1]['accuracy_percentage'] == 70.0
    
    def test_random_quiz_with_different_flashcard_types_integration(
        self, random_quiz_strategy, mock_cli_interface
    ):
        """Test integration with different types of flashcard content."""
        mixed_flashcards = [
            Flashcard(front="Simple", back="Easy"),
            Flashcard(front="Unicode: 你好", back="Hello"),
            Flashcard(front="Math: 2+2=?", back="4"),
            Flashcard(front="Long question with lots of text content", back="Short"),
            Flashcard(front="Special !@#$%", back="Symbols")
        ]
        
        mock_cli_interface.get_user_input.side_effect = [
            "Easy", "Hello", "4", "Short", "Symbols"
        ]
        
        result = random_quiz_strategy.execute_quiz(mixed_flashcards, mock_cli_interface)
        
        # All different types should be processed correctly
        assert result == []  # All correct
        mock_cli_interface.display_quiz_summary.assert_called_once()
        
        call_args = mock_cli_interface.display_quiz_summary.call_args
        assert call_args[1]['accuracy_percentage'] == 100.0
        assert call_args[1]['total_cards'] == 5