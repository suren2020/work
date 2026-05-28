"""
Comprehensive test suite for AdaptiveQuizStrategy class.
Tests happy path scenarios, error conditions, edge cases, and quiz logic.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
import time

from src.quiz.strategies.adaptive_quiz_strategy import AdaptiveQuizStrategy
from src.models.flashcard import Flashcard


class TestAdaptiveQuizStrategyFixtures:
    """Test fixtures for AdaptiveQuizStrategy testing."""
    
    @pytest.fixture
    def adaptive_strategy(self):
        """Create an AdaptiveQuizStrategy instance for testing."""
        return AdaptiveQuizStrategy()
    
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
    def missed_flashcards(self):
        """Create sample missed flashcards for testing."""
        return [
            Flashcard(front="Difficult question 1", back="Difficult answer 1"),
            Flashcard(front="Difficult question 2", back="Difficult answer 2")
        ]
    
    @pytest.fixture
    def mock_cli_interface(self):
        """Create a mock CLI interface for testing."""
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


class TestAdaptiveQuizStrategyHappyPath(TestAdaptiveQuizStrategyFixtures):
    """Happy path test scenarios for normal card processing."""
    
    def test_adaptive_strategy_initialization_creates_empty_missed_cards_list(
        self, adaptive_strategy
    ):
        """Test that AdaptiveQuizStrategy initializes with empty missed cards list."""
        # Assert
        assert adaptive_strategy.initial_missed_cards == []
        assert isinstance(adaptive_strategy.initial_missed_cards, list)
    
    def test_set_initial_missed_cards_stores_cards_correctly(
        self, adaptive_strategy, missed_flashcards
    ):
        """Test that set_initial_missed_cards properly stores missed cards."""
        # Act
        adaptive_strategy.set_initial_missed_cards(missed_flashcards)
        
        # Assert
        assert adaptive_strategy.initial_missed_cards == missed_flashcards
        assert len(adaptive_strategy.initial_missed_cards) == 2
    
    def test_execute_quiz_with_no_initial_missed_cards_runs_main_quiz_only(
        self, adaptive_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test adaptive quiz with no initial missed cards runs main quiz only."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = ["Programming language", "4", "Paris", "Guido van Rossum"]
        
        # Act
        result = adaptive_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
        
        # Assert
        assert isinstance(result, list)
        # Should display message about no previous missed cards
        mock_cli_interface.display_message.assert_any_call(
            "Adaptive Quiz - No previous missed cards. Starting full quiz.\n"
        )
        # Should quiz on all cards
        assert mock_cli_interface.display_card_front.call_count == 4
        # Should display summary
        mock_cli_interface.display_quiz_summary.assert_called_once()
    
    def test_execute_quiz_with_initial_missed_cards_runs_review_then_main_quiz(
        self, adaptive_strategy, sample_flashcards, missed_flashcards, mock_cli_interface
    ):
        """Test adaptive quiz with initial missed cards runs review phase first."""
        # Arrange
        adaptive_strategy.set_initial_missed_cards(missed_flashcards)
        # Answers for review phase (2 cards) + main quiz (4 cards)
        mock_cli_interface.get_user_input.side_effect = [
            "Difficult answer 1", "Difficult answer 2",  # Review phase
            "Programming language", "4", "Paris", "Guido van Rossum"  # Main quiz
        ]
        
        # Act
        result = adaptive_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
        
        # Assert
        assert isinstance(result, list)
        # Should display review phase message
        mock_cli_interface.display_message.assert_any_call(
            "Adaptive Quiz - Reviewing 2 previously missed cards first.\n"
        )
        # Should display completion of review phase
        mock_cli_interface.display_message.assert_any_call(
            "\nReview phase completed. Starting full quiz...\n"
        )
        # Should quiz on review cards (2) + main cards (4) = 6 total
        assert mock_cli_interface.display_card_front.call_count == 6
    
    def test_execute_quiz_with_all_correct_answers_returns_empty_missed_list(
        self, adaptive_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that all correct answers result in empty missed cards list."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = ["Programming language", "4", "Paris", "Guido van Rossum"]
        
        # Act
        result = adaptive_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
        
        # Assert
        assert result == []
        assert len(result) == 0
        # Should call correct feedback for each answer
        assert mock_cli_interface.display_correct_feedback.call_count == 4
        assert mock_cli_interface.display_incorrect_feedback.call_count == 0
    
    def test_execute_quiz_with_mixed_answers_returns_correct_missed_cards(
        self, adaptive_strategy, sample_flashcards, mock_cli_interface
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
        result = adaptive_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
        
        # Assert
        assert len(result) == 2  # Two missed cards
        assert result[0] == sample_flashcards[0]  # First card missed
        assert result[1] == sample_flashcards[2]  # Third card missed
        assert mock_cli_interface.display_correct_feedback.call_count == 2
        assert mock_cli_interface.display_incorrect_feedback.call_count == 2
    
    def test_execute_quiz_calls_display_methods_in_correct_sequence(
        self, adaptive_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that UI methods are called in the correct sequence."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = ["Programming language", "4", "Paris", "Guido van Rossum"]
        
        # Act
        adaptive_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
        
        # Assert
        # Verify sequence of calls
        expected_calls = [
            call("Adaptive Quiz - No previous missed cards. Starting full quiz.\n"),
        ]
        mock_cli_interface.display_message.assert_has_calls(expected_calls, any_order=False)
        
        # Should display each card front
        assert mock_cli_interface.display_card_front.call_count == 4
        # Should display separator after each card
        assert mock_cli_interface.display_separator.call_count == 4
        # Should display final summary
        mock_cli_interface.display_quiz_summary.assert_called_once()


class TestAdaptiveQuizStrategyErrorConditions(TestAdaptiveQuizStrategyFixtures):
    """Error condition test scenarios for incorrect responses and bad formats."""
    
    def test_execute_quiz_with_cli_interface_get_user_input_raises_exception_propagates_error(
        self, adaptive_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that exceptions from CLI interface are properly propagated."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = RuntimeError("CLI error")
        
        # Act & Assert
        with pytest.raises(RuntimeError, match="CLI error"):
            adaptive_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
    
    def test_execute_quiz_with_cli_interface_display_methods_raise_exception_propagates_error(
        self, adaptive_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that exceptions from CLI display methods are properly propagated."""
        # Arrange
        mock_cli_interface.display_card_front.side_effect = RuntimeError("Display error")
        
        # Act & Assert
        with pytest.raises(RuntimeError, match="Display error"):
            adaptive_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
    
    def test_execute_quiz_with_flashcard_matches_answer_raises_exception_propagates_error(
        self, adaptive_strategy, mock_cli_interface
    ):
        """Test that exceptions from flashcard answer matching are properly propagated."""
        # Arrange
        mock_flashcard = Mock()
        mock_flashcard.front = "Test question"
        mock_flashcard.back = "Test answer"
        mock_flashcard.matches_answer.side_effect = RuntimeError("Flashcard error")
        
        mock_cli_interface.get_user_input.return_value = "Some answer"
        
        # Act & Assert
        with pytest.raises(RuntimeError, match="Flashcard error"):
            adaptive_strategy.execute_quiz([mock_flashcard], mock_cli_interface)
    
    def test_execute_quiz_with_empty_user_input_handles_correctly(
        self, adaptive_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that empty user input is handled correctly as incorrect answer."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = ["", "", "", ""]
        
        # Act
        result = adaptive_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
        
        # Assert
        assert len(result) == 4  # All cards should be missed due to empty answers
        assert mock_cli_interface.display_incorrect_feedback.call_count == 4
        assert mock_cli_interface.display_correct_feedback.call_count == 0
    
    def test_execute_quiz_with_very_long_user_input_handles_correctly(
        self, adaptive_strategy, single_flashcard, mock_cli_interface
    ):
        """Test that very long user input is handled correctly."""
        # Arrange
        very_long_input = "A" * 10000  # Very long input
        mock_cli_interface.get_user_input.return_value = very_long_input
        
        # Act
        result = adaptive_strategy.execute_quiz(single_flashcard, mock_cli_interface)
        
        # Assert
        assert len(result) == 1  # Should be marked as incorrect (doesn't match "Single answer")
        mock_cli_interface.display_incorrect_feedback.assert_called_once()
    
    def test_execute_quiz_with_unicode_user_input_handles_correctly(
        self, adaptive_strategy, mock_cli_interface
    ):
        """Test that unicode user input is handled correctly."""
        # Arrange
        unicode_flashcard = [Flashcard(front="Unicode test", back="测试")]
        mock_cli_interface.get_user_input.return_value = "测试"
        
        # Act
        result = adaptive_strategy.execute_quiz(unicode_flashcard, mock_cli_interface)
        
        # Assert
        assert len(result) == 0  # Should be correct match
        mock_cli_interface.display_correct_feedback.assert_called_once()
    
    def test_execute_quiz_with_special_characters_in_user_input_handles_correctly(
        self, adaptive_strategy, mock_cli_interface
    ):
        """Test that special characters in user input are handled correctly."""
        # Arrange
        special_flashcard = [Flashcard(front="Special test", back="@#$%^&*()")]
        mock_cli_interface.get_user_input.return_value = "@#$%^&*()"
        
        # Act
        result = adaptive_strategy.execute_quiz(special_flashcard, mock_cli_interface)
        
        # Assert
        assert len(result) == 0  # Should be correct match
        mock_cli_interface.display_correct_feedback.assert_called_once()


class TestAdaptiveQuizStrategyEdgeCases(TestAdaptiveQuizStrategyFixtures):
    """Edge case test scenarios for boundary conditions and special situations."""
    
    def test_execute_quiz_with_empty_flashcard_list_handles_gracefully(
        self, adaptive_strategy, mock_cli_interface
    ):
        """Test that empty flashcard list is handled gracefully."""
        # Act
        result = adaptive_strategy.execute_quiz([], mock_cli_interface)
        
        # Assert
        assert result == []
        mock_cli_interface.display_message.assert_called_with(
            "Adaptive Quiz - No previous missed cards. Starting full quiz.\n"
        )
        # Should display summary even with empty list
        mock_cli_interface.display_quiz_summary.assert_called_once()
        assert mock_cli_interface.display_card_front.call_count == 0
    
    def test_execute_quiz_with_single_flashcard_works_correctly(
        self, adaptive_strategy, single_flashcard, mock_cli_interface
    ):
        """Test that single flashcard quiz works correctly."""
        # Arrange
        mock_cli_interface.get_user_input.return_value = "Single answer"
        
        # Act
        result = adaptive_strategy.execute_quiz(single_flashcard, mock_cli_interface)
        
        # Assert
        assert result == []
        mock_cli_interface.display_card_front.assert_called_once()
        mock_cli_interface.display_correct_feedback.assert_called_once()
        mock_cli_interface.display_quiz_summary.assert_called_once()
    
    def test_execute_quiz_with_duplicate_flashcards_handles_correctly(
        self, adaptive_strategy, mock_cli_interface
    ):
        """Test that duplicate flashcards are handled correctly."""
        # Arrange
        duplicate_card = Flashcard(front="Duplicate", back="Answer")
        duplicate_flashcards = [duplicate_card, duplicate_card, duplicate_card]
        mock_cli_interface.get_user_input.side_effect = ["Wrong", "Wrong", "Answer"]
        
        # Act
        result = adaptive_strategy.execute_quiz(duplicate_flashcards, mock_cli_interface)
        
        # Assert
        # Should only have one instance of the duplicate card in missed list
        assert len(result) == 1
        assert result[0] == duplicate_card
        assert mock_cli_interface.display_card_front.call_count == 3
    
    def test_execute_quiz_with_review_phase_duplicate_prevention_works_correctly(
        self, adaptive_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that duplicate cards are not added to missed list during review phase."""
        # Arrange
        # Set one of the main quiz cards as initially missed
        initially_missed = [sample_flashcards[0]]  # First card
        adaptive_strategy.set_initial_missed_cards(initially_missed)
        
        # Miss the same card in both review and main quiz
        mock_cli_interface.get_user_input.side_effect = [
            "Wrong answer",      # Miss in review phase
            "Wrong answer",      # Miss same card in main quiz  
            "4", "Paris", "Guido van Rossum"  # Correct answers for other cards
        ]
        
        # Act
        result = adaptive_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
        
        # Assert
        # Should only have the first card once in missed list (no duplicates)
        assert len(result) == 1
        assert result[0] == sample_flashcards[0]
        assert result.count(sample_flashcards[0]) == 1  # No duplicates
    
    def test_set_initial_missed_cards_with_empty_list_works_correctly(
        self, adaptive_strategy
    ):
        """Test that setting empty initial missed cards list works correctly."""
        # Act
        adaptive_strategy.set_initial_missed_cards([])
        
        # Assert
        assert adaptive_strategy.initial_missed_cards == []
    
    def test_set_initial_missed_cards_replaces_previous_list(
        self, adaptive_strategy, missed_flashcards, sample_flashcards
    ):
        """Test that setting initial missed cards replaces previous list."""
        # Arrange
        adaptive_strategy.set_initial_missed_cards(missed_flashcards)
        assert len(adaptive_strategy.initial_missed_cards) == 2
        
        # Act
        adaptive_strategy.set_initial_missed_cards(sample_flashcards[:2])
        
        # Assert
        assert adaptive_strategy.initial_missed_cards == sample_flashcards[:2]
        assert len(adaptive_strategy.initial_missed_cards) == 2
        assert adaptive_strategy.initial_missed_cards != missed_flashcards
    
    def test_execute_quiz_accuracy_calculation_with_zero_cards_handles_division_by_zero(
        self, adaptive_strategy, mock_cli_interface
    ):
        """Test that accuracy calculation handles division by zero correctly."""
        # Act
        adaptive_strategy.execute_quiz([], mock_cli_interface)
        
        # Assert
        # Should call display_quiz_summary with 0% accuracy (not raise division error)
        mock_cli_interface.display_quiz_summary.assert_called_once()
        args, kwargs = mock_cli_interface.display_quiz_summary.call_args
        assert kwargs['accuracy_percentage'] == 0
    
    def test_quiz_card_set_with_very_large_card_set_handles_correctly(
        self, adaptive_strategy, large_flashcard_set, mock_cli_interface
    ):
        """Test that large card sets are handled correctly."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = ["Wrong"] * 100  # All wrong answers
        
        # Act
        start_time = time.time()
        correct, total = adaptive_strategy._quiz_card_set(
            large_flashcard_set, mock_cli_interface, [], "Test Phase"
        )
        end_time = time.time()
        
        # Assert
        assert correct == 0
        assert total == 100
        assert (end_time - start_time) < 5.0  # Should complete within reasonable time
        assert mock_cli_interface.display_card_front.call_count == 100


class TestAdaptiveQuizStrategyMocking(TestAdaptiveQuizStrategyFixtures):
    """Test scenarios using mocks to verify internal behavior and external interactions."""
    
    def test_execute_quiz_calls_quiz_card_set_with_correct_parameters(
        self, adaptive_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that execute_quiz calls _quiz_card_set with correct parameters."""
        # Arrange
        with patch.object(adaptive_strategy, '_quiz_card_set', return_value=(4, 4)) as mock_quiz_set:
            mock_cli_interface.get_user_input.side_effect = ["Programming language", "4", "Paris", "Guido van Rossum"]
            
            # Act
            adaptive_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
            
            # Assert
            mock_quiz_set.assert_called_once_with(
                sample_flashcards, mock_cli_interface, [], "Main Quiz"
            )
    
    def test_execute_quiz_with_initial_missed_cards_calls_quiz_card_set_twice(
        self, adaptive_strategy, sample_flashcards, missed_flashcards, mock_cli_interface
    ):
        """Test that quiz with initial missed cards calls _quiz_card_set twice."""
        # Arrange
        adaptive_strategy.set_initial_missed_cards(missed_flashcards)
        with patch.object(adaptive_strategy, '_quiz_card_set', return_value=(2, 2)) as mock_quiz_set:
            
            # Act
            adaptive_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
            
            # Assert
            assert mock_quiz_set.call_count == 2
            # First call should be for review phase
            first_call = mock_quiz_set.call_args_list[0]
            assert first_call[0][0] == missed_flashcards  # Cards parameter
            assert first_call[0][3] == "Review Phase"      # Phase name
            
            # Second call should be for main quiz
            second_call = mock_quiz_set.call_args_list[1]
            assert second_call[0][0] == sample_flashcards  # Cards parameter
            assert second_call[0][3] == "Main Quiz"        # Phase name
    
    def test_quiz_card_set_calls_flashcard_matches_answer_for_each_card(
        self, adaptive_strategy, mock_cli_interface
    ):
        """Test that _quiz_card_set calls matches_answer for each flashcard."""
        # Arrange
        mock_cards = [Mock(), Mock(), Mock()]
        for i, card in enumerate(mock_cards):
            card.front = f"Question {i}"
            card.back = f"Answer {i}"
            card.matches_answer.return_value = True
        
        mock_cli_interface.get_user_input.side_effect = ["Answer1", "Answer2", "Answer3"]
        
        # Act
        adaptive_strategy._quiz_card_set(mock_cards, mock_cli_interface, [], "Test")
        
        # Assert
        for card in mock_cards:
            card.matches_answer.assert_called_once()
    
    def test_display_quiz_summary_called_with_correct_parameters(
        self, adaptive_strategy, sample_flashcards, mock_cli_interface
    ):
        """Test that display_quiz_summary is called with correct parameters."""
        # Arrange
        mock_cli_interface.get_user_input.side_effect = ["Programming language", "Wrong", "Paris", "Wrong"]
        
        # Act
        result = adaptive_strategy.execute_quiz(sample_flashcards, mock_cli_interface)
        
        # Assert
        mock_cli_interface.display_quiz_summary.assert_called_once()
        args, kwargs = mock_cli_interface.display_quiz_summary.call_args
        
        assert kwargs['strategy_name'] == "Adaptive Quiz"
        assert kwargs['correct_answers'] == 2
        assert kwargs['total_cards'] == 4
        assert kwargs['accuracy_percentage'] == 50.0
        assert len(kwargs['missed_cards']) == 2


class TestAdaptiveQuizStrategyIntegration(TestAdaptiveQuizStrategyFixtures):
    """Integration test scenarios testing adaptive strategy with realistic workflows."""
    
    def test_adaptive_quiz_complete_workflow_with_realistic_scenario(
        self, adaptive_strategy, mock_cli_interface
    ):
        """Test complete adaptive quiz workflow with realistic user interaction."""
        # Arrange - Setup flashcards and previously missed cards
        all_cards = [
            Flashcard(front="Easy question", back="Easy answer"),
            Flashcard(front="Medium question", back="Medium answer"),
            Flashcard(front="Hard question", back="Hard answer"),
        ]
        initially_missed = [all_cards[2]]  # Hard question was missed before
        adaptive_strategy.set_initial_missed_cards(initially_missed)
        
        # Simulate user answers: correct on review, then mixed results on main quiz
        mock_cli_interface.get_user_input.side_effect = [
            "Hard answer",      # Correct on review
            "Easy answer",      # Correct on easy
            "Wrong answer",     # Miss medium  
            "Hard answer"       # Correct on hard again
        ]
        
        # Act
        result = adaptive_strategy.execute_quiz(all_cards, mock_cli_interface)
        
        # Assert
        # Should have review phase message
        mock_cli_interface.display_message.assert_any_call(
            "Adaptive Quiz - Reviewing 1 previously missed cards first.\n"
        )
        
        # Should have only medium card in final missed list
        assert len(result) == 1
        assert result[0] == all_cards[1]  # Medium question
        
        # Should have correct number of UI interactions
        assert mock_cli_interface.display_card_front.call_count == 4  # 1 review + 3 main
        assert mock_cli_interface.display_correct_feedback.call_count == 3
        assert mock_cli_interface.display_incorrect_feedback.call_count == 1
    
    def test_adaptive_quiz_multiple_rounds_simulation(
        self, mock_cli_interface
    ):
        """Test simulation of multiple quiz rounds with adaptive learning."""
        # Arrange
        cards = [
            Flashcard(front="Question 1", back="Answer 1"),
            Flashcard(front="Question 2", back="Answer 2"),
            Flashcard(front="Question 3", back="Answer 3"),
        ]
        
        # Round 1: Miss questions 2 and 3
        round1_strategy = AdaptiveQuizStrategy()
        mock_cli_interface.get_user_input.side_effect = ["Answer 1", "Wrong", "Wrong"]
        round1_missed = round1_strategy.execute_quiz(cards, mock_cli_interface)
        
        # Round 2: Use missed cards from round 1, get question 2 right, miss question 3 again
        round2_strategy = AdaptiveQuizStrategy()
        round2_strategy.set_initial_missed_cards(round1_missed)
        mock_cli_interface.reset_mock()
        mock_cli_interface.get_user_input.side_effect = [
            "Answer 2", "Wrong",       # Review phase: get Q2 right, miss Q3
            "Answer 1", "Answer 2", "Wrong"  # Main quiz: get Q1&Q2 right, miss Q3
        ]
        round2_missed = round2_strategy.execute_quiz(cards, mock_cli_interface)
        
        # Assert
        # Round 1 should have 2 missed cards
        assert len(round1_missed) == 2
        
        # Round 2 should have only 1 missed card (Question 3)
        assert len(round2_missed) == 1
        assert round2_missed[0] == cards[2]  # Question 3
        
        # Round 2 should have review phase
        mock_cli_interface.display_message.assert_any_call(
            "Adaptive Quiz - Reviewing 2 previously missed cards first.\n"
        )
    
    def test_adaptive_quiz_performance_with_realistic_dataset(
        self, adaptive_strategy, mock_cli_interface
    ):
        """Test adaptive quiz performance with realistic dataset size."""
        # Arrange
        realistic_cards = [
            Flashcard(front=f"Question {i}", back=f"Answer {i}")
            for i in range(50)  # Realistic flashcard deck size
        ]
        
        # Simulate mixed performance (70% correct)
        answers = []
        for i in range(50):
            if i % 10 < 7:  # 70% correct
                answers.append(f"Answer {i}")
            else:
                answers.append("Wrong answer")
        
        mock_cli_interface.get_user_input.side_effect = answers
        
        # Act
        start_time = time.time()
        result = adaptive_strategy.execute_quiz(realistic_cards, mock_cli_interface)
        end_time = time.time()
        
        # Assert
        # Should complete within reasonable time
        assert (end_time - start_time) < 3.0
        
        # Should have 15 missed cards (30% of 50)
        assert len(result) == 15
        
        # Should have called all UI methods appropriate number of times
        assert mock_cli_interface.display_card_front.call_count == 50
        assert mock_cli_interface.display_separator.call_count == 50
        mock_cli_interface.display_quiz_summary.assert_called_once()