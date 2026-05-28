"""
Comprehensive test suite for CLIInterface class.
Tests command-line interface functionality with pytest framework.
"""

import pytest
import sys
from io import StringIO
from unittest.mock import Mock, patch, call, MagicMock
from typing import List

from src.ui.cli_interface import CLIInterface
from src.models.flashcard import Flashcard


class TestCLIInterfaceFixtures:
    """Test fixtures for CLIInterface testing."""
    
    @pytest.fixture
    def cli_interface(self):
        """Create a CLIInterface instance for testing."""
        return CLIInterface()
    
    @pytest.fixture
    def sample_flashcards(self):
        """Create sample flashcard objects for testing."""
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
    def large_content_flashcards(self):
        """Create flashcards with large content for stress testing."""
        large_front = "A" * 1000
        large_back = "B" * 1000
        return [Flashcard(front=large_front, back=large_back)]
    
    @pytest.fixture
    def empty_flashcards(self):
        """Create empty flashcard list for edge case testing."""
        return []


class TestCLIInterfaceHappyPath:
    """Happy path test scenarios for normal display and operations."""
    
    def test_display_message_outputs_to_stdout(self, cli_interface):
        """Test that display_message outputs correctly to stdout."""
        test_message = "This is a test message"
        
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_message(test_message)
            output = fake_stdout.getvalue().strip()
        
        assert output == test_message
    
    def test_display_error_outputs_to_stderr(self, cli_interface):
        """Test that display_error outputs correctly to stderr."""
        test_error = "This is an error"
        
        with patch('sys.stderr', new=StringIO()) as fake_stderr:
            cli_interface.display_error(test_error)
            output = fake_stderr.getvalue().strip()
        
        assert output == f"Error: {test_error}"
    
    def test_display_card_front_with_basic_parameters(self, cli_interface):
        """Test display_card_front with basic parameters."""
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_card_front("What is 2+2?", 1, 5)
            output = fake_stdout.getvalue().strip()
        
        assert output == "Card 1/5: What is 2+2?"
    
    def test_display_card_front_with_phase_name(self, cli_interface):
        """Test display_card_front with phase name parameter."""
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_card_front("What is 2+2?", 1, 5, "Review Phase")
            output = fake_stdout.getvalue().strip()
        
        assert output == "[Review Phase] Card 1/5: What is 2+2?"
    
    def test_get_user_input_returns_stripped_input(self, cli_interface):
        """Test that get_user_input returns stripped input."""
        test_input = "  test answer  "
        
        with patch('builtins.input', return_value=test_input):
            result = cli_interface.get_user_input()
        
        assert result == "test answer"
    
    def test_get_user_input_with_custom_prompt(self, cli_interface):
        """Test get_user_input with custom prompt."""
        custom_prompt = "Enter your response: "
        test_input = "response"
        
        with patch('builtins.input', return_value=test_input) as mock_input:
            result = cli_interface.get_user_input(custom_prompt)
            
            mock_input.assert_called_once_with(custom_prompt)
            assert result == test_input
    
    def test_display_correct_feedback_shows_positive_message(self, cli_interface):
        """Test that display_correct_feedback shows positive message."""
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_correct_feedback()
            output = fake_stdout.getvalue().strip()
        
        assert output == "Correct"
    
    def test_display_incorrect_feedback_shows_correct_answer(self, cli_interface):
        """Test that display_incorrect_feedback shows the correct answer."""
        correct_answer = "Paris"
        
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_incorrect_feedback(correct_answer)
            output = fake_stdout.getvalue().strip()
        
        assert output == f"Incorrect (correct answer: {correct_answer})"
    
    def test_display_separator_shows_dashes(self, cli_interface):
        """Test that display_separator shows proper separator."""
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_separator()
            output = fake_stdout.getvalue().strip()
        
        assert output == "-" * 40
    
    def test_display_quiz_summary_with_perfect_score(self, cli_interface, sample_flashcards):
        """Test display_quiz_summary with perfect score."""
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_quiz_summary(
                strategy_name="Test Quiz",
                correct_answers=3,
                total_cards=3,
                accuracy_percentage=100.0,
                missed_cards=[]
            )
            output = fake_stdout.getvalue()
        
        assert "TEST QUIZ RESULTS" in output
        assert "Total Questions: 3" in output
        assert "Correct Answers: 3" in output
        assert "Incorrect Answers: 0" in output
        assert "Accuracy: 100.0%" in output
        assert "Perfect score! No missed terms." in output
    
    def test_display_quiz_summary_with_missed_cards(self, cli_interface, sample_flashcards):
        """Test display_quiz_summary with missed cards."""
        missed_cards = sample_flashcards[:2]  # First two cards missed
        
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_quiz_summary(
                strategy_name="Test Quiz",
                correct_answers=1,
                total_cards=3,
                accuracy_percentage=33.3,
                missed_cards=missed_cards
            )
            output = fake_stdout.getvalue()
        
        assert "TEST QUIZ RESULTS" in output
        assert "Total Questions: 3" in output
        assert "Correct Answers: 1" in output
        assert "Incorrect Answers: 2" in output
        assert "Accuracy: 33.3%" in output
        assert "Terms you missed (2):" in output
        assert "1. What is 2 + 2? → 4" in output
        assert "2. What is the capital of France? → Paris" in output


class TestCLIInterfaceErrorConditions:
    """Error condition test scenarios for incorrect inputs and malformed data."""
    
    def test_display_message_with_none_input_raises_error(self, cli_interface):
        """Test that display_message with None input raises appropriate error."""
        with pytest.raises(TypeError):
            cli_interface.display_message(None)
    
    def test_display_error_with_none_input_raises_error(self, cli_interface):
        """Test that display_error with None input raises appropriate error."""
        with pytest.raises(TypeError):
            cli_interface.display_error(None)
    
    def test_display_card_front_with_invalid_card_number_type(self, cli_interface):
        """Test display_card_front with invalid card number type."""
        with pytest.raises(TypeError):
            cli_interface.display_card_front("Test", "invalid", 5)
    
    def test_display_card_front_with_negative_card_number(self, cli_interface):
        """Test display_card_front with negative card number."""
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_card_front("Test", -1, 5)
            output = fake_stdout.getvalue().strip()
        
        # Should still display but with negative number (unusual but not breaking)
        assert "Card -1/5: Test" in output
    
    def test_display_card_front_with_zero_total_cards(self, cli_interface):
        """Test display_card_front with zero total cards."""
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_card_front("Test", 1, 0)
            output = fake_stdout.getvalue().strip()
        
        assert "Card 1/0: Test" in output
    
    def test_get_user_input_handles_eof_error_gracefully(self, cli_interface):
        """Test that get_user_input handles EOFError (Ctrl+D) gracefully."""
        with patch('builtins.input', side_effect=EOFError()):
            with patch('sys.exit') as mock_exit:
                with patch('sys.stdout', new=StringIO()) as fake_stdout:
                    cli_interface.get_user_input()
                    
                    output = fake_stdout.getvalue()
                    assert "Quiz terminated by user." in output
                    mock_exit.assert_called_once_with(0)
    
    def test_get_user_input_with_empty_string_returns_empty(self, cli_interface):
        """Test that get_user_input with empty string returns empty string."""
        with patch('builtins.input', return_value=""):
            result = cli_interface.get_user_input()
        
        assert result == ""
    
    def test_display_incorrect_feedback_with_empty_answer(self, cli_interface):
        """Test display_incorrect_feedback with empty correct answer."""
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_incorrect_feedback("")
            output = fake_stdout.getvalue().strip()
        
        assert output == "Incorrect (correct answer: )"
    
    def test_display_quiz_summary_with_none_missed_cards(self, cli_interface):
        """Test display_quiz_summary with None missed cards."""
        with pytest.raises(TypeError):
            cli_interface.display_quiz_summary(
                strategy_name="Test Quiz",
                correct_answers=3,
                total_cards=3,
                accuracy_percentage=100.0,
                missed_cards=None
            )
    
    def test_display_quiz_summary_with_invalid_accuracy_format(self, cli_interface):
        """Test display_quiz_summary with invalid accuracy format."""
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_quiz_summary(
                strategy_name="Test Quiz",
                correct_answers=3,
                total_cards=3,
                accuracy_percentage=float('inf'),
                missed_cards=[]
            )
            output = fake_stdout.getvalue()
        
        # Should handle inf gracefully
        assert "Accuracy: inf%" in output
    
    def test_display_quiz_summary_with_very_long_strategy_name(self, cli_interface):
        """Test display_quiz_summary with very long strategy name."""
        long_name = "A" * 1000
        
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_quiz_summary(
                strategy_name=long_name,
                correct_answers=1,
                total_cards=1,
                accuracy_percentage=100.0,
                missed_cards=[]
            )
            output = fake_stdout.getvalue()
        
        assert long_name.upper() in output


class TestCLIInterfaceEdgeCases:
    """Edge case test scenarios for boundary conditions."""
    
    def test_display_card_front_with_very_long_content(self, cli_interface):
        """Test display_card_front with very long front text."""
        long_text = "A" * 10000
        
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_card_front(long_text, 1, 1)
            output = fake_stdout.getvalue().strip()
        
        assert f"Card 1/1: {long_text}" in output
    
    def test_display_card_front_with_unicode_content(self, cli_interface):
        """Test display_card_front with unicode content."""
        unicode_text = "测试 🌟 émojis"
        
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_card_front(unicode_text, 1, 1)
            output = fake_stdout.getvalue().strip()
        
        assert f"Card 1/1: {unicode_text}" in output
    
    def test_display_card_front_with_maximum_card_numbers(self, cli_interface):
        """Test display_card_front with very large card numbers."""
        large_number = 999999
        
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_card_front("Test", large_number, large_number)
            output = fake_stdout.getvalue().strip()
        
        assert f"Card {large_number}/{large_number}: Test" in output
    
    def test_get_user_input_with_unicode_input(self, cli_interface):
        """Test get_user_input with unicode input."""
        unicode_input = "测试答案 🎯"
        
        with patch('builtins.input', return_value=unicode_input):
            result = cli_interface.get_user_input()
        
        assert result == unicode_input
    
    def test_get_user_input_with_very_long_input(self, cli_interface):
        """Test get_user_input with very long input."""
        long_input = "A" * 10000
        
        with patch('builtins.input', return_value=long_input):
            result = cli_interface.get_user_input()
        
        assert result == long_input
    
    def test_display_quiz_summary_with_empty_missed_cards_list(self, cli_interface):
        """Test display_quiz_summary with explicitly empty missed cards list."""
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_quiz_summary(
                strategy_name="Test",
                correct_answers=0,
                total_cards=0,
                accuracy_percentage=0.0,
                missed_cards=[]
            )
            output = fake_stdout.getvalue()
        
        assert "Perfect score! No missed terms." in output
    
    def test_display_quiz_summary_with_single_missed_card(self, cli_interface):
        """Test display_quiz_summary with exactly one missed card."""
        missed_card = Flashcard(front="Test question", back="Test answer")
        
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_quiz_summary(
                strategy_name="Test",
                correct_answers=0,
                total_cards=1,
                accuracy_percentage=0.0,
                missed_cards=[missed_card]
            )
            output = fake_stdout.getvalue()
        
        assert "Terms you missed (1):" in output
        assert "1. Test question → Test answer" in output
    
    def test_display_quiz_summary_with_zero_accuracy_calculation(self, cli_interface):
        """Test display_quiz_summary with zero accuracy."""
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_quiz_summary(
                strategy_name="Test",
                correct_answers=0,
                total_cards=5,
                accuracy_percentage=0.0,
                missed_cards=[]
            )
            output = fake_stdout.getvalue()
        
        assert "Accuracy: 0.0%" in output
        assert "Correct Answers: 0" in output
        assert "Incorrect Answers: 5" in output
    
    def test_display_quiz_summary_with_very_large_card_count(self, cli_interface):
        """Test display_quiz_summary with very large numbers of cards."""
        large_count = 999999
        
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_quiz_summary(
                strategy_name="Test",
                correct_answers=large_count,
                total_cards=large_count,
                accuracy_percentage=100.0,
                missed_cards=[]
            )
            output = fake_stdout.getvalue()
        
        assert f"Total Questions: {large_count}" in output
        assert f"Correct Answers: {large_count}" in output


class TestCLIInterfacePerformance:
    """Performance test scenarios for repeated operations."""
    
    def test_display_message_performance_with_repeated_calls(self, cli_interface):
        """Test performance of display_message with many repeated calls."""
        import time
        
        start_time = time.time()
        
        with patch('sys.stdout', new=StringIO()):
            for i in range(1000):
                cli_interface.display_message(f"Message {i}")
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete within reasonable time
        assert execution_time < 1.0
    
    def test_display_card_front_performance_with_repeated_calls(self, cli_interface):
        """Test performance of display_card_front with many repeated calls."""
        import time
        
        start_time = time.time()
        
        with patch('sys.stdout', new=StringIO()):
            for i in range(1000):
                cli_interface.display_card_front(f"Question {i}", i, 1000)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete within reasonable time
        assert execution_time < 1.0
    
    def test_get_user_input_performance_with_repeated_calls(self, cli_interface):
        """Test performance of get_user_input with many repeated calls."""
        import time
        
        start_time = time.time()
        
        with patch('builtins.input', return_value="answer"):
            for i in range(1000):
                result = cli_interface.get_user_input()
                assert result == "answer"
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete within reasonable time
        assert execution_time < 1.0
    
    def test_display_quiz_summary_performance_with_large_missed_cards(self, cli_interface):
        """Test performance of display_quiz_summary with large missed cards list."""
        # Create large list of missed cards
        missed_cards = []
        for i in range(500):
            missed_cards.append(Flashcard(front=f"Question {i}", back=f"Answer {i}"))
        
        import time
        start_time = time.time()
        
        with patch('sys.stdout', new=StringIO()):
            cli_interface.display_quiz_summary(
                strategy_name="Performance Test",
                correct_answers=0,
                total_cards=500,
                accuracy_percentage=0.0,
                missed_cards=missed_cards
            )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete within reasonable time even with 500 missed cards
        assert execution_time < 2.0


class TestCLIInterfaceMocking:
    """Test scenarios using mocks to verify I/O behavior and dependencies."""
    
    def test_display_message_calls_print_with_correct_parameters(self, cli_interface):
        """Test that display_message calls print with correct parameters."""
        test_message = "Test message"
        
        with patch('builtins.print') as mock_print:
            cli_interface.display_message(test_message)
            
            mock_print.assert_called_once_with(test_message)
    
    def test_display_error_calls_print_with_stderr(self, cli_interface):
        """Test that display_error calls print with stderr parameter."""
        test_error = "Test error"
        
        with patch('builtins.print') as mock_print:
            cli_interface.display_error(test_error)
            
            mock_print.assert_called_once_with(f"Error: {test_error}", file=sys.stderr)
    
    def test_get_user_input_calls_input_with_correct_prompt(self, cli_interface):
        """Test that get_user_input calls input with correct prompt."""
        custom_prompt = "Custom prompt: "
        test_response = "user response"
        
        with patch('builtins.input', return_value=test_response) as mock_input:
            result = cli_interface.get_user_input(custom_prompt)
            
            mock_input.assert_called_once_with(custom_prompt)
            assert result == test_response
    
    def test_display_card_front_constructs_correct_output_format(self, cli_interface):
        """Test that display_card_front constructs correct output format."""
        with patch('builtins.print') as mock_print:
            cli_interface.display_card_front("Test question", 3, 10, "Review")
            
            expected_output = "[Review] Card 3/10: Test question"
            mock_print.assert_called_once_with(expected_output)
    
    def test_display_correct_feedback_calls_print_with_exact_message(self, cli_interface):
        """Test that display_correct_feedback calls print with exact message."""
        with patch('builtins.print') as mock_print:
            cli_interface.display_correct_feedback()
            
            mock_print.assert_called_once_with("Correct")
    
    def test_display_incorrect_feedback_formats_message_correctly(self, cli_interface):
        """Test that display_incorrect_feedback formats message correctly."""
        correct_answer = "Expected Answer"
        
        with patch('builtins.print') as mock_print:
            cli_interface.display_incorrect_feedback(correct_answer)
            
            expected_message = f"Incorrect (correct answer: {correct_answer})"
            mock_print.assert_called_once_with(expected_message)
    
    def test_display_separator_prints_exact_separator(self, cli_interface):
        """Test that display_separator prints exact separator."""
        with patch('builtins.print') as mock_print:
            cli_interface.display_separator()
            
            mock_print.assert_called_once_with("-" * 40)


class TestCLIInterfaceIntegration:
    """Integration test scenarios with realistic workflows."""
    
    def test_complete_card_display_workflow(self, cli_interface, sample_flashcards):
        """Test complete workflow of displaying cards with feedback."""
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            # Simulate displaying first card
            cli_interface.display_card_front(
                sample_flashcards[0].front, 1, len(sample_flashcards)
            )
            
            # Simulate correct feedback
            cli_interface.display_correct_feedback()
            cli_interface.display_separator()
            
            # Simulate displaying second card
            cli_interface.display_card_front(
                sample_flashcards[1].front, 2, len(sample_flashcards)
            )
            
            # Simulate incorrect feedback
            cli_interface.display_incorrect_feedback(sample_flashcards[1].back)
            cli_interface.display_separator()
            
            output = fake_stdout.getvalue()
        
        # Verify complete workflow output
        assert "Card 1/3: What is 2 + 2?" in output
        assert "Correct" in output
        assert "Card 2/3: What is the capital of France?" in output
        assert "Incorrect (correct answer: Paris)" in output
        assert "-" * 40 in output
    
    def test_quiz_summary_with_realistic_data(self, cli_interface, sample_flashcards):
        """Test quiz summary with realistic mixed results."""
        missed_cards = [sample_flashcards[1]]  # Only second card missed
        
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            cli_interface.display_quiz_summary(
                strategy_name="Sequential Quiz",
                correct_answers=2,
                total_cards=3,
                accuracy_percentage=66.7,
                missed_cards=missed_cards
            )
            output = fake_stdout.getvalue()
        
        # Verify comprehensive summary
        assert "SEQUENTIAL QUIZ RESULTS" in output
        assert "Total Questions: 3" in output
        assert "Correct Answers: 2" in output
        assert "Incorrect Answers: 1" in output
        assert "Accuracy: 66.7%" in output
        assert "Terms you missed (1):" in output
        assert "1. What is the capital of France? → Paris" in output
    
    def test_unicode_content_integration_workflow(self, cli_interface, unicode_flashcards):
        """Test complete workflow with unicode content."""
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            # Display unicode card
            cli_interface.display_card_front(
                unicode_flashcards[0].front, 1, len(unicode_flashcards)
            )
            
            # Display incorrect feedback with unicode
            cli_interface.display_incorrect_feedback(unicode_flashcards[0].back)
            
            # Display summary with unicode content
            cli_interface.display_quiz_summary(
                strategy_name="Unicode Test",
                correct_answers=0,
                total_cards=1,
                accuracy_percentage=0.0,
                missed_cards=unicode_flashcards[:1]
            )
            
            output = fake_stdout.getvalue()
        
        # Verify unicode handling
        assert "What is 你好 in English?" in output
        assert "Hello" in output
        assert "UNICODE TEST RESULTS" in output
    
    def test_error_handling_workflow_integration(self, cli_interface):
        """Test integration of error handling across multiple methods."""
        with patch('sys.stderr', new=StringIO()) as fake_stderr:
            with patch('sys.stdout', new=StringIO()) as fake_stdout:
                # Display error message
                cli_interface.display_error("File not found")
                
                # Display regular message
                cli_interface.display_message("Continuing with defaults...")
                
                # Display quiz summary with zero results
                cli_interface.display_quiz_summary(
                    strategy_name="Error Recovery",
                    correct_answers=0,
                    total_cards=0,
                    accuracy_percentage=0.0,
                    missed_cards=[]
                )
        
        stderr_output = fake_stderr.getvalue()
        stdout_output = fake_stdout.getvalue()
        
        # Verify error went to stderr, others to stdout
        assert "Error: File not found" in stderr_output
        assert "Continuing with defaults..." in stdout_output
        assert "ERROR RECOVERY RESULTS" in stdout_output
    
    def test_user_input_integration_with_eof_handling(self, cli_interface):
        """Test user input integration with EOF handling."""
        with patch('builtins.input', side_effect=EOFError()):
            with patch('sys.exit') as mock_exit:
                with patch('sys.stdout', new=StringIO()) as fake_stdout:
                    cli_interface.get_user_input("Enter answer: ")
                    
                    output = fake_stdout.getvalue()
                    
                    # Verify graceful termination
                    assert "Quiz terminated by user." in output
                    mock_exit.assert_called_once_with(0)