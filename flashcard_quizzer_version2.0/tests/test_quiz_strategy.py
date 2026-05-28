"""
Comprehensive test suite for QuizStrategy abstract base class.
Tests ABC interface compliance and implementation requirements with pytest framework.
"""

import pytest
from abc import ABC, abstractmethod
from unittest.mock import Mock, MagicMock
from typing import List

from src.quiz.quiz_strategy import QuizStrategy
from src.models.flashcard import Flashcard


class TestQuizStrategyFixtures:
    """Test fixtures for QuizStrategy testing."""
    
    @pytest.fixture
    def valid_concrete_strategy(self):
        """Create a valid concrete implementation of QuizStrategy for testing."""
        class ValidQuizStrategy(QuizStrategy):
            def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
                # Simple implementation that returns first flashcard as missed
                return flashcards[:1] if flashcards else []
        
        return ValidQuizStrategy()
    
    @pytest.fixture
    def mock_concrete_strategy(self):
        """Create a mock concrete implementation of QuizStrategy for testing."""
        class MockQuizStrategy(QuizStrategy):
            def __init__(self):
                self.execute_quiz = Mock()
                self.execute_quiz.return_value = []
            
            def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
                return self.execute_quiz(flashcards, cli_interface)
        
        return MockQuizStrategy()
    
    @pytest.fixture
    def normal_flashcards(self):
        """Create normal flashcard objects for testing."""
        return [
            Flashcard(front="What is 2 + 2?", back="4"),
            Flashcard(front="What is the capital of France?", back="Paris"),
            Flashcard(front="What is 5 * 3?", back="15")
        ]
    
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
    def empty_flashcards(self):
        """Create empty flashcard list for edge case testing."""
        return []
    
    @pytest.fixture
    def single_flashcard(self):
        """Create a single flashcard for boundary testing."""
        return [Flashcard(front="Single question", back="Single answer")]


class TestQuizStrategyAbstractBaseClass:
    """Test scenarios for abstract base class interface compliance."""
    
    def test_quiz_strategy_is_abstract_base_class(self):
        """Test that QuizStrategy is properly defined as an abstract base class."""
        # Verify it's an ABC subclass
        assert issubclass(QuizStrategy, ABC)
        
        # Verify it has abstract methods
        assert hasattr(QuizStrategy, '__abstractmethods__')
        assert 'execute_quiz' in QuizStrategy.__abstractmethods__
    
    def test_quiz_strategy_cannot_be_instantiated_directly(self):
        """Test that QuizStrategy cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class QuizStrategy"):
            QuizStrategy()
    
    def test_incomplete_concrete_implementation_cannot_be_instantiated(self):
        """Test that incomplete concrete implementations cannot be instantiated."""
        class IncompleteQuizStrategy(QuizStrategy):
            # Missing execute_quiz implementation
            pass
        
        with pytest.raises(TypeError, match="Can't instantiate abstract class IncompleteQuizStrategy"):
            IncompleteQuizStrategy()
    
    def test_complete_concrete_implementation_can_be_instantiated(self, valid_concrete_strategy):
        """Test that complete concrete implementations can be instantiated."""
        # Should not raise any exceptions
        assert isinstance(valid_concrete_strategy, QuizStrategy)
        assert hasattr(valid_concrete_strategy, 'execute_quiz')
        assert callable(valid_concrete_strategy.execute_quiz)
    
    def test_execute_quiz_method_signature_is_correct(self, valid_concrete_strategy):
        """Test that execute_quiz method has correct signature."""
        import inspect
        
        signature = inspect.signature(valid_concrete_strategy.execute_quiz)
        parameters = list(signature.parameters.keys())
        
        # Should have self, flashcards, cli_interface parameters
        assert len(parameters) == 3
        assert parameters[0] == 'self'
        assert parameters[1] == 'flashcards'
        assert parameters[2] == 'cli_interface'
        
        # Check return annotation if present
        if signature.return_annotation != inspect.Signature.empty:
            assert signature.return_annotation == List[Flashcard]
    
    def test_execute_quiz_method_is_callable(self, valid_concrete_strategy, normal_flashcards, mock_cli_interface):
        """Test that execute_quiz method is callable with correct parameters."""
        # Should not raise any exceptions when called
        result = valid_concrete_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Should return a list (type checking)
        assert isinstance(result, list)
    
    def test_multiple_concrete_implementations_are_independent(self):
        """Test that multiple concrete implementations are independent."""
        class Strategy1(QuizStrategy):
            def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
                return flashcards[:1]  # Return first card as missed
        
        class Strategy2(QuizStrategy):
            def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
                return flashcards[-1:]  # Return last card as missed
        
        strategy1 = Strategy1()
        strategy2 = Strategy2()
        
        # Verify they are different instances
        assert strategy1 is not strategy2
        assert type(strategy1) != type(strategy2)
        
        # Verify they are both QuizStrategy instances
        assert isinstance(strategy1, QuizStrategy)
        assert isinstance(strategy2, QuizStrategy)


class TestQuizStrategyInterfaceCompliance:
    """Test scenarios for interface compliance and method contracts."""
    
    def test_concrete_strategy_execute_quiz_accepts_correct_parameters(
        self, valid_concrete_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that concrete strategy accepts correct parameter types."""
        # Should accept List[Flashcard] and cli_interface
        result = valid_concrete_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        assert isinstance(result, list)
    
    def test_concrete_strategy_returns_list_of_flashcards(
        self, valid_concrete_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that concrete strategy returns List[Flashcard]."""
        result = valid_concrete_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        
        assert isinstance(result, list)
        # All items in result should be Flashcard instances
        for item in result:
            assert isinstance(item, Flashcard)
    
    def test_concrete_strategy_with_empty_flashcards_returns_list(
        self, valid_concrete_strategy, empty_flashcards, mock_cli_interface
    ):
        """Test that concrete strategy handles empty flashcard list correctly."""
        result = valid_concrete_strategy.execute_quiz(empty_flashcards, mock_cli_interface)
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_concrete_strategy_with_single_flashcard_returns_list(
        self, valid_concrete_strategy, single_flashcard, mock_cli_interface
    ):
        """Test that concrete strategy handles single flashcard correctly."""
        result = valid_concrete_strategy.execute_quiz(single_flashcard, mock_cli_interface)
        
        assert isinstance(result, list)
        # Result should contain 0 or 1 flashcards
        assert len(result) <= 1
    
    def test_concrete_strategy_preserves_flashcard_integrity(
        self, valid_concrete_strategy, normal_flashcards, mock_cli_interface
    ):
        """Test that concrete strategy doesn't modify original flashcard objects."""
        original_fronts = [card.front for card in normal_flashcards]
        original_backs = [card.back for card in normal_flashcards]
        
        valid_concrete_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Original flashcards should be unchanged
        for i, card in enumerate(normal_flashcards):
            assert card.front == original_fronts[i]
            assert card.back == original_backs[i]
    
    def test_abstract_method_decorator_is_present(self):
        """Test that execute_quiz has the abstractmethod decorator."""
        # Check that the method is marked as abstract
        assert hasattr(QuizStrategy.execute_quiz, '__isabstractmethod__')
        assert QuizStrategy.execute_quiz.__isabstractmethod__ is True


class TestQuizStrategyErrorConditions:
    """Error condition test scenarios for invalid implementations and usage."""
    
    def test_concrete_strategy_with_invalid_return_type_detection(self):
        """Test detection of invalid return types from concrete strategies."""
        class InvalidReturnStrategy(QuizStrategy):
            def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
                return "invalid return type"  # Should return List[Flashcard]
        
        strategy = InvalidReturnStrategy()
        normal_flashcards = [Flashcard(front="Test", back="Answer")]
        mock_cli_interface = Mock()
        
        # The method will execute but return wrong type
        result = strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        assert not isinstance(result, list)  # This violates the contract
    
    def test_concrete_strategy_with_exception_in_execute_quiz(self):
        """Test handling of exceptions in concrete strategy execute_quiz method."""
        class ExceptionStrategy(QuizStrategy):
            def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
                raise RuntimeError("Strategy execution failed")
        
        strategy = ExceptionStrategy()
        normal_flashcards = [Flashcard(front="Test", back="Answer")]
        mock_cli_interface = Mock()
        
        with pytest.raises(RuntimeError, match="Strategy execution failed"):
            strategy.execute_quiz(normal_flashcards, mock_cli_interface)
    
    def test_concrete_strategy_with_none_parameters_handling(self):
        """Test concrete strategy handling of None parameters."""
        class RobustStrategy(QuizStrategy):
            def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
                if flashcards is None:
                    raise ValueError("Flashcards cannot be None")
                if cli_interface is None:
                    raise ValueError("CLI interface cannot be None")
                return []
        
        strategy = RobustStrategy()
        
        # Test with None flashcards
        with pytest.raises(ValueError, match="Flashcards cannot be None"):
            strategy.execute_quiz(None, Mock())
        
        # Test with None CLI interface
        with pytest.raises(ValueError, match="CLI interface cannot be None"):
            strategy.execute_quiz([], None)
    
    def test_concrete_strategy_with_invalid_flashcard_objects(self):
        """Test concrete strategy handling of invalid flashcard objects."""
        class StrictStrategy(QuizStrategy):
            def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
                # Verify all items are Flashcard instances
                for card in flashcards:
                    if not isinstance(card, Flashcard):
                        raise TypeError(f"Invalid flashcard type: {type(card)}")
                return []
        
        strategy = StrictStrategy()
        invalid_flashcards = ["not", "flashcard", "objects"]
        mock_cli_interface = Mock()
        
        with pytest.raises(TypeError, match="Invalid flashcard type"):
            strategy.execute_quiz(invalid_flashcards, mock_cli_interface)
    
    def test_concrete_strategy_method_signature_mismatch(self):
        """Test detection of method signature mismatches in concrete implementations."""
        # This will fail at class definition time
        with pytest.raises(TypeError):
            class WrongSignatureStrategy(QuizStrategy):
                def execute_quiz(self, wrong_param):  # Missing required parameters
                    return []


class TestQuizStrategyEdgeCases:
    """Edge case test scenarios for boundary conditions and special situations."""
    
    def test_inheritance_chain_with_multiple_levels(self):
        """Test inheritance chain with multiple levels of abstract and concrete classes."""
        class AbstractQuizVariant(QuizStrategy):
            """Another level of abstraction"""
            @abstractmethod
            def prepare_quiz(self):
                pass
            
            def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
                self.prepare_quiz()
                return []
        
        class ConcreteVariant(AbstractQuizVariant):
            def prepare_quiz(self):
                pass  # Concrete implementation
        
        # AbstractQuizVariant should not be instantiable
        with pytest.raises(TypeError):
            AbstractQuizVariant()
        
        # ConcreteVariant should be instantiable
        strategy = ConcreteVariant()
        assert isinstance(strategy, QuizStrategy)
        assert isinstance(strategy, AbstractQuizVariant)
    
    def test_strategy_with_additional_methods(self):
        """Test strategy implementations with additional non-abstract methods."""
        class ExtendedStrategy(QuizStrategy):
            def __init__(self):
                self.call_count = 0
            
            def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
                self.call_count += 1
                return []
            
            def get_call_count(self):
                return self.call_count
            
            def reset_count(self):
                self.call_count = 0
        
        strategy = ExtendedStrategy()
        normal_flashcards = [Flashcard(front="Test", back="Answer")]
        mock_cli_interface = Mock()
        
        # Should work normally
        assert strategy.get_call_count() == 0
        strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        assert strategy.get_call_count() == 1
        
        strategy.reset_count()
        assert strategy.get_call_count() == 0
    
    def test_strategy_with_class_variables_and_instance_variables(self):
        """Test strategy implementations with various variable types."""
        class StatefulStrategy(QuizStrategy):
            class_counter = 0  # Class variable
            
            def __init__(self, name):
                self.name = name  # Instance variable
                StatefulStrategy.class_counter += 1
                self.instance_id = StatefulStrategy.class_counter
            
            def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
                return []
        
        strategy1 = StatefulStrategy("Strategy 1")
        strategy2 = StatefulStrategy("Strategy 2")
        
        assert strategy1.name == "Strategy 1"
        assert strategy2.name == "Strategy 2"
        assert strategy1.instance_id == 1
        assert strategy2.instance_id == 2
        assert StatefulStrategy.class_counter == 2
    
    def test_strategy_with_very_large_flashcard_sets(self):
        """Test strategy performance with very large flashcard sets."""
        class PerformanceStrategy(QuizStrategy):
            def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
                # Simple implementation that should be fast
                return []
        
        strategy = PerformanceStrategy()
        
        # Create large flashcard set
        large_flashcards = []
        for i in range(1000):
            large_flashcards.append(Flashcard(front=f"Question {i}", back=f"Answer {i}"))
        
        mock_cli_interface = Mock()
        
        import time
        start_time = time.time()
        result = strategy.execute_quiz(large_flashcards, mock_cli_interface)
        end_time = time.time()
        
        # Should complete quickly
        execution_time = end_time - start_time
        assert execution_time < 1.0  # Should complete in less than 1 second
        assert isinstance(result, list)
    
    def test_strategy_memory_efficiency_with_large_datasets(self):
        """Test strategy memory efficiency with large datasets."""
        class MemoryEfficientStrategy(QuizStrategy):
            def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
                # Process cards one by one to minimize memory usage
                missed_cards = []
                for card in flashcards:
                    # Simulate some processing
                    if len(card.front) > 100:  # Arbitrary condition
                        missed_cards.append(card)
                return missed_cards
        
        strategy = MemoryEfficientStrategy()
        
        # Create large content flashcards
        large_content_cards = []
        for i in range(100):
            large_content = "A" * 1000  # 1KB per card
            large_content_cards.append(Flashcard(front=large_content, back=f"Answer {i}"))
        
        mock_cli_interface = Mock()
        result = strategy.execute_quiz(large_content_cards, mock_cli_interface)
        
        # Should return all cards (since front length > 100)
        assert len(result) == 100
        assert all(isinstance(card, Flashcard) for card in result)


class TestQuizStrategyMocking:
    """Test scenarios using mocks to verify interface behavior and compliance."""
    
    def test_strategy_interface_with_mock_implementation(self):
        """Test QuizStrategy interface using mock implementation."""
        # Create a mock that inherits from QuizStrategy
        class MockStrategy(QuizStrategy):
            def __init__(self):
                self.execute_quiz = Mock(return_value=[])
        
        # This should fail because we need actual implementation
        with pytest.raises(TypeError):
            MockStrategy()
    
    def test_strategy_method_call_verification(self, mock_concrete_strategy, normal_flashcards, mock_cli_interface):
        """Test verification of method calls on strategy implementations."""
        result = mock_concrete_strategy.execute_quiz(normal_flashcards, mock_cli_interface)
        
        # Verify the method was called
        mock_concrete_strategy.execute_quiz.assert_called_once_with(normal_flashcards, mock_cli_interface)
        assert result == []
    
    def test_strategy_parameter_verification(self):
        """Test parameter verification for strategy method calls."""
        class TrackingStrategy(QuizStrategy):
            def __init__(self):
                self.last_flashcards = None
                self.last_cli_interface = None
            
            def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
                self.last_flashcards = flashcards
                self.last_cli_interface = cli_interface
                return []
        
        strategy = TrackingStrategy()
        test_flashcards = [Flashcard(front="Test", back="Answer")]
        test_cli_interface = Mock()
        
        strategy.execute_quiz(test_flashcards, test_cli_interface)
        
        # Verify parameters were received correctly
        assert strategy.last_flashcards is test_flashcards
        assert strategy.last_cli_interface is test_cli_interface
    
    def test_strategy_return_value_verification(self):
        """Test verification of return values from strategy implementations."""
        class PredictableStrategy(QuizStrategy):
            def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
                # Return specific flashcards based on content
                missed = []
                for card in flashcards:
                    if "difficult" in card.front.lower():
                        missed.append(card)
                return missed
        
        strategy = PredictableStrategy()
        test_flashcards = [
            Flashcard(front="Easy question", back="Answer"),
            Flashcard(front="Difficult question", back="Answer"),
            Flashcard(front="Another difficult one", back="Answer")
        ]
        mock_cli_interface = Mock()
        
        result = strategy.execute_quiz(test_flashcards, mock_cli_interface)
        
        # Should return only the "difficult" cards
        assert len(result) == 2
        assert all("difficult" in card.front.lower() for card in result)


class TestQuizStrategyIntegration:
    """Integration test scenarios testing strategy interface with realistic workflows."""
    
    def test_quiz_strategy_integration_with_multiple_implementations(self):
        """Test integration of QuizStrategy with multiple concrete implementations."""
        class SimpleStrategy(QuizStrategy):
            def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
                return []  # No missed cards
        
        class SelectiveStrategy(QuizStrategy):
            def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
                return flashcards[::2]  # Every second card is missed
        
        simple = SimpleStrategy()
        selective = SelectiveStrategy()
        
        test_flashcards = [
            Flashcard(front="Q1", back="A1"),
            Flashcard(front="Q2", back="A2"),
            Flashcard(front="Q3", back="A3"),
            Flashcard(front="Q4", back="A4")
        ]
        mock_cli_interface = Mock()
        
        # Test both strategies
        simple_result = simple.execute_quiz(test_flashcards, mock_cli_interface)
        selective_result = selective.execute_quiz(test_flashcards, mock_cli_interface)
        
        assert len(simple_result) == 0
        assert len(selective_result) == 2
        assert selective_result[0].front == "Q1"
        assert selective_result[1].front == "Q3"
    
    def test_quiz_strategy_polymorphic_behavior(self):
        """Test polymorphic behavior of QuizStrategy implementations."""
        class AlwaysMissStrategy(QuizStrategy):
            def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
                return flashcards  # All cards are missed
        
        class NeverMissStrategy(QuizStrategy):
            def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
                return []  # No cards are missed
        
        strategies = [AlwaysMissStrategy(), NeverMissStrategy()]
        test_flashcards = [Flashcard(front="Test", back="Answer")]
        mock_cli_interface = Mock()
        
        results = []
        for strategy in strategies:
            # Polymorphic call - same interface, different behavior
            result = strategy.execute_quiz(test_flashcards, mock_cli_interface)
            results.append(len(result))
        
        assert results == [1, 0]  # AlwaysMiss returns 1, NeverMiss returns 0
    
    def test_quiz_strategy_with_realistic_implementation(self):
        """Test QuizStrategy with realistic implementation mimicking actual strategies."""
        class RealisticStrategy(QuizStrategy):
            def execute_quiz(self, flashcards: List[Flashcard], cli_interface) -> List[Flashcard]:
                # Simulate realistic quiz behavior
                missed_cards = []
                
                for i, card in enumerate(flashcards, 1):
                    # Simulate displaying card
                    cli_interface.display_card_front(card.front, i, len(flashcards))
                    
                    # Simulate getting user input
                    user_answer = cli_interface.get_user_input()
                    
                    # Simulate checking answer
                    if not card.matches_answer(user_answer):
                        cli_interface.display_incorrect_feedback(card.back)
                        missed_cards.append(card)
                    else:
                        cli_interface.display_correct_feedback()
                
                return missed_cards
        
        strategy = RealisticStrategy()
        
        # Create realistic test data
        test_flashcards = [
            Flashcard(front="2 + 2 = ?", back="4"),
            Flashcard(front="Capital of France?", back="Paris")
        ]
        
        # Create mock CLI with realistic responses
        mock_cli_interface = Mock()
        mock_cli_interface.get_user_input.side_effect = ["4", "London"]  # First correct, second wrong
        
        result = strategy.execute_quiz(test_flashcards, mock_cli_interface)
        
        # Verify realistic behavior
        assert len(result) == 1  # One card missed
        assert result[0].front == "Capital of France?"
        
        # Verify CLI interactions
        assert mock_cli_interface.display_card_front.call_count == 2
        assert mock_cli_interface.get_user_input.call_count == 2
        assert mock_cli_interface.display_correct_feedback.call_count == 1
        assert mock_cli_interface.display_incorrect_feedback.call_count == 1