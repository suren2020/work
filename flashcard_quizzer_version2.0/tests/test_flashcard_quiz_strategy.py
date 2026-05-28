"""
Comprehensive test suite for FlashcardQuizStrategy class.
Tests happy path scenarios, error conditions, edge cases, and sequential quiz logic.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
import time

from src.quiz.strategies.flashcard_quiz_strategy import FlashcardQuizStrategy
from src.models.flashcard import Flashcard


class TestFlashcardQuizStrategyFixtures:
    """Test fixtures for FlashcardQuizStrategy testing."""
    
    @pytest.fixture
    def flashcard_strategy(self):
        """Create a FlashcardQuizStrategy instance for testing."""
        return FlashcardQuizStrategy()
    
    @pytest.fixture
    def sample_flashcards(self):
        """Create sample flashcards for testing."""
        return [
            Flashcard(front="What is Python?", back="Programming language"),
            Flashcard(front="What is 2+2?", back="4"),
            Flashcard(front="Capital of France?", back="Paris"),
            Flashcard(front="Who created Python?", back="Guido van Rossum")
        ]
    
    @pytest.fixture
    def single_flashcard(self):
        """Create a single flashcard for edge case testing."""
        return [Flashcard(front="Single question", back="Single answer")]
    
    @pytest.fixture
    def large_flashcard_set(self):
        """Create a large set of flashcards for performance testing."""
        return [
            Flashcard(front=f"Question {i}", back=f"Answer {i}")
            for i in range(100)
        ]
    
    @pytest.fixture
    def mock_cli_interface(self):
        """Create a comprehensive mock CLI interface for testing."""
        mock_cli = Mock()
        mock_cli.display_message = Mock()
        mock_cli.display_card_front = Mock()
        mock_cli.get_user_input = Mock()
        mock_cli.display_correct_feedback = Mock()
        mock_cli.display_incorrect_feedback = Mock()
        mock_cli.display_separator = Mock()
        mock_cli.display_quiz_summary = Mock()
        return mock_cli
    
    @pytest.fixture
    def unicode_flashcards(self):
        """Create flashcards with unicode content for testing."""
        return [
            Flashcard(front="What is 你好 in English?", back="Hello"),
            Flashcard(front="Math symbol: ∑", back="Summation"),
            Flashcard(front="Emoji test 🎯", back="Target")
        ]
    
    @pytest.fixture
    def special_character_flashcards(self):
        """Create flashcards with special characters for testing."""
        return [
            Flashcard(front="Special chars: @#$%^&*()", back="Symbols"),
            Flashcard(front="Quote test: \"Hello World\"", back="Quoted text"),
            Flashcard(front="Newline test:\nMultiple lines", back="Multi-line")
        ]


class TestFlashcardQuizStrategyHappyPath(TestFlashcardQuizStrategyFixtures):
    """Happy path test scenarios for normal card processing."""
    
    def test_execute_quiz_with_all_correct_answers_returns_empty_missed_list(
        self, flashcard_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that all correct answers result in empty missed cards list."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = [
            "Programming language", "4", "Paris", "Guido van Rossum"
        ]
        
        # Act
        result = flashcard_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
        
        # Assert
        assert result == []
        assert len(result) == 0
        mock_cli_interface.display_correct_feedback.assert_called()
        assert mock_cli_interface.display_correct_feedback.call_count == 4
        assert mock_cli_interface.display_incorrect_feedback.call_count == 0
    
    def test_execute_quiz_with_mixed_answers_returns_correct_missed_cards(
        self, flashcard_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that mixed correct/incorrect answers properly track missed cards."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = [
            "Wrong answer",      # Miss first card
            "4",                 # Correct second card  
            "Wrong answer",      # Miss third card
            "Guido van Rossum"   # Correct fourth card
        ]
        
        # Act
        result = flashcard_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
        
        # Assert
        assert len(result) == 2  # Two missed cards
        assert result[0] == sample_flashcards[0]  # First card missed
        assert result[1] == sample_flashcards[2]  # Third card missed
        assert mock_cli_interface.display_correct_feedback.call_count == 2
        assert mock_cli_interface.display_incorrect_feedback.call_count == 2
    
    def test_execute_quiz_displays_correct_starting_message(
        self, flashcard_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that correct starting message is displayed."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = ["ans1", "ans2", "ans3", "ans4"]
        
        # Act
        flashcard_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
        
        # Assert
        mock_cli_interface.display_message.assert_called_with(
            "Starting sequential quiz with 4 flashcards.\n"
        )
    
    def test_execute_quiz_presents_cards_in_sequential_order(
        self, flashcard_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that cards are presented in the correct sequential order."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = ["ans1", "ans2", "ans3", "ans4"]
        
        # Act
        flashcard_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
        
        # Assert
        expected_calls = [
            call("What is Python?", 1, 4),
            call("What is 2+2?", 2, 4),
            call("Capital of France?", 3, 4),
            call("Who created Python?", 4, 4)
        ]
        mock_cli_interface.display_card_front.assert_has_calls(expected_calls)
    
    def test_execute_quiz_calls_display_methods_in_correct_sequence(
        self, flashcard_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that UI methods are called in the correct sequence."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = [
            "Programming language", "4", "Paris", "Guido van Rossum"
        ]
        
        # Act
        flashcard_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
        
        # Assert
        # Should display starting message first
        assert mock_cli_interface.display_message.call_count == 1
        # Should display each card front
        assert mock_cli_interface.display_card_front.call_count == 4
        # Should get user input for each card
        assert mock_cli_interface.get_user_input.call_count == 4
        # Should display separator after each card
        assert mock_cli_interface.display_separator.call_count == 4
        # Should display final summary
        mock_cli_interface.display_quiz_summary.assert_called_once()
    
    def test_execute_quiz_with_case_insensitive_answers_works_correctly(
        self, flashcard_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that case-insensitive answer matching works correctly."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = [
            "PROGRAMMING LANGUAGE", "4", "paris", "GUIDO VAN ROSSUM"
        ]
        
        # Act
        result = flashcard_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
        
        # Assert
        assert len(result) == 0  # All should be correct
        assert mock_cli_interface.display_correct_feedback.call_count == 4
    
    def test_execute_quiz_displays_quiz_summary_with_correct_parameters(
        self, flashcard_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that quiz summary is displayed with correct parameters."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = [
            "Programming language", "Wrong", "Paris", "Wrong"
        ]
        
        # Act
        result = flashcard_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
        
        # Assert
        mock_cli_interface.display_quiz_summary.assert_called_once()
        args, kwargs = mock_cli_interface.display_quiz_summary.call_args
        
        assert kwargs['strategy_name'] == "Sequential Quiz"
        assert kwargs['correct_answers'] == 2
        assert kwargs['total_cards'] == 4
        assert kwargs['accuracy_percentage'] == 50.0
        assert len(kwargs['missed_cards']) == 2


class TestFlashcardQuizStrategyErrorConditions(TestFlashcardQuizStrategyFixtures):
    """Error condition test scenarios for incorrect and malformed responses."""
    
    def test_execute_quiz_with_cli_interface_exception_propagates_error(
        self, flashcard_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that exceptions from CLI interface are properly propagated."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = RuntimeError("CLI input error")
        
        # Act & Assert
        with pytest.raises(RuntimeError, match="CLI input error"):
            flashcard_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
    
    def test_execute_quiz_with_display_method_exception_propagates_error(
        self, flashcard_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that exceptions from display methods are properly propagated."""
        # Arrange
        mock_cli_interface.display_card_front.side_effect = RuntimeError("Display error")
        
        # Act & Assert
        with pytest.raises(RuntimeError, match="Display error"):
            flashcard_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
    
    def test_execute_quiz_with_flashcard_exception_propagates_error(
        self, flashcard_strategy, mock_cli_interface
    ):
        """Test that exceptions from flashcard methods are properly propagated."""
        # Arrange
        mock_flashcard = Mock()
        mock_flashcard.front = "Test question"
        mock_flashcard.back = "Test answer"
        mock_flashcard.matches_answer.side_effect = RuntimeError("Flashcard error")
        
        mock_cli_interface.get_user_input.return_value = "Some answer"
        
        # Act & Assert
        with pytest.raises(RuntimeError, match="Flashcard error"):
            flashcard_strategy.execute_quiz([mock_flashcard], mock_cli_interface)
    
    def test_execute_quiz_with_empty_user_input_handles_correctly(
        self, flashcard_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that empty user input is handled correctly as incorrect answer."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = ["", "", "", ""]
        
        # Act
        result = flashcard_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
        
        # Assert
        assert len(result) == 4  # All cards should be missed due to empty answers
        assert mock_cli_interface.display_incorrect_feedback.call_count == 4
        assert mock_cli_interface.display_correct_feedback.call_count == 0
    
    def test_execute_quiz_with_very_long_user_input_handles_correctly(
        self, flashcard_strategy, single_flashcard, mock_cli_interface
    ):
        """Test that very long user input is handled correctly."""
        # Arrange
        very_long_input = "A" * 10000  # Very long input
        mock_cli_interface.get_user_input.return_value = very_long_input
        
        # Act
        result = flashcard_strategy.execute_quiz(single_flashcard, mock_cli_interface)
        
        # Assert
        assert len(result) == 1  # Should be marked as incorrect (doesn't match "Single answer")
        mock_cli_interface.display_incorrect_feedback.assert_called_once_with("Single answer")
    
    def test_execute_quiz_with_whitespace_only_input_handles_correctly(
        self, flashcard_strategy, single_flashcard, mock_cli_interface
    ):
        """Test that whitespace-only input is handled correctly."""
        # Arrange
        mock_cli_interface.get_user_input.return_value = "   \t\n   "
        
        # Act
        result = flashcard_strategy.execute_quiz(single_flashcard, mock_cli_interface)
        
        # Assert
        assert len(result) == 1  # Should be marked as incorrect
        mock_cli_interface.display_incorrect_feedback.assert_called_once()
    
    def test_execute_quiz_with_unicode_input_handles_correctly(
        self, flashcard_strategy, unicode_flashcards, mock_cli_interface
    ):
        """Test that unicode input is handled correctly."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = ["Hello", "Summation", "Target"]
        
        # Act
        result = flashcard_strategy.execute_quiz(unicode_flashcards, mock_cli_interface)
        
        # Assert
        assert len(result) == 0  # All should be correct
        assert mock_cli_interface.display_correct_feedback.call_count == 3
    
    def test_execute_quiz_with_special_characters_in_input_handles_correctly(
        self, flashcard_strategy, special_character_flashcards, mock_cli_interface
    ):
        """Test that special characters in input are handled correctly."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = ["Symbols", "Quoted text", "Multi-line"]
        
        # Act
        result = flashcard_strategy.execute_quiz(special_character_flashcards, mock_cli_interface)
        
        # Assert
        assert len(result) == 0  # All should be correct
        assert mock_cli_interface.display_correct_feedback.call_count == 3
    
    def test_execute_quiz_with_partial_match_input_marks_as_incorrect(
        self, flashcard_strategy, single_flashcard, mock_cli_interface
    ):
        """Test that partial matches are marked as incorrect."""
        # Arrange
        mock_cli_interface.get_user_input.return_value = "Single"  # Partial match
        
        # Act
        result = flashcard_strategy.execute_quiz(single_flashcard, mock_cli_interface)
        
        # Assert
        assert len(result) == 1  # Should be marked as incorrect
        mock_cli_interface.display_incorrect_feedback.assert_called_once()


class TestFlashcardQuizStrategyEdgeCases(TestFlashcardQuizStrategyFixtures):
    """Edge case test scenarios for boundary conditions and special situations."""
    
    def test_execute_quiz_with_empty_flashcard_list_handles_gracefully(
        self, flashcard_strategy, mock_cli_interface
    ):
        """Test that empty flashcard list is handled gracefully."""
        # Act
        result = flashcard_strategy.execute_quiz([], mock_cli_interface)
        
        # Assert
        assert result == []
        mock_cli_interface.display_message.assert_called_with(
            "Starting sequential quiz with 0 flashcards.\n"
        )
        # Should still display summary even with empty list
        mock_cli_interface.display_quiz_summary.assert_called_once()
        assert mock_cli_interface.display_card_front.call_count == 0
        assert mock_cli_interface.get_user_input.call_count == 0
    
    def test_execute_quiz_with_single_flashcard_works_correctly(
        self, flashcard_strategy, single_flashcard, mock_cli_interface
    ):
        """Test that single flashcard quiz works correctly."""
        # Arrange
        mock_cli_interface.get_user_input.return_value = "Single answer"
        
        # Act
        result = flashcard_strategy.execute_quiz(single_flashcard, mock_cli_interface)
        
        # Assert
        assert result == []
        mock_cli_interface.display_card_front.assert_called_once_with("Single question", 1, 1)
        mock_cli_interface.display_correct_feedback.assert_called_once()
        mock_cli_interface.display_quiz_summary.assert_called_once()
    
    def test_execute_quiz_accuracy_calculation_with_zero_division_prevention(
        self, flashcard_strategy, mock_cli_interface
    ):
        """Test that accuracy calculation handles division by zero correctly."""
        # Act
        flashcard_strategy.execute_quiz([], mock_cli_interface)
        
        # Assert
        # Should call display_quiz_summary with 0% accuracy (not raise division error)
        mock_cli_interface.display_quiz_summary.assert_called_once()
        args, kwargs = mock_cli_interface.display_quiz_summary.call_args
        # With 0 total cards, we expect 0 correct answers and 0% accuracy
        assert kwargs['total_cards'] == 0
        assert kwargs['correct_answers'] == 0
    
    def test_execute_quiz_with_duplicate_flashcards_processes_each_instance(
        self, flashcard_strategy, mock_cli_interface
    ):
        """Test that duplicate flashcards are processed as separate instances."""
        # Arrange
        duplicate_card = Flashcard(front="Duplicate", back="Answer")
        duplicate_flashcards = [duplicate_card, duplicate_card, duplicate_card]
        mock_cli_interface.get_user_input.side_effect = ["Wrong", "Answer", "Wrong"]
        
        # Act
        result = flashcard_strategy.execute_quiz(duplicate_flashcards, mock_cli_interface)
        
        # Assert
        # Should have 2 instances of the duplicate card in missed list
        assert len(result) == 2
        assert all(card == duplicate_card for card in result)
        assert mock_cli_interface.display_card_front.call_count == 3
    
    def test_execute_quiz_with_all_incorrect_answers_returns_all_cards(
        self, flashcard_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that all incorrect answers result in all cards being missed."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = ["Wrong1", "Wrong2", "Wrong3", "Wrong4"]
        
        # Act
        result = flashcard_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
        
        # Assert
        assert len(result) == 4  # All cards missed
        assert result == sample_flashcards  # Same order as input
        assert mock_cli_interface.display_incorrect_feedback.call_count == 4
        assert mock_cli_interface.display_correct_feedback.call_count == 0
    
    def test_execute_quiz_with_very_large_dataset_handles_efficiently(
        self, flashcard_strategy, large_flashcard_set, mock_cli_interface
    ):
        """Test that large datasets are handled efficiently."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = [f"Answer {i}" for i in range(100)]
        
        # Act
        start_time = time.time()
        result = flashcard_strategy.execute_quiz(large_flashcard_set, mock_cli_interface)
        end_time = time.time()
        
        # Assert
        assert len(result) == 0  # All correct answers
        assert (end_time - start_time) < 3.0  # Should complete within reasonable time
        assert mock_cli_interface.display_card_front.call_count == 100
        assert mock_cli_interface.display_correct_feedback.call_count == 100
    
    def test_execute_quiz_with_numeric_string_answers_handles_correctly(
        self, flashcard_strategy, mock_cli_interface
    ):
        """Test that numeric string answers are handled correctly."""
        # Arrange
        numeric_cards = [
            Flashcard(front="What is 10 + 5?", back="15"),
            Flashcard(front="Binary 1010?", back="10")
        ]
        mock_cli_interface.get_user_input.side_effect = ["15", "10"]
        
        # Act
        result = flashcard_strategy.execute_quiz(numeric_cards, mock_cli_interface)
        
        # Assert
        assert len(result) == 0  # All correct
        assert mock_cli_interface.display_correct_feedback.call_count == 2
    
    def test_execute_quiz_with_whitespace_in_answers_trims_correctly(
        self, flashcard_strategy, single_flashcard, mock_cli_interface
    ):
        """Test that whitespace in user answers is trimmed correctly."""
        # Arrange
        mock_cli_interface.get_user_input.return_value = "  Single answer  "
        
        # Act
        result = flashcard_strategy.execute_quiz(single_flashcard, mock_cli_interface)
        
        # Assert
        assert len(result) == 0  # Should be correct after trimming
        mock_cli_interface.display_correct_feedback.assert_called_once()


class TestFlashcardQuizStrategyMocking(TestFlashcardQuizStrategyFixtures):
    """Test scenarios using mocks to verify internal behavior and dependencies."""
    
    def test_execute_quiz_calls_flashcard_matches_answer_for_each_card(
        self, flashcard_strategy, mock_cli_interface
    ):
        """Test that matches_answer is called for each flashcard."""
        # Arrange
        mock_cards = [Mock(), Mock(), Mock()]
        for i, card in enumerate(mock_cards):
            card.front = f"Question {i}"
            card.back = f"Answer {i}"
            card.matches_answer.return_value = True
        
        mock_cli_interface.get_user_input.side_effect = ["ans1", "ans2", "ans3"]
        
        # Act
        flashcard_strategy.execute_quiz(mock_cards, mock_cli_interface)
        
        # Assert
        for i, card in enumerate(mock_cards):
            card.matches_answer.assert_called_once_with(f"ans{i+1}")
    
    def test_execute_quiz_calls_display_quiz_summary_with_internal_method(
        self, flashcard_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that _display_quiz_summary is called internally."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = ["Wrong", "4", "Wrong", "Wrong"]
        
        with patch.object(flashcard_strategy, '_display_quiz_summary') as mock_summary:
            # Act
            flashcard_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
            
            # Assert
            mock_summary.assert_called_once()
            args = mock_summary.call_args[0]
            assert args[0] == mock_cli_interface  # cli_interface
            assert args[1] == 1  # correct_answers
            assert args[2] == 4  # total_cards
            assert len(args[3]) == 3  # missed_cards
    
    def test_display_quiz_summary_calls_cli_interface_with_correct_parameters(
        self, flashcard_strategy, mock_cli_interface
    ):
        """Test that _display_quiz_summary calls CLI interface with correct parameters."""
        # Arrange
        missed_cards = [Flashcard(front="Q1", back="A1"), Flashcard(front="Q2", back="A2")]
        
        # Act
        flashcard_strategy._display_quiz_summary(mock_cli_interface, 3, 5, missed_cards)
        
        # Assert
        mock_cli_interface.display_quiz_summary.assert_called_once()
        args, kwargs = mock_cli_interface.display_quiz_summary.call_args
        
        assert kwargs['strategy_name'] == "Sequential Quiz"
        assert kwargs['correct_answers'] == 3
        assert kwargs['total_cards'] == 5
        assert kwargs['accuracy_percentage'] == 60.0
        assert kwargs['missed_cards'] == missed_cards
    
    def test_execute_quiz_user_input_values_passed_to_flashcard_correctly(
        self, flashcard_strategy, mock_cli_interface
    ):
        """Test that user input values are passed correctly to flashcard matching."""
        # Arrange
        mock_flashcard = Mock()
        mock_flashcard.front = "Test"
        mock_flashcard.back = "Test"
        mock_flashcard.matches_answer.return_value = False
        
        user_inputs = ["input1", "input2", "input3"]
        mock_cli_interface.get_user_input.side_effect = user_inputs
        
        # Act
        flashcard_strategy.execute_quiz([mock_flashcard] * 3, mock_cli_interface)
        
        # Assert
        expected_calls = [call(inp) for inp in user_inputs]
        mock_flashcard.matches_answer.assert_has_calls(expected_calls)


class TestFlashcardQuizStrategyIntegration(TestFlashcardQuizStrategyFixtures):
    """Integration test scenarios testing strategy with realistic workflows."""
    
    def test_flashcard_quiz_complete_workflow_with_realistic_scenario(
        self, flashcard_strategy, mock_cli_interface
    ):
        """Test complete quiz workflow with realistic user interaction."""
        # Arrange
        realistic_cards = [
            Flashcard(front="What is OOP?", back="Object-Oriented Programming"),
            Flashcard(front="Python creator?", back="Guido van Rossum"),
            Flashcard(front="HTTP status OK?", back="200"),
            Flashcard(front="Git init command?", back="git init")
        ]
        
        # Simulate realistic user performance (75% accuracy)
        mock_cli_interface.get_user_input.side_effect = [
            "Object-Oriented Programming",  # Correct
            "Van Rossum",                   # Incorrect (missing first name)
            "200",                          # Correct
            "git init"                      # Correct
        ]
        
        # Act
        result = flashcard_strategy.execute_quiz(realistic_cards, mock_cli_interface)
        
        # Assert
        # Should have 1 missed card
        assert len(result) == 1
        assert result[0] == realistic_cards[1]  # Second card (Python creator)
        
        # Should have correct UI interactions
        assert mock_cli_interface.display_card_front.call_count == 4
        assert mock_cli_interface.display_correct_feedback.call_count == 3
        assert mock_cli_interface.display_incorrect_feedback.call_count == 1
        assert mock_cli_interface.display_separator.call_count == 4
        
        # Should display summary with correct stats
        mock_cli_interface.display_quiz_summary.assert_called_once()
        args, kwargs = mock_cli_interface.display_quiz_summary.call_args
        assert kwargs['correct_answers'] == 3
        assert kwargs['total_cards'] == 4
        assert kwargs['accuracy_percentage'] == 75.0
    
    def test_flashcard_quiz_performance_with_realistic_dataset(
        self, flashcard_strategy, mock_cli_interface
    ):
        """Test quiz performance with realistic dataset size."""
        # Arrange
        realistic_cards = [
            Flashcard(front=f"Programming term {i}", back=f"Definition {i}")
            for i in range(25)  # Realistic study session size
        ]
        
        # Simulate 80% accuracy
        answers = []
        for i in range(25):
            if i % 5 == 0:  # Every 5th wrong (20% error rate)
                answers.append(f"Wrong definition {i}")
            else:
                answers.append(f"Definition {i}")
        
        mock_cli_interface.get_user_input.side_effect = answers
        
        # Act
        start_time = time.time()
        result = flashcard_strategy.execute_quiz(realistic_cards, mock_cli_interface)
        end_time = time.time()
        
        # Assert
        # Should complete within reasonable time
        assert (end_time - start_time) < 2.0
        
        # Should have 5 missed cards (20% of 25)
        assert len(result) == 5
        
        # Should have called all UI methods appropriate number of times
        assert mock_cli_interface.display_card_front.call_count == 25
        assert mock_cli_interface.display_separator.call_count == 25
        assert mock_cli_interface.display_correct_feedback.call_count == 20
        assert mock_cli_interface.display_incorrect_feedback.call_count == 5
        mock_cli_interface.display_quiz_summary.assert_called_once()
    
    def test_flashcard_quiz_maintains_state_consistency_throughout_execution(
        self, flashcard_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that internal state remains consistent throughout quiz execution."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = [
            "Programming language", "Wrong", "Paris", "Wrong"
        ]
        
        # Track internal state during execution
        with patch.object(flashcard_strategy, '_display_quiz_summary', wraps=flashcard_strategy._display_quiz_summary) as mock_summary:
            # Act
            result = flashcard_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
            
            # Assert
            # Verify final state consistency
            assert len(result) == 2  # Two missed cards
            
            # Verify internal method was called with consistent data
            mock_summary.assert_called_once()
            args = mock_summary.call_args[0]
            correct_answers = args[1]
            total_cards = args[2]
            missed_cards = args[3]
            
            assert correct_answers == 2
            assert total_cards == 4
            assert len(missed_cards) == 2
            assert missed_cards == result  # Returned value should match internal state