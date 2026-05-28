"""
Comprehensive test suite for MenuSystem class.
Tests menu display, navigation, and quiz orchestration with pytest framework.
"""

import pytest
from unittest.mock import Mock, patch, call, MagicMock
from typing import List

from src.ui.menu_system import MenuSystem
from src.ui.cli_interface import CLIInterface
from src.models.flashcard import Flashcard
from src.quiz.quiz_context import QuizContext
from src.quiz.strategies.flashcard_quiz_strategy import FlashcardQuizStrategy
from src.quiz.strategies.random_quiz_strategy import RandomQuizStrategy
from src.quiz.strategies.adaptive_quiz_strategy import AdaptiveQuizStrategy


class TestMenuSystemFixtures:
    """Test fixtures for MenuSystem testing."""
    
    @pytest.fixture
    def mock_cli_interface(self):
        """Create a mock CLI interface for testing."""
        cli_mock = Mock(spec=CLIInterface)
        cli_mock.display_message = Mock()
        cli_mock.display_error = Mock()
        cli_mock.get_user_input = Mock()
        return cli_mock
    
    @pytest.fixture
    def menu_system(self, mock_cli_interface):
        """Create a MenuSystem instance with mock CLI interface."""
        return MenuSystem(mock_cli_interface)
    
    @pytest.fixture
    def sample_flashcards(self):
        """Create sample flashcard objects for testing."""
        return [
            Flashcard(front="What is 2 + 2?", back="4"),
            Flashcard(front="What is the capital of France?", back="Paris"),
            Flashcard(front="What is 5 * 3?", back="15")
        ]
    
    @pytest.fixture
    def large_flashcard_set(self):
        """Create large set of flashcards for performance testing."""
        return [
            Flashcard(front=f"Question {i}", back=f"Answer {i}")
            for i in range(100)
        ]
    
    @pytest.fixture
    def empty_flashcards(self):
        """Create empty flashcard list for edge case testing."""
        return []
    
    @pytest.fixture
    def single_flashcard(self):
        """Create single flashcard for boundary testing."""
        return [Flashcard(front="Single question", back="Single answer")]


class TestMenuSystemHappyPath:
    """Happy path test scenarios for normal menu display and navigation."""
    
    def test_menu_system_initialization_sets_up_components_correctly(self, mock_cli_interface):
        """Test that MenuSystem initializes with correct components."""
        menu_system = MenuSystem(mock_cli_interface)
        
        assert menu_system.cli_interface is mock_cli_interface
        assert isinstance(menu_system.quiz_context, QuizContext)
        assert menu_system.missed_cards == []
    
    def test_display_menu_shows_all_menu_options(self, menu_system, mock_cli_interface):
        """Test that display_menu shows all available menu options."""
        menu_system._display_menu()
        
        # Verify all menu display calls
        expected_calls = [
            call("\n" + "="*40),
            call("FLASHCARD QUIZ MENU"),
            call("="*40),
            call("1. Sequential"),
            call("2. Random"),
            call("3. Adaptive"),
            call("4. Exit"),
            call("="*40)
        ]
        
        mock_cli_interface.display_message.assert_has_calls(expected_calls)
    
    def test_get_menu_choice_prompts_user_for_input(self, menu_system, mock_cli_interface):
        """Test that get_menu_choice prompts user correctly."""
        mock_cli_interface.get_user_input.return_value = "1"
        
        result = menu_system._get_menu_choice()
        
        mock_cli_interface.get_user_input.assert_called_once_with("Enter your choice (1-4): ")
        assert result == "1"
    
    def test_run_sequential_quiz_executes_flashcard_strategy(self, menu_system, sample_flashcards):
        """Test that sequential quiz runs with FlashcardQuizStrategy."""
        with patch.object(menu_system.quiz_context, 'set_strategy') as mock_set_strategy:
            with patch.object(menu_system.quiz_context, 'execute_quiz', return_value=[]) as mock_execute:
                menu_system._run_sequential_quiz(sample_flashcards)
        
        # Verify strategy was set and quiz executed
        mock_set_strategy.assert_called_once()
        mock_execute.assert_called_once_with(sample_flashcards, menu_system.cli_interface)
        
        # Verify strategy type
        strategy_arg = mock_set_strategy.call_args[0][0]
        assert isinstance(strategy_arg, FlashcardQuizStrategy)
    
    def test_run_random_quiz_executes_random_strategy(self, menu_system, sample_flashcards):
        """Test that random quiz runs with RandomQuizStrategy."""
        with patch.object(menu_system.quiz_context, 'set_strategy') as mock_set_strategy:
            with patch.object(menu_system.quiz_context, 'execute_quiz', return_value=[]) as mock_execute:
                menu_system._run_random_quiz(sample_flashcards)
        
        # Verify strategy was set and quiz executed
        mock_set_strategy.assert_called_once()
        mock_execute.assert_called_once_with(sample_flashcards, menu_system.cli_interface)
        
        # Verify strategy type
        strategy_arg = mock_set_strategy.call_args[0][0]
        assert isinstance(strategy_arg, RandomQuizStrategy)
    
    def test_run_adaptive_quiz_executes_adaptive_strategy(self, menu_system, sample_flashcards):
        """Test that adaptive quiz runs with AdaptiveQuizStrategy."""
        with patch.object(menu_system.quiz_context, 'set_strategy') as mock_set_strategy:
            with patch.object(menu_system.quiz_context, 'execute_quiz', return_value=[]) as mock_execute:
                menu_system._run_adaptive_quiz(sample_flashcards)
        
        # Verify strategy was set and quiz executed
        mock_set_strategy.assert_called_once()
        mock_execute.assert_called_once_with(sample_flashcards, menu_system.cli_interface)
        
        # Verify strategy type
        strategy_arg = mock_set_strategy.call_args[0][0]
        assert isinstance(strategy_arg, AdaptiveQuizStrategy)
    
    def test_run_quiz_menu_exits_on_choice_4(self, menu_system, sample_flashcards, mock_cli_interface):
        """Test that quiz menu exits gracefully on choice 4."""
        mock_cli_interface.get_user_input.return_value = "4"
        
        menu_system.run_quiz_menu(sample_flashcards)
        
        # Verify exit message displayed
        mock_cli_interface.display_message.assert_any_call("Goodbye!")
    
    def test_missed_cards_updated_after_sequential_quiz(self, menu_system, sample_flashcards):
        """Test that missed cards are updated after sequential quiz."""
        missed_cards = [sample_flashcards[0]]
        
        with patch.object(menu_system.quiz_context, 'execute_quiz', return_value=missed_cards):
            menu_system._run_sequential_quiz(sample_flashcards)
        
        assert menu_system.missed_cards == missed_cards
    
    def test_missed_cards_updated_after_random_quiz(self, menu_system, sample_flashcards):
        """Test that missed cards are updated after random quiz."""
        missed_cards = [sample_flashcards[1]]
        
        with patch.object(menu_system.quiz_context, 'execute_quiz', return_value=missed_cards):
            menu_system._run_random_quiz(sample_flashcards)
        
        assert menu_system.missed_cards == missed_cards
    
    def test_adaptive_quiz_receives_initial_missed_cards(self, menu_system, sample_flashcards):
        """Test that adaptive quiz receives initial missed cards."""
        # Set up some missed cards
        initial_missed = [sample_flashcards[0]]
        menu_system.missed_cards = initial_missed
        
        with patch('src.ui.menu_system.AdaptiveQuizStrategy') as mock_strategy_class:
            mock_strategy = Mock()
            mock_strategy.set_initial_missed_cards = Mock()
            mock_strategy_class.return_value = mock_strategy
            
            with patch.object(menu_system.quiz_context, 'execute_quiz', return_value=[]):
                menu_system._run_adaptive_quiz(sample_flashcards)
        
        # Verify missed cards were passed to adaptive strategy
        mock_strategy.set_initial_missed_cards.assert_called_once_with(initial_missed)


class TestMenuSystemErrorConditions:
    """Error condition test scenarios for incorrect menu selections and malformed inputs."""
    
    def test_run_quiz_menu_handles_invalid_choice(self, menu_system, sample_flashcards, mock_cli_interface):
        """Test that invalid menu choice shows error message."""
        mock_cli_interface.get_user_input.side_effect = ["5", "4"]  # Invalid then exit
        
        menu_system.run_quiz_menu(sample_flashcards)
        
        # Verify error message displayed
        mock_cli_interface.display_error.assert_called_with("Invalid choice. Please try again.")
    
    def test_run_quiz_menu_handles_non_numeric_choice(self, menu_system, sample_flashcards, mock_cli_interface):
        """Test that non-numeric menu choice shows error message."""
        mock_cli_interface.get_user_input.side_effect = ["abc", "4"]  # Non-numeric then exit
        
        menu_system.run_quiz_menu(sample_flashcards)
        
        # Verify error message displayed
        mock_cli_interface.display_error.assert_called_with("Invalid choice. Please try again.")
    
    def test_run_quiz_menu_handles_empty_choice(self, menu_system, sample_flashcards, mock_cli_interface):
        """Test that empty menu choice shows error message."""
        mock_cli_interface.get_user_input.side_effect = ["", "4"]  # Empty then exit
        
        menu_system.run_quiz_menu(sample_flashcards)
        
        # Verify error message displayed
        mock_cli_interface.display_error.assert_called_with("Invalid choice. Please try again.")
    
    def test_run_quiz_menu_handles_strategy_execution_error(self, menu_system, sample_flashcards, mock_cli_interface):
        """Test that strategy execution errors are handled appropriately."""
        mock_cli_interface.get_user_input.side_effect = ["1", "4"]  # Sequential then exit
        
        with patch.object(menu_system.quiz_context, 'execute_quiz', side_effect=RuntimeError("Quiz error")):
            with pytest.raises(RuntimeError, match="Quiz error"):
                menu_system.run_quiz_menu(sample_flashcards)
    
    def test_sequential_quiz_with_none_flashcards_handles_error(self, menu_system):
        """Test sequential quiz handling of None flashcards."""
        with patch.object(menu_system.quiz_context, 'execute_quiz', side_effect=AttributeError("NoneType")):
            with pytest.raises(AttributeError):
                menu_system._run_sequential_quiz(None)
    
    def test_random_quiz_with_none_flashcards_handles_error(self, menu_system):
        """Test random quiz handling of None flashcards."""
        with patch.object(menu_system.quiz_context, 'execute_quiz', side_effect=AttributeError("NoneType")):
            with pytest.raises(AttributeError):
                menu_system._run_random_quiz(None)
    
    def test_adaptive_quiz_with_none_flashcards_handles_error(self, menu_system):
        """Test adaptive quiz handling of None flashcards."""
        with patch.object(menu_system.quiz_context, 'execute_quiz', side_effect=AttributeError("NoneType")):
            with pytest.raises(AttributeError):
                menu_system._run_adaptive_quiz(None)
    
    def test_menu_system_initialization_with_none_cli_interface_raises_error(self):
        """Test that MenuSystem initialization with None CLI interface raises error."""
        with pytest.raises(AttributeError):
            menu_system = MenuSystem(None)
            menu_system._display_menu()  # This should trigger the error


class TestMenuSystemEdgeCases:
    """Edge case test scenarios for boundary conditions."""
    
    def test_run_quiz_menu_with_empty_flashcards_list(self, menu_system, empty_flashcards, mock_cli_interface):
        """Test menu operation with empty flashcards list."""
        mock_cli_interface.get_user_input.side_effect = ["1", "4"]  # Sequential then exit
        
        with patch.object(menu_system.quiz_context, 'execute_quiz', return_value=[]):
            menu_system.run_quiz_menu(empty_flashcards)
        
        # Should complete without errors
        mock_cli_interface.display_message.assert_any_call("Goodbye!")
    
    def test_run_quiz_menu_with_single_flashcard(self, menu_system, single_flashcard, mock_cli_interface):
        """Test menu operation with single flashcard."""
        mock_cli_interface.get_user_input.side_effect = ["2", "4"]  # Random then exit
        
        with patch.object(menu_system.quiz_context, 'execute_quiz', return_value=[]):
            menu_system.run_quiz_menu(single_flashcard)
        
        # Should complete without errors
        mock_cli_interface.display_message.assert_any_call("Goodbye!")
    
    def test_missed_cards_handling_with_empty_result(self, menu_system, sample_flashcards):
        """Test missed cards handling when quiz returns empty list."""
        with patch.object(menu_system.quiz_context, 'execute_quiz', return_value=[]):
            menu_system._run_sequential_quiz(sample_flashcards)
        
        # Missed cards should remain empty or unchanged
        assert menu_system.missed_cards == []
    
    def test_adaptive_quiz_without_set_initial_missed_cards_method(self, menu_system, sample_flashcards):
        """Test adaptive quiz when strategy doesn't have set_initial_missed_cards method."""
        menu_system.missed_cards = [sample_flashcards[0]]
        
        with patch('src.ui.menu_system.AdaptiveQuizStrategy') as mock_strategy_class:
            mock_strategy = Mock()
            # Don't add set_initial_missed_cards method
            if hasattr(mock_strategy, 'set_initial_missed_cards'):
                delattr(mock_strategy, 'set_initial_missed_cards')
            mock_strategy_class.return_value = mock_strategy
            
            with patch.object(menu_system.quiz_context, 'execute_quiz', return_value=[]):
                # Should not raise an error
                menu_system._run_adaptive_quiz(sample_flashcards)
    
    def test_menu_choice_with_whitespace_handling(self, menu_system, mock_cli_interface):
        """Test menu choice handling with whitespace."""
        mock_cli_interface.get_user_input.return_value = "  1  "  # Choice with whitespace
        
        result = menu_system._get_menu_choice()
        
        # Should return the choice as-is (CLI interface handles stripping)
        assert result == "  1  "
    
    def test_very_large_flashcard_set_handling(self, menu_system, large_flashcard_set, mock_cli_interface):
        """Test menu operation with very large flashcard set."""
        mock_cli_interface.get_user_input.side_effect = ["3", "4"]  # Adaptive then exit
        
        with patch.object(menu_system.quiz_context, 'execute_quiz', return_value=[]):
            menu_system.run_quiz_menu(large_flashcard_set)
        
        # Should handle large dataset without issues
        mock_cli_interface.display_message.assert_any_call("Goodbye!")
    
    def test_multiple_consecutive_quizzes_with_missed_cards_accumulation(self, menu_system, sample_flashcards):
        """Test multiple consecutive quizzes with missed cards accumulation."""
        # First quiz - some missed cards
        missed_cards_1 = [sample_flashcards[0]]
        with patch.object(menu_system.quiz_context, 'execute_quiz', return_value=missed_cards_1):
            menu_system._run_sequential_quiz(sample_flashcards)
        
        assert menu_system.missed_cards == missed_cards_1
        
        # Second quiz - different missed cards
        missed_cards_2 = [sample_flashcards[1], sample_flashcards[2]]
        with patch.object(menu_system.quiz_context, 'execute_quiz', return_value=missed_cards_2):
            menu_system._run_random_quiz(sample_flashcards)
        
        assert menu_system.missed_cards == missed_cards_2


class TestMenuSystemPerformance:
    """Performance test scenarios for repeated menu operations."""
    
    def test_menu_display_performance_with_repeated_calls(self, menu_system, mock_cli_interface):
        """Test performance of menu display with many repeated calls."""
        import time
        
        start_time = time.time()
        
        for _ in range(1000):
            menu_system._display_menu()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete within reasonable time
        assert execution_time < 1.0
        
        # Verify correct number of calls
        assert mock_cli_interface.display_message.call_count == 8000  # 8 calls per menu * 1000
    
    def test_menu_choice_performance_with_repeated_calls(self, menu_system, mock_cli_interface):
        """Test performance of menu choice with many repeated calls."""
        mock_cli_interface.get_user_input.return_value = "1"
        
        import time
        start_time = time.time()
        
        for _ in range(1000):
            result = menu_system._get_menu_choice()
            assert result == "1"
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete within reasonable time
        assert execution_time < 1.0
    
    def test_strategy_switching_performance_with_repeated_operations(self, menu_system, sample_flashcards):
        """Test performance of strategy switching with repeated operations."""
        import time
        
        with patch.object(menu_system.quiz_context, 'execute_quiz', return_value=[]):
            start_time = time.time()
            
            for i in range(100):
                if i % 3 == 0:
                    menu_system._run_sequential_quiz(sample_flashcards)
                elif i % 3 == 1:
                    menu_system._run_random_quiz(sample_flashcards)
                else:
                    menu_system._run_adaptive_quiz(sample_flashcards)
            
            end_time = time.time()
            execution_time = end_time - start_time
        
        # Should complete within reasonable time
        assert execution_time < 2.0


class TestMenuSystemMocking:
    """Test scenarios using mocks to verify behavior and dependencies."""
    
    def test_menu_system_uses_correct_cli_interface_methods(self, menu_system, mock_cli_interface):
        """Test that MenuSystem uses correct CLI interface methods."""
        menu_system._display_menu()
        
        # Verify only display_message is called, not other methods
        assert mock_cli_interface.display_message.called
        mock_cli_interface.display_error.assert_not_called()
    
    def test_quiz_context_strategy_setting_verification(self, menu_system, sample_flashcards):
        """Test that quiz context strategy setting is called correctly."""
        with patch.object(menu_system.quiz_context, 'set_strategy') as mock_set_strategy:
            with patch.object(menu_system.quiz_context, 'execute_quiz', return_value=[]):
                menu_system._run_sequential_quiz(sample_flashcards)
        
        mock_set_strategy.assert_called_once()
        strategy_arg = mock_set_strategy.call_args[0][0]
        assert isinstance(strategy_arg, FlashcardQuizStrategy)
    
    def test_quiz_context_execute_quiz_parameter_verification(self, menu_system, sample_flashcards):
        """Test that quiz context execute_quiz receives correct parameters."""
        with patch.object(menu_system.quiz_context, 'execute_quiz', return_value=[]) as mock_execute:
            menu_system._run_random_quiz(sample_flashcards)
        
        mock_execute.assert_called_once_with(sample_flashcards, menu_system.cli_interface)
    
    def test_adaptive_strategy_method_call_verification(self, menu_system, sample_flashcards):
        """Test that adaptive strategy method calls are verified."""
        menu_system.missed_cards = [sample_flashcards[0]]
        
        with patch('src.ui.menu_system.AdaptiveQuizStrategy') as mock_strategy_class:
            mock_strategy = Mock()
            mock_strategy.set_initial_missed_cards = Mock()
            mock_strategy_class.return_value = mock_strategy
            
            with patch.object(menu_system.quiz_context, 'execute_quiz', return_value=[]):
                menu_system._run_adaptive_quiz(sample_flashcards)
        
        # Verify strategy instantiation and method calls
        mock_strategy_class.assert_called_once()
        mock_strategy.set_initial_missed_cards.assert_called_once_with([sample_flashcards[0]])


class TestMenuSystemIntegration:
    """Integration test scenarios with realistic workflows."""
    
    def test_complete_menu_workflow_with_sequential_quiz(self, menu_system, sample_flashcards, mock_cli_interface):
        """Test complete menu workflow with sequential quiz selection."""
        mock_cli_interface.get_user_input.side_effect = ["1", "4"]  # Sequential then exit
        
        with patch.object(menu_system.quiz_context, 'execute_quiz', return_value=[sample_flashcards[0]]):
            menu_system.run_quiz_menu(sample_flashcards)
        
        # Verify complete workflow
        assert mock_cli_interface.display_message.call_count > 0
        mock_cli_interface.display_message.assert_any_call("\nStarting Sequential Quiz...")
        mock_cli_interface.display_message.assert_any_call("Goodbye!")
        
        # Verify missed cards were updated
        assert menu_system.missed_cards == [sample_flashcards[0]]
    
    def test_complete_menu_workflow_with_multiple_quizzes(self, menu_system, sample_flashcards, mock_cli_interface):
        """Test complete menu workflow with multiple quiz selections."""
        mock_cli_interface.get_user_input.side_effect = ["1", "2", "3", "4"]  # All quizzes then exit
        
        quiz_results = [
            [sample_flashcards[0]],  # Sequential result
            [sample_flashcards[1]],  # Random result  
            []                       # Adaptive result (perfect)
        ]
        
        with patch.object(menu_system.quiz_context, 'execute_quiz', side_effect=quiz_results):
            menu_system.run_quiz_menu(sample_flashcards)
        
        # Verify all quiz types were started
        mock_cli_interface.display_message.assert_any_call("\nStarting Sequential Quiz...")
        mock_cli_interface.display_message.assert_any_call("\nStarting Random Quiz...")
        mock_cli_interface.display_message.assert_any_call("\nStarting Adaptive Quiz...")
        mock_cli_interface.display_message.assert_any_call("Goodbye!")
    
    def test_error_recovery_workflow_with_invalid_then_valid_choice(self, menu_system, sample_flashcards, mock_cli_interface):
        """Test error recovery workflow with invalid then valid choice."""
        mock_cli_interface.get_user_input.side_effect = ["5", "abc", "", "1", "4"]  # Invalid choices then valid
        
        with patch.object(menu_system.quiz_context, 'execute_quiz', return_value=[]):
            menu_system.run_quiz_menu(sample_flashcards)
        
        # Verify multiple error messages
        assert mock_cli_interface.display_error.call_count == 3
        mock_cli_interface.display_error.assert_called_with("Invalid choice. Please try again.")
        
        # Verify eventually succeeded
        mock_cli_interface.display_message.assert_any_call("Goodbye!")
    
    def test_adaptive_quiz_integration_with_previous_missed_cards(self, menu_system, sample_flashcards, mock_cli_interface):
        """Test adaptive quiz integration with missed cards from previous quiz."""
        mock_cli_interface.get_user_input.side_effect = ["1", "3", "4"]  # Sequential, Adaptive, Exit
        
        # Sequential quiz misses some cards
        missed_from_sequential = [sample_flashcards[0], sample_flashcards[2]]
        
        quiz_results = [
            missed_from_sequential,  # Sequential result
            []                       # Adaptive result (improved)
        ]
        
        with patch.object(menu_system.quiz_context, 'execute_quiz', side_effect=quiz_results):
            menu_system.run_quiz_menu(sample_flashcards)
        
        # Verify workflow completed
        mock_cli_interface.display_message.assert_any_call("\nStarting Sequential Quiz...")
        mock_cli_interface.display_message.assert_any_call("\nStarting Adaptive Quiz...")
        mock_cli_interface.display_message.assert_any_call("Goodbye!")
        
        # Final missed cards should be empty (perfect adaptive performance)
        assert menu_system.missed_cards == []
    
    def test_realistic_user_interaction_simulation(self, menu_system, sample_flashcards, mock_cli_interface):
        """Test realistic user interaction simulation with mixed choices."""
        # Simulate realistic user behavior: try different quizzes, make some errors
        user_inputs = [
            "2",     # Random quiz
            "invalid", # Invalid choice
            "3",     # Adaptive quiz  
            "1",     # Sequential quiz
            "4"      # Exit
        ]
        
        mock_cli_interface.get_user_input.side_effect = user_inputs
        
        quiz_results = [
            [sample_flashcards[0]],      # Random result
            [sample_flashcards[1]],      # Adaptive result
            []                           # Sequential result (perfect)
        ]
        
        with patch.object(menu_system.quiz_context, 'execute_quiz', side_effect=quiz_results):
            menu_system.run_quiz_menu(sample_flashcards)
        
        # Verify complete realistic interaction
        assert mock_cli_interface.display_error.call_count == 1  # One invalid choice
        mock_cli_interface.display_message.assert_any_call("\nStarting Random Quiz...")
        mock_cli_interface.display_message.assert_any_call("\nStarting Adaptive Quiz...")
        mock_cli_interface.display_message.assert_any_call("\nStarting Sequential Quiz...")
        mock_cli_interface.display_message.assert_any_call("Goodbye!")
        
        # Final state should reflect last quiz results
        assert menu_system.missed_cards == []