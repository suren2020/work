"""
Comprehensive test suite for QuizContext class.
Tests the Strategy pattern context implementation with pytest framework.
"""

import pytest
from unittest.mock import Mock, MagicMock, call
from typing import List

from src.quiz.quiz_context import QuizContext
from src.quiz.quiz_strategy import QuizStrategy
from src.models.flashcard import Flashcard


class TestQuizContextFixtures:
    """Test fixtures for QuizContext testing."""
    
    @pytest.fixture
    def mock_quiz_strategy(self):
        """Create a mock quiz strategy for testing."""
        strategy_mock = Mock(spec=QuizStrategy)
        strategy_mock.execute_quiz = Mock()
        return strategy_mock
    
    @pytest.fixture
    def alternative_mock_strategy(self):
        """Create an alternative mock quiz strategy for testing strategy switching."""
        strategy_mock = Mock(spec=QuizStrategy)
        strategy_mock.execute_quiz = Mock()
        return strategy_mock
    
    @pytest.fixture
    def quiz_context(self, mock_quiz_strategy):
        """Create a QuizContext instance with mock strategy for testing."""
        return QuizContext(mock_quiz_strategy)
    
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
            Flashcard(front="What is 5 * 3?", back="15")
        ]
    
    @pytest.fixture
    def unicode_flashcards(self):
        """Create flashcards with unicode content for testing."""
        return [
            Flashcard(front="What is 你好 in English?", back="Hello"),
            Flashcard(front="What does 🌟 represent?", back="Star")
        ]
    
    @pytest.fixture
    def large_flashcard_set(self):
        """Create large set of flashcards for performance testing."""
        return [
            Flashcard(front=f"Question {i}", back=f"Answer {i}")
            for i in range(100)
        ]
    
    @pytest.fixture
    def single_flashcard(self):
        """Create a single flashcard for boundary testing."""
        return [Flashcard(front="Single question", back="Single answer")]
    
    @pytest.fixture
    def empty_flashcards(self):
        """Create empty flashcard list for edge case testing."""
        return []


class TestQuizContextHappyPath:
    """Happy path test scenarios for normal quiz context operations."""
    
    def test_quiz_context_initialization_with_strategy_stores_strategy_correctly(
        self, mock_quiz_strategy
    ):
        """Test that QuizContext initializes correctly with a strategy."""
        quiz_context = QuizContext(mock_quiz_strategy)
        
        # Verify strategy is stored correctly
        assert quiz_context._strategy is mock_quiz_strategy
    
    def test_execute_quiz_delegates_to_strategy_and_returns_result(
        self, quiz_context, mock_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that execute_quiz properly delegates to strategy and returns result."""
        expected_missed_cards = [normal_flashcards[1]]  # Second card missed
        mock_quiz_strategy.execute_quiz.return_value = expected_missed_cards
        
        result = quiz_context.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Verify strategy execute_quiz was called with correct parameters
        mock_quiz_strategy.execute_quiz.assert_called_once_with(
            normal_flashcards, mock_cli_interface
        )
        
        # Verify result is passed through correctly
        assert result == expected_missed_cards
    
    def test_execute_quiz_with_empty_flashcards_delegates_correctly(
        self, quiz_context, mock_quiz_strategy, empty_flashcards, mock_cli_interface
    ):
        """Test that execute_quiz works correctly with empty flashcard list."""
        mock_quiz_strategy.execute_quiz.return_value = []
        
        result = quiz_context.execute_quiz(empty_flashcards, mock_cli_interface)
        
        mock_quiz_strategy.execute_quiz.assert_called_once_with(
            empty_flashcards, mock_cli_interface
        )
        assert result == []
    
    def test_execute_quiz_with_single_flashcard_delegates_correctly(
        self, quiz_context, mock_quiz_strategy, single_flashcard, mock_cli_interface
    ):
        """Test that execute_quiz works correctly with single flashcard."""
        mock_quiz_strategy.execute_quiz.return_value = single_flashcard
        
        result = quiz_context.execute_quiz(single_flashcard, mock_cli_interface)
        
        mock_quiz_strategy.execute_quiz.assert_called_once_with(
            single_flashcard, mock_cli_interface
        )
        assert result == single_flashcard
    
    def test_set_strategy_changes_strategy_correctly(
        self, quiz_context, mock_quiz_strategy, alternative_mock_strategy
    ):
        """Test that set_strategy correctly changes the quiz strategy."""
        # Verify initial strategy
        assert quiz_context._strategy is mock_quiz_strategy
        
        # Change strategy
        quiz_context.set_strategy(alternative_mock_strategy)
        
        # Verify strategy was changed
        assert quiz_context._strategy is alternative_mock_strategy
        assert quiz_context._strategy is not mock_quiz_strategy
    
    def test_strategy_switching_affects_quiz_execution(
        self, quiz_context, mock_quiz_strategy, alternative_mock_strategy,
        normal_flashcards, mock_cli_interface
    ):
        """Test that switching strategies affects which strategy executes the quiz."""
        # Setup different return values for strategies
        mock_quiz_strategy.execute_quiz.return_value = [normal_flashcards[0]]
        alternative_mock_strategy.execute_quiz.return_value = [normal_flashcards[1]]
        
        # Execute with original strategy
        result1 = quiz_context.execute_quiz(normal_flashcards, mock_cli_interface)
        assert result1 == [normal_flashcards[0]]
        mock_quiz_strategy.execute_quiz.assert_called_once()
        
        # Switch strategy
        quiz_context.set_strategy(alternative_mock_strategy)
        
        # Execute with new strategy
        result2 = quiz_context.execute_quiz(normal_flashcards, mock_cli_interface)
        assert result2 == [normal_flashcards[1]]
        alternative_mock_strategy.execute_quiz.assert_called_once()
    
    def test_execute_quiz_preserves_flashcard_list_integrity(
        self, quiz_context, mock_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that execute_quiz doesn't modify the original flashcard list."""
        original_cards = normal_flashcards.copy()
        mock_quiz_strategy.execute_quiz.return_value = []
        
        quiz_context.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Verify original list is unchanged
        assert normal_flashcards == original_cards
        
        # Verify strategy received the correct list
        called_cards = mock_quiz_strategy.execute_quiz.call_args[0][0]
        assert called_cards is normal_flashcards


class TestQuizContextErrorConditions:
    """Error condition test scenarios for incorrect and malformed responses."""
    
    def test_quiz_context_initialization_with_none_strategy_raises_exception(self):
        """Test that initializing with None strategy raises appropriate exception."""
        with pytest.raises(TypeError):
            QuizContext(None)
    
    def test_set_strategy_with_none_strategy_raises_exception(
        self, quiz_context
    ):
        """Test that setting None strategy raises appropriate exception."""
        with pytest.raises(TypeError):
            quiz_context.set_strategy(None)
    
    def test_execute_quiz_with_strategy_exception_propagates_error(
        self, quiz_context, mock_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that strategy exceptions are properly propagated."""
        mock_quiz_strategy.execute_quiz.side_effect = RuntimeError("Strategy execution failed")
        
        with pytest.raises(RuntimeError, match="Strategy execution failed"):
            quiz_context.execute_quiz(normal_flashcards, mock_cli_interface)
    
    def test_execute_quiz_with_invalid_flashcard_type_propagates_error(
        self, quiz_context, mock_quiz_strategy, mock_cli_interface
    ):
        """Test that invalid flashcard types cause appropriate errors."""
        invalid_flashcards = ["not", "flashcard", "objects"]
        mock_quiz_strategy.execute_quiz.side_effect = AttributeError("Invalid flashcard type")
        
        with pytest.raises(AttributeError, match="Invalid flashcard type"):
            quiz_context.execute_quiz(invalid_flashcards, mock_cli_interface)
    
    def test_execute_quiz_with_none_cli_interface_propagates_error(
        self, quiz_context, mock_quiz_strategy, normal_flashcards
    ):
        """Test that None CLI interface causes appropriate error."""
        mock_quiz_strategy.execute_quiz.side_effect = AttributeError("NoneType has no attribute")
        
        with pytest.raises(AttributeError, match="NoneType has no attribute"):
            quiz_context.execute_quiz(normal_flashcards, None)
    
    def test_execute_quiz_with_strategy_returning_invalid_type_propagates_error(
        self, quiz_context, mock_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that strategy returning invalid type is handled correctly."""
        # Strategy returns invalid type instead of list
        mock_quiz_strategy.execute_quiz.return_value = "invalid return type"
        
        # Context should return whatever strategy returns (no validation in context)
        result = quiz_context.execute_quiz(normal_flashcards, mock_cli_interface)
        assert result == "invalid return type"
    
    def test_execute_quiz_with_large_flashcard_content_handles_correctly(
        self, quiz_context, mock_quiz_strategy, mock_cli_interface
    ):
        """Test that very large flashcard content is handled correctly."""
        large_content_cards = [
            Flashcard(front="A" * 10000, back="B" * 10000)
        ]
        mock_quiz_strategy.execute_quiz.return_value = []
        
        result = quiz_context.execute_quiz(large_content_cards, mock_cli_interface)
        
        mock_quiz_strategy.execute_quiz.assert_called_once_with(
            large_content_cards, mock_cli_interface
        )
        assert result == []
    
    def test_execute_quiz_with_unicode_content_handles_correctly(
        self, quiz_context, mock_quiz_strategy, unicode_flashcards, mock_cli_interface
    ):
        """Test that unicode content in flashcards is handled correctly."""
        mock_quiz_strategy.execute_quiz.return_value = unicode_flashcards
        
        result = quiz_context.execute_quiz(unicode_flashcards, mock_cli_interface)
        
        mock_quiz_strategy.execute_quiz.assert_called_once_with(
            unicode_flashcards, mock_cli_interface
        )
        assert result == unicode_flashcards


class TestQuizContextEdgeCases:
    """Edge case test scenarios for boundary conditions and special situations."""
    
    def test_execute_quiz_with_empty_flashcard_list_works_correctly(
        self, quiz_context, mock_quiz_strategy, empty_flashcards, mock_cli_interface
    ):
        """Test that empty flashcard list is handled gracefully."""
        mock_quiz_strategy.execute_quiz.return_value = []
        
        result = quiz_context.execute_quiz(empty_flashcards, mock_cli_interface)
        
        mock_quiz_strategy.execute_quiz.assert_called_once_with(
            empty_flashcards, mock_cli_interface
        )
        assert result == []
    
    def test_execute_quiz_with_very_large_flashcard_set_works_correctly(
        self, quiz_context, mock_quiz_strategy, large_flashcard_set, mock_cli_interface
    ):
        """Test that very large flashcard sets are handled efficiently."""
        mock_quiz_strategy.execute_quiz.return_value = large_flashcard_set[:10]  # 10 missed
        
        import time
        start_time = time.time()
        
        result = quiz_context.execute_quiz(large_flashcard_set, mock_cli_interface)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Context overhead should be minimal (< 0.1 seconds)
        assert execution_time < 0.1
        mock_quiz_strategy.execute_quiz.assert_called_once_with(
            large_flashcard_set, mock_cli_interface
        )
        assert result == large_flashcard_set[:10]
    
    def test_multiple_strategy_changes_work_correctly(
        self, mock_quiz_strategy, alternative_mock_strategy
    ):
        """Test that multiple strategy changes work correctly."""
        # Create third strategy
        third_strategy = Mock(spec=QuizStrategy)
        
        quiz_context = QuizContext(mock_quiz_strategy)
        assert quiz_context._strategy is mock_quiz_strategy
        
        # Change to second strategy
        quiz_context.set_strategy(alternative_mock_strategy)
        assert quiz_context._strategy is alternative_mock_strategy
        
        # Change to third strategy
        quiz_context.set_strategy(third_strategy)
        assert quiz_context._strategy is third_strategy
        
        # Change back to first strategy
        quiz_context.set_strategy(mock_quiz_strategy)
        assert quiz_context._strategy is mock_quiz_strategy
    
    def test_strategy_state_isolation_between_context_instances(
        self, mock_quiz_strategy, alternative_mock_strategy
    ):
        """Test that different context instances don't affect each other."""
        context1 = QuizContext(mock_quiz_strategy)
        context2 = QuizContext(alternative_mock_strategy)
        
        # Verify initial states
        assert context1._strategy is mock_quiz_strategy
        assert context2._strategy is alternative_mock_strategy
        
        # Change strategy in context1
        third_strategy = Mock(spec=QuizStrategy)
        context1.set_strategy(third_strategy)
        
        # Verify context2 is unaffected
        assert context1._strategy is third_strategy
        assert context2._strategy is alternative_mock_strategy
    
    def test_execute_quiz_with_duplicate_flashcards_handles_correctly(
        self, quiz_context, mock_quiz_strategy, mock_cli_interface
    ):
        """Test that duplicate flashcards are handled correctly."""
        duplicate_card = Flashcard(front="Duplicate", back="Answer")
        duplicate_flashcards = [duplicate_card, duplicate_card, duplicate_card]
        
        mock_quiz_strategy.execute_quiz.return_value = [duplicate_card]
        
        result = quiz_context.execute_quiz(duplicate_flashcards, mock_cli_interface)
        
        mock_quiz_strategy.execute_quiz.assert_called_once_with(
            duplicate_flashcards, mock_cli_interface
        )
        assert result == [duplicate_card]
    
    def test_context_with_strategy_returning_none_handles_correctly(
        self, quiz_context, mock_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that strategy returning None is handled correctly."""
        mock_quiz_strategy.execute_quiz.return_value = None
        
        result = quiz_context.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Context should return whatever strategy returns
        assert result is None
        mock_quiz_strategy.execute_quiz.assert_called_once()
    
    def test_context_with_strategy_returning_empty_list_handles_correctly(
        self, quiz_context, mock_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that strategy returning empty list is handled correctly."""
        mock_quiz_strategy.execute_quiz.return_value = []
        
        result = quiz_context.execute_quiz(normal_flashcards, mock_cli_interface)
        
        assert result == []
        mock_quiz_strategy.execute_quiz.assert_called_once()
    
    def test_context_memory_efficiency_with_large_datasets(
        self, quiz_context, mock_quiz_strategy, mock_cli_interface
    ):
        """Test that context doesn't consume excessive memory with large datasets."""
        # Create very large flashcard set
        large_set = []
        for i in range(1000):
            large_set.append(
                Flashcard(front=f"Question {i} with content" * 10, back=f"Answer {i}")
            )
        
        mock_quiz_strategy.execute_quiz.return_value = []
        
        result = quiz_context.execute_quiz(large_set, mock_cli_interface)
        
        # Verify delegation works with large datasets
        mock_quiz_strategy.execute_quiz.assert_called_once_with(
            large_set, mock_cli_interface
        )
        assert result == []


class TestQuizContextMocking:
    """Test scenarios using mocks to verify internal behavior and dependencies."""
    
    def test_execute_quiz_calls_strategy_execute_quiz_exactly_once(
        self, quiz_context, mock_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that strategy's execute_quiz is called exactly once."""
        mock_quiz_strategy.execute_quiz.return_value = []
        
        quiz_context.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Verify exactly one call to strategy
        mock_quiz_strategy.execute_quiz.assert_called_once()
        
        # Verify call parameters
        call_args = mock_quiz_strategy.execute_quiz.call_args
        assert call_args[0][0] is normal_flashcards
        assert call_args[0][1] is mock_cli_interface
    
    def test_execute_quiz_passes_exact_parameters_to_strategy(
        self, quiz_context, mock_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that exact parameters are passed to strategy without modification."""
        mock_quiz_strategy.execute_quiz.return_value = []
        
        quiz_context.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Verify exact parameter passing
        mock_quiz_strategy.execute_quiz.assert_called_once_with(
            normal_flashcards, mock_cli_interface
        )
    
    def test_set_strategy_does_not_call_any_strategy_methods(
        self, quiz_context, mock_quiz_strategy, alternative_mock_strategy
    ):
        """Test that set_strategy only changes strategy without calling methods."""
        # Reset mocks to ensure clean state
        mock_quiz_strategy.reset_mock()
        alternative_mock_strategy.reset_mock()
        
        quiz_context.set_strategy(alternative_mock_strategy)
        
        # Verify no methods were called on either strategy
        mock_quiz_strategy.execute_quiz.assert_not_called()
        alternative_mock_strategy.execute_quiz.assert_not_called()
    
    def test_context_does_not_modify_strategy_state(
        self, quiz_context, mock_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that context doesn't modify strategy state or call unexpected methods."""
        # Setup strategy mock with additional methods to verify they're not called
        mock_quiz_strategy.some_other_method = Mock()
        mock_quiz_strategy.execute_quiz.return_value = []
        
        quiz_context.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Verify only execute_quiz was called
        mock_quiz_strategy.execute_quiz.assert_called_once()
        mock_quiz_strategy.some_other_method.assert_not_called()
    
    def test_context_returns_exact_strategy_result_without_modification(
        self, quiz_context, mock_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that context returns strategy result without any modification."""
        # Create specific return value to verify exact passing
        expected_result = [normal_flashcards[0], normal_flashcards[2]]
        mock_quiz_strategy.execute_quiz.return_value = expected_result
        
        result = quiz_context.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Verify exact object return (identity check)
        assert result is expected_result


class TestQuizContextIntegration:
    """Integration test scenarios testing context with realistic workflows."""
    
    def test_quiz_context_complete_workflow_with_strategy_switching(
        self, mock_quiz_strategy, alternative_mock_strategy, 
        normal_flashcards, mock_cli_interface
    ):
        """Test complete workflow including strategy switching."""
        # Setup different return values for strategies
        mock_quiz_strategy.execute_quiz.return_value = [normal_flashcards[0]]
        alternative_mock_strategy.execute_quiz.return_value = [normal_flashcards[1], normal_flashcards[2]]
        
        # Create context with first strategy
        context = QuizContext(mock_quiz_strategy)
        
        # Execute first quiz
        result1 = context.execute_quiz(normal_flashcards, mock_cli_interface)
        assert result1 == [normal_flashcards[0]]
        mock_quiz_strategy.execute_quiz.assert_called_once()
        
        # Switch to second strategy
        context.set_strategy(alternative_mock_strategy)
        
        # Execute second quiz
        result2 = context.execute_quiz(normal_flashcards, mock_cli_interface)
        assert result2 == [normal_flashcards[1], normal_flashcards[2]]
        alternative_mock_strategy.execute_quiz.assert_called_once()
        
        # Verify total calls
        assert mock_quiz_strategy.execute_quiz.call_count == 1
        assert alternative_mock_strategy.execute_quiz.call_count == 1
    
    def test_quiz_context_performance_with_multiple_executions(
        self, quiz_context, mock_quiz_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test performance with multiple quiz executions."""
        mock_quiz_strategy.execute_quiz.return_value = []
        
        import time
        start_time = time.time()
        
        # Execute multiple quizzes
        for _ in range(100):
            quiz_context.execute_quiz(normal_flashcards, mock_cli_interface)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete 100 executions quickly (context overhead is minimal)
        assert execution_time < 1.0
        assert mock_quiz_strategy.execute_quiz.call_count == 100
    
    def test_quiz_context_integration_with_different_flashcard_types(
        self, quiz_context, mock_quiz_strategy, mock_cli_interface
    ):
        """Test integration with different types of flashcard content."""
        # Test with various flashcard types
        test_cases = [
            # Normal flashcards
            [Flashcard(front="Q1", back="A1"), Flashcard(front="Q2", back="A2")],
            # Unicode flashcards
            [Flashcard(front="你好", back="Hello"), Flashcard(front="🌟", back="Star")],
            # Large content flashcards
            [Flashcard(front="X" * 1000, back="Y" * 1000)],
            # Empty list
            [],
            # Single flashcard
            [Flashcard(front="Single", back="Answer")]
        ]
        
        for i, flashcards in enumerate(test_cases):
            mock_quiz_strategy.execute_quiz.return_value = flashcards[:1] if flashcards else []
            
            result = quiz_context.execute_quiz(flashcards, mock_cli_interface)
            
            # Verify delegation worked for each type
            expected_calls = i + 1
            assert mock_quiz_strategy.execute_quiz.call_count == expected_calls
    
    def test_quiz_context_with_realistic_strategy_behavior_simulation(
        self, normal_flashcards, mock_cli_interface
    ):
        """Test context with realistic strategy behavior simulation."""
        # Create realistic strategy mock that simulates actual behavior
        realistic_strategy = Mock(spec=QuizStrategy)
        
        def simulate_quiz_execution(flashcards, cli_interface):
            # Simulate some missed cards based on flashcard content
            missed = []
            for card in flashcards:
                if "France" in card.front:  # Simulate missing geography questions
                    missed.append(card)
            return missed
        
        realistic_strategy.execute_quiz.side_effect = simulate_quiz_execution
        
        context = QuizContext(realistic_strategy)
        result = context.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Should return the card with "France" in the question
        assert len(result) == 1
        assert "France" in result[0].front
        realistic_strategy.execute_quiz.assert_called_once_with(
            normal_flashcards, mock_cli_interface
        )