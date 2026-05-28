#!/usr/bin/env python3
"""
Comprehensive test scenarios for FlashcardQuizzerApp class.
Tests app initialization, data loading, error handling, and integration workflows.
"""

import pytest
import sys
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
from typing import List

from main import FlashcardQuizzerApp
from src.models.flashcard import Flashcard


class TestFlashcardQuizzerAppHappyPath:
    """Test cases for normal application operation scenarios."""
    
    @pytest.fixture
    def mock_dependencies(self):
        """Create mock objects for all FlashcardQuizzerApp dependencies."""
        with patch('main.JSONLoader') as mock_json_loader, \
             patch('main.CLIInterface') as mock_cli_interface, \
             patch('main.MenuSystem') as mock_menu_system:
            
            mock_json_loader_instance = Mock()
            mock_cli_interface_instance = Mock()
            mock_menu_system_instance = Mock()
            
            mock_json_loader.return_value = mock_json_loader_instance
            mock_cli_interface.return_value = mock_cli_interface_instance
            mock_menu_system.return_value = mock_menu_system_instance
            
            yield {
                'json_loader_class': mock_json_loader,
                'cli_interface_class': mock_cli_interface,
                'menu_system_class': mock_menu_system,
                'json_loader': mock_json_loader_instance,
                'cli_interface': mock_cli_interface_instance,
                'menu_system': mock_menu_system_instance
            }
    
    @pytest.fixture
    def sample_flashcards(self):
        """Create sample flashcard objects for testing."""
        return [
            Flashcard("What is Python?", "A programming language"),
            Flashcard("What is a variable?", "A storage location"),
            Flashcard("What is a function?", "A reusable code block")
        ]
    
    def test_app_initialization_sets_up_components_correctly(self, mock_dependencies):
        """Test that FlashcardQuizzerApp initializes all components correctly."""
        app = FlashcardQuizzerApp()
        
        mock_dependencies['json_loader_class'].assert_called_once()
        mock_dependencies['cli_interface_class'].assert_called_once()
        mock_dependencies['menu_system_class'].assert_called_once_with(
            mock_dependencies['cli_interface']
        )
        
        assert app.json_loader == mock_dependencies['json_loader']
        assert app.cli_interface == mock_dependencies['cli_interface']
        assert app.menu_system == mock_dependencies['menu_system']
    
    @patch('pathlib.Path.exists')
    def test_successful_data_loading_and_quiz_execution(self, mock_exists, mock_dependencies, sample_flashcards):
        """Test successful data loading and quiz menu execution."""
        mock_exists.return_value = True
        mock_dependencies['json_loader'].load_flashcards.return_value = sample_flashcards
        
        app = FlashcardQuizzerApp()
        app.run("test_file.json")
        
        mock_dependencies['json_loader'].load_flashcards.assert_called_once_with("test_file.json")
        mock_dependencies['cli_interface'].display_message.assert_called_with(
            "Successfully loaded 3 flashcards."
        )
        mock_dependencies['menu_system'].run_quiz_menu.assert_called_once_with(sample_flashcards)
    
    @patch('pathlib.Path.exists')
    def test_load_and_validate_data_returns_flashcards(self, mock_exists, mock_dependencies, sample_flashcards):
        """Test _load_and_validate_data returns loaded flashcards."""
        mock_exists.return_value = True
        mock_dependencies['json_loader'].load_flashcards.return_value = sample_flashcards
        
        app = FlashcardQuizzerApp()
        result = app._load_and_validate_data("test_file.json")
        
        assert result == sample_flashcards
        mock_dependencies['cli_interface'].display_message.assert_called_with(
            "Successfully loaded 3 flashcards."
        )
    
    @patch('pathlib.Path.exists')
    def test_empty_flashcard_list_handling(self, mock_exists, mock_dependencies):
        """Test handling of empty flashcard list."""
        mock_exists.return_value = True
        mock_dependencies['json_loader'].load_flashcards.return_value = []
        
        app = FlashcardQuizzerApp()
        result = app._load_and_validate_data("test_file.json")
        
        assert result == []
        mock_dependencies['cli_interface'].display_message.assert_called_with(
            "Successfully loaded 0 flashcards."
        )
    
    @patch('pathlib.Path.exists')
    def test_large_flashcard_set_loading(self, mock_exists, mock_dependencies):
        """Test loading large flashcard set."""
        mock_exists.return_value = True
        large_flashcard_set = [
            Flashcard(f"Question {i}", f"Answer {i}") for i in range(1000)
        ]
        mock_dependencies['json_loader'].load_flashcards.return_value = large_flashcard_set
        
        app = FlashcardQuizzerApp()
        result = app._load_and_validate_data("test_file.json")
        
        assert len(result) == 1000
        mock_dependencies['cli_interface'].display_message.assert_called_with(
            "Successfully loaded 1000 flashcards."
        )
    
    @patch('pathlib.Path.exists')
    def test_run_with_empty_flashcards_exits_early(self, mock_exists, mock_dependencies):
        """Test run method exits early when no flashcards loaded."""
        mock_exists.return_value = True
        mock_dependencies['json_loader'].load_flashcards.return_value = []
        
        app = FlashcardQuizzerApp()
        
        with patch.object(app, '_load_and_validate_data', return_value=[]):
            app.run("test_file.json")
        
        mock_dependencies['menu_system'].run_quiz_menu.assert_not_called()


class TestFlashcardQuizzerAppErrorConditions:
    """Test cases for error conditions and malformed inputs."""
    
    @pytest.fixture
    def mock_dependencies(self):
        """Create mock objects for all FlashcardQuizzerApp dependencies."""
        with patch('main.JSONLoader') as mock_json_loader, \
             patch('main.CLIInterface') as mock_cli_interface, \
             patch('main.MenuSystem') as mock_menu_system:
            
            mock_json_loader_instance = Mock()
            mock_cli_interface_instance = Mock()
            mock_menu_system_instance = Mock()
            
            mock_json_loader.return_value = mock_json_loader_instance
            mock_cli_interface.return_value = mock_cli_interface_instance
            mock_menu_system.return_value = mock_menu_system_instance
            
            yield {
                'json_loader': mock_json_loader_instance,
                'cli_interface': mock_cli_interface_instance,
                'menu_system': mock_menu_system_instance
            }
    
    @patch('pathlib.Path.exists')
    @patch('sys.exit')
    def test_file_not_found_error_handling(self, mock_exit, mock_exists, mock_dependencies):
        """Test handling when JSON file does not exist."""
        mock_exists.return_value = False
        
        app = FlashcardQuizzerApp()
        app.run("nonexistent_file.json")
        
        mock_dependencies['cli_interface'].display_error.assert_called_with(
            "File not found: nonexistent_file.json"
        )
        mock_exit.assert_called_with(1)
    
    @patch('pathlib.Path.exists')
    @patch('sys.exit')
    def test_json_loading_error_handling(self, mock_exit, mock_exists, mock_dependencies):
        """Test handling of JSON loading errors."""
        mock_exists.return_value = True
        mock_dependencies['json_loader'].load_flashcards.side_effect = Exception("Invalid JSON format")
        
        app = FlashcardQuizzerApp()
        app.run("test_file.json")
        
        mock_dependencies['cli_interface'].display_error.assert_called_with(
            "Failed to load flashcards: Invalid JSON format"
        )
        mock_exit.assert_called_with(1)
    
    @patch('pathlib.Path.exists')
    @patch('sys.exit')
    def test_keyboard_interrupt_handling(self, mock_exit, mock_exists, mock_dependencies):
        """Test graceful handling of KeyboardInterrupt."""
        mock_exists.return_value = True
        mock_dependencies['json_loader'].load_flashcards.return_value = [
            Flashcard("Test", "Answer")
        ]
        mock_dependencies['menu_system'].run_quiz_menu.side_effect = KeyboardInterrupt
        
        app = FlashcardQuizzerApp()
        app.run("test_file.json")
        
        mock_dependencies['cli_interface'].display_message.assert_called_with(
            "\nQuiz interrupted by user."
        )
        mock_exit.assert_called_with(0)
    
    @patch('pathlib.Path.exists')
    @patch('sys.exit')
    def test_unexpected_error_handling(self, mock_exit, mock_exists, mock_dependencies):
        """Test handling of unexpected errors during execution."""
        mock_exists.return_value = True
        mock_dependencies['json_loader'].load_flashcards.return_value = [
            Flashcard("Test", "Answer")
        ]
        mock_dependencies['menu_system'].run_quiz_menu.side_effect = RuntimeError("Unexpected error")
        
        app = FlashcardQuizzerApp()
        app.run("test_file.json")
        
        mock_dependencies['cli_interface'].display_error.assert_called_with(
            "Unexpected error: Unexpected error"
        )
        mock_exit.assert_called_with(1)
    
    @patch('pathlib.Path.exists')
    @patch('sys.exit')
    def test_permission_error_handling(self, mock_exit, mock_exists, mock_dependencies):
        """Test handling of file permission errors."""
        mock_exists.return_value = True
        mock_dependencies['json_loader'].load_flashcards.side_effect = PermissionError("Permission denied")
        
        app = FlashcardQuizzerApp()
        app.run("test_file.json")
        
        mock_dependencies['cli_interface'].display_error.assert_called_with(
            "Failed to load flashcards: Permission denied"
        )
        mock_exit.assert_called_with(1)
    
    @patch('pathlib.Path.exists')
    @patch('sys.exit')
    def test_none_file_path_error_handling(self, mock_exit, mock_exists, mock_dependencies):
        """Test handling when None is passed as file path."""
        mock_exists.side_effect = TypeError("argument should be a str, bytes or os.PathLike object")
        
        app = FlashcardQuizzerApp()
        app.run(None)
        
        mock_dependencies['cli_interface'].display_error.assert_called()
        mock_exit.assert_called_with(1)
    
    @patch('pathlib.Path.exists')
    @patch('sys.exit')
    def test_empty_string_file_path_handling(self, mock_exit, mock_exists, mock_dependencies):
        """Test handling of empty string as file path."""
        mock_exists.return_value = False
        
        app = FlashcardQuizzerApp()
        app.run("")
        
        mock_dependencies['cli_interface'].display_error.assert_called_with(
            "File not found: "
        )
        mock_exit.assert_called_with(1)
    
    @patch('pathlib.Path.exists')
    @patch('sys.exit')
    def test_unicode_file_path_error_handling(self, mock_exit, mock_exists, mock_dependencies):
        """Test handling of unicode characters in file path."""
        mock_exists.return_value = False
        unicode_path = "测试文件.json"
        
        app = FlashcardQuizzerApp()
        app.run(unicode_path)
        
        mock_dependencies['cli_interface'].display_error.assert_called_with(
            f"File not found: {unicode_path}"
        )
        mock_exit.assert_called_with(1)


class TestFlashcardQuizzerAppEdgeCases:
    """Test cases for edge cases and boundary conditions."""
    
    @pytest.fixture
    def mock_dependencies(self):
        """Create mock objects for all FlashcardQuizzerApp dependencies."""
        with patch('main.JSONLoader') as mock_json_loader, \
             patch('main.CLIInterface') as mock_cli_interface, \
             patch('main.MenuSystem') as mock_menu_system:
            
            mock_json_loader_instance = Mock()
            mock_cli_interface_instance = Mock()
            mock_menu_system_instance = Mock()
            
            mock_json_loader.return_value = mock_json_loader_instance
            mock_cli_interface.return_value = mock_cli_interface_instance
            mock_menu_system.return_value = mock_menu_system_instance
            
            yield {
                'json_loader': mock_json_loader_instance,
                'cli_interface': mock_cli_interface_instance,
                'menu_system': mock_menu_system_instance
            }
    
    @patch('pathlib.Path.exists')
    def test_very_long_file_path_handling(self, mock_exists, mock_dependencies):
        """Test handling of very long file paths."""
        mock_exists.return_value = True
        long_path = "a" * 1000 + ".json"
        mock_dependencies['json_loader'].load_flashcards.return_value = [
            Flashcard("Test", "Answer")
        ]
        
        app = FlashcardQuizzerApp()
        app.run(long_path)
        
        mock_dependencies['json_loader'].load_flashcards.assert_called_once_with(long_path)
        mock_dependencies['menu_system'].run_quiz_menu.assert_called_once()
    
    @patch('pathlib.Path.exists')
    def test_special_characters_in_file_path(self, mock_exists, mock_dependencies):
        """Test handling of special characters in file path."""
        mock_exists.return_value = True
        special_path = "test!@#$%^&*()_+file.json"
        mock_dependencies['json_loader'].load_flashcards.return_value = [
            Flashcard("Test", "Answer")
        ]
        
        app = FlashcardQuizzerApp()
        app.run(special_path)
        
        mock_dependencies['json_loader'].load_flashcards.assert_called_once_with(special_path)
        mock_dependencies['menu_system'].run_quiz_menu.assert_called_once()
    
    @patch('pathlib.Path.exists')
    def test_relative_path_handling(self, mock_exists, mock_dependencies):
        """Test handling of relative file paths."""
        mock_exists.return_value = True
        relative_path = "../data/flashcards.json"
        mock_dependencies['json_loader'].load_flashcards.return_value = [
            Flashcard("Test", "Answer")
        ]
        
        app = FlashcardQuizzerApp()
        app.run(relative_path)
        
        mock_dependencies['json_loader'].load_flashcards.assert_called_once_with(relative_path)
        mock_dependencies['menu_system'].run_quiz_menu.assert_called_once()
    
    @patch('pathlib.Path.exists')
    def test_absolute_path_handling(self, mock_exists, mock_dependencies):
        """Test handling of absolute file paths."""
        mock_exists.return_value = True
        absolute_path = "/absolute/path/to/flashcards.json"
        mock_dependencies['json_loader'].load_flashcards.return_value = [
            Flashcard("Test", "Answer")
        ]
        
        app = FlashcardQuizzerApp()
        app.run(absolute_path)
        
        mock_dependencies['json_loader'].load_flashcards.assert_called_once_with(absolute_path)
        mock_dependencies['menu_system'].run_quiz_menu.assert_called_once()
    
    @patch('pathlib.Path.exists')
    def test_file_without_extension_handling(self, mock_exists, mock_dependencies):
        """Test handling of files without extension."""
        mock_exists.return_value = True
        no_extension_path = "flashcards"
        mock_dependencies['json_loader'].load_flashcards.return_value = [
            Flashcard("Test", "Answer")
        ]
        
        app = FlashcardQuizzerApp()
        app.run(no_extension_path)
        
        mock_dependencies['json_loader'].load_flashcards.assert_called_once_with(no_extension_path)
        mock_dependencies['menu_system'].run_quiz_menu.assert_called_once()
    
    @patch('pathlib.Path.exists')
    def test_duplicate_consecutive_runs(self, mock_exists, mock_dependencies):
        """Test multiple consecutive runs of the same file."""
        mock_exists.return_value = True
        mock_dependencies['json_loader'].load_flashcards.return_value = [
            Flashcard("Test", "Answer")
        ]
        
        app = FlashcardQuizzerApp()
        
        app.run("test_file.json")
        app.run("test_file.json")
        
        assert mock_dependencies['json_loader'].load_flashcards.call_count == 2
        assert mock_dependencies['menu_system'].run_quiz_menu.call_count == 2
    
    @patch('pathlib.Path.exists')
    def test_single_flashcard_handling(self, mock_exists, mock_dependencies):
        """Test handling of single flashcard."""
        mock_exists.return_value = True
        single_flashcard = [Flashcard("Single question", "Single answer")]
        mock_dependencies['json_loader'].load_flashcards.return_value = single_flashcard
        
        app = FlashcardQuizzerApp()
        app.run("test_file.json")
        
        mock_dependencies['cli_interface'].display_message.assert_called_with(
            "Successfully loaded 1 flashcards."
        )
        mock_dependencies['menu_system'].run_quiz_menu.assert_called_once_with(single_flashcard)
    
    @patch('pathlib.Path.exists')
    def test_maximum_flashcards_handling(self, mock_exists, mock_dependencies):
        """Test handling of maximum number of flashcards."""
        mock_exists.return_value = True
        max_flashcards = [Flashcard(f"Q{i}", f"A{i}") for i in range(999999)]
        mock_dependencies['json_loader'].load_flashcards.return_value = max_flashcards
        
        app = FlashcardQuizzerApp()
        app.run("test_file.json")
        
        mock_dependencies['cli_interface'].display_message.assert_called_with(
            "Successfully loaded 999999 flashcards."
        )
        mock_dependencies['menu_system'].run_quiz_menu.assert_called_once_with(max_flashcards)


class TestFlashcardQuizzerAppPerformance:
    """Test cases for performance scenarios with repeated operations."""
    
    @pytest.fixture
    def mock_dependencies(self):
        """Create mock objects for all FlashcardQuizzerApp dependencies."""
        with patch('main.JSONLoader') as mock_json_loader, \
             patch('main.CLIInterface') as mock_cli_interface, \
             patch('main.MenuSystem') as mock_menu_system:
            
            mock_json_loader_instance = Mock()
            mock_cli_interface_instance = Mock()
            mock_menu_system_instance = Mock()
            
            mock_json_loader.return_value = mock_json_loader_instance
            mock_cli_interface.return_value = mock_cli_interface_instance
            mock_menu_system.return_value = mock_menu_system_instance
            
            yield {
                'json_loader': mock_json_loader_instance,
                'cli_interface': mock_cli_interface_instance,
                'menu_system': mock_menu_system_instance
            }
    
    @patch('pathlib.Path.exists')
    def test_repeated_app_initialization_performance(self, mock_exists, mock_dependencies):
        """Test performance of repeated app initializations."""
        start_time = time.time()
        
        for _ in range(100):
            FlashcardQuizzerApp()
        
        end_time = time.time()
        assert end_time - start_time < 1.0
    
    @patch('pathlib.Path.exists')
    def test_repeated_file_loading_performance(self, mock_exists, mock_dependencies):
        """Test performance of repeated file loading operations."""
        mock_exists.return_value = True
        mock_dependencies['json_loader'].load_flashcards.return_value = [
            Flashcard("Test", "Answer")
        ]
        
        app = FlashcardQuizzerApp()
        start_time = time.time()
        
        for _ in range(100):
            app._load_and_validate_data("test_file.json")
        
        end_time = time.time()
        assert end_time - start_time < 1.0
    
    @patch('pathlib.Path.exists')
    def test_repeated_run_calls_performance(self, mock_exists, mock_dependencies):
        """Test performance of repeated run method calls."""
        mock_exists.return_value = True
        mock_dependencies['json_loader'].load_flashcards.return_value = [
            Flashcard("Test", "Answer")
        ]
        
        app = FlashcardQuizzerApp()
        start_time = time.time()
        
        for _ in range(50):
            app.run("test_file.json")
        
        end_time = time.time()
        assert end_time - start_time < 2.0
    
    @patch('pathlib.Path.exists')
    def test_large_flashcard_processing_performance(self, mock_exists, mock_dependencies):
        """Test performance with large flashcard sets."""
        mock_exists.return_value = True
        large_set = [Flashcard(f"Q{i}", f"A{i}") for i in range(5000)]
        mock_dependencies['json_loader'].load_flashcards.return_value = large_set
        
        app = FlashcardQuizzerApp()
        start_time = time.time()
        
        app.run("test_file.json")
        
        end_time = time.time()
        assert end_time - start_time < 2.0
    
    @patch('pathlib.Path.exists')
    def test_memory_efficiency_with_repeated_operations(self, mock_exists, mock_dependencies):
        """Test memory efficiency with repeated operations."""
        mock_exists.return_value = True
        mock_dependencies['json_loader'].load_flashcards.return_value = [
            Flashcard("Test", "Answer") for _ in range(100)
        ]
        
        apps = []
        start_time = time.time()
        
        for i in range(100):
            app = FlashcardQuizzerApp()
            app.run("test_file.json")
            apps.append(app)
        
        end_time = time.time()
        assert end_time - start_time < 3.0
        assert len(apps) == 100


class TestFlashcardQuizzerAppMocking:
    """Test cases for verifying dependency interactions through mocking."""
    
    @pytest.fixture
    def mock_dependencies(self):
        """Create mock objects for all FlashcardQuizzerApp dependencies."""
        with patch('main.JSONLoader') as mock_json_loader, \
             patch('main.CLIInterface') as mock_cli_interface, \
             patch('main.MenuSystem') as mock_menu_system:
            
            mock_json_loader_instance = Mock()
            mock_cli_interface_instance = Mock()
            mock_menu_system_instance = Mock()
            
            mock_json_loader.return_value = mock_json_loader_instance
            mock_cli_interface.return_value = mock_cli_interface_instance
            mock_menu_system.return_value = mock_menu_system_instance
            
            yield {
                'json_loader_class': mock_json_loader,
                'cli_interface_class': mock_cli_interface,
                'menu_system_class': mock_menu_system,
                'json_loader': mock_json_loader_instance,
                'cli_interface': mock_cli_interface_instance,
                'menu_system': mock_menu_system_instance
            }
    
    def test_component_initialization_calls(self, mock_dependencies):
        """Test that component initialization calls are made correctly."""
        FlashcardQuizzerApp()
        
        mock_dependencies['json_loader_class'].assert_called_once_with()
        mock_dependencies['cli_interface_class'].assert_called_once_with()
        mock_dependencies['menu_system_class'].assert_called_once_with(
            mock_dependencies['cli_interface']
        )
    
    @patch('pathlib.Path.exists')
    def test_path_exists_call_verification(self, mock_exists, mock_dependencies):
        """Test that Path.exists is called with correct file path."""
        mock_exists.return_value = True
        mock_dependencies['json_loader'].load_flashcards.return_value = []
        
        app = FlashcardQuizzerApp()
        app.run("test_file.json")
        
        mock_exists.assert_called_once()
    
    @patch('pathlib.Path.exists')
    def test_json_loader_call_verification(self, mock_exists, mock_dependencies):
        """Test that JSONLoader.load_flashcards is called with correct parameters."""
        mock_exists.return_value = True
        mock_dependencies['json_loader'].load_flashcards.return_value = [
            Flashcard("Test", "Answer")
        ]
        
        app = FlashcardQuizzerApp()
        app.run("specific_file.json")
        
        mock_dependencies['json_loader'].load_flashcards.assert_called_once_with(
            "specific_file.json"
        )
    
    @patch('pathlib.Path.exists')
    def test_cli_interface_success_message_call(self, mock_exists, mock_dependencies):
        """Test that CLI interface success message is called correctly."""
        mock_exists.return_value = True
        flashcards = [Flashcard("Q1", "A1"), Flashcard("Q2", "A2")]
        mock_dependencies['json_loader'].load_flashcards.return_value = flashcards
        
        app = FlashcardQuizzerApp()
        app.run("test_file.json")
        
        expected_calls = [
            call("Successfully loaded 2 flashcards.")
        ]
        mock_dependencies['cli_interface'].display_message.assert_has_calls(expected_calls)
    
    @patch('pathlib.Path.exists')
    def test_menu_system_run_call_verification(self, mock_exists, mock_dependencies):
        """Test that MenuSystem.run_quiz_menu is called with loaded flashcards."""
        mock_exists.return_value = True
        flashcards = [Flashcard("Test", "Answer")]
        mock_dependencies['json_loader'].load_flashcards.return_value = flashcards
        
        app = FlashcardQuizzerApp()
        app.run("test_file.json")
        
        mock_dependencies['menu_system'].run_quiz_menu.assert_called_once_with(flashcards)
    
    @patch('pathlib.Path.exists')
    def test_error_display_call_verification(self, mock_exists, mock_dependencies):
        """Test that error messages are displayed through CLI interface."""
        mock_exists.return_value = False
        
        with patch('sys.exit'):
            app = FlashcardQuizzerApp()
            app.run("nonexistent.json")
        
        mock_dependencies['cli_interface'].display_error.assert_called_once_with(
            "File not found: nonexistent.json"
        )
    
    @patch('pathlib.Path.exists')
    @patch('sys.exit')
    def test_sys_exit_call_verification(self, mock_exit, mock_exists, mock_dependencies):
        """Test that sys.exit is called with correct exit codes."""
        mock_exists.return_value = False
        
        app = FlashcardQuizzerApp()
        app.run("nonexistent.json")
        
        mock_exit.assert_called_once_with(1)
    
    @patch('pathlib.Path.exists')
    def test_keyboard_interrupt_message_call(self, mock_exists, mock_dependencies):
        """Test that KeyboardInterrupt displays correct message."""
        mock_exists.return_value = True
        mock_dependencies['json_loader'].load_flashcards.return_value = [
            Flashcard("Test", "Answer")
        ]
        mock_dependencies['menu_system'].run_quiz_menu.side_effect = KeyboardInterrupt
        
        with patch('sys.exit'):
            app = FlashcardQuizzerApp()
            app.run("test_file.json")
        
        mock_dependencies['cli_interface'].display_message.assert_called_with(
            "\nQuiz interrupted by user."
        )


class TestFlashcardQuizzerAppIntegration:
    """Test cases for realistic application workflows and integration scenarios."""
    
    @pytest.fixture
    def mock_dependencies(self):
        """Create mock objects for all FlashcardQuizzerApp dependencies."""
        with patch('main.JSONLoader') as mock_json_loader, \
             patch('main.CLIInterface') as mock_cli_interface, \
             patch('main.MenuSystem') as mock_menu_system:
            
            mock_json_loader_instance = Mock()
            mock_cli_interface_instance = Mock()
            mock_menu_system_instance = Mock()
            
            mock_json_loader.return_value = mock_json_loader_instance
            mock_cli_interface.return_value = mock_cli_interface_instance
            mock_menu_system.return_value = mock_menu_system_instance
            
            yield {
                'json_loader': mock_json_loader_instance,
                'cli_interface': mock_cli_interface_instance,
                'menu_system': mock_menu_system_instance
            }
    
    @pytest.fixture
    def realistic_flashcards(self):
        """Create realistic flashcard set for integration testing."""
        return [
            Flashcard("What is the capital of France?", "Paris"),
            Flashcard("What is 2 + 2?", "4"),
            Flashcard("Who wrote Romeo and Juliet?", "William Shakespeare"),
            Flashcard("What is the chemical symbol for water?", "H2O"),
            Flashcard("What year did World War II end?", "1945")
        ]
    
    @patch('pathlib.Path.exists')
    def test_complete_successful_workflow(self, mock_exists, mock_dependencies, realistic_flashcards):
        """Test complete successful application workflow."""
        mock_exists.return_value = True
        mock_dependencies['json_loader'].load_flashcards.return_value = realistic_flashcards
        
        app = FlashcardQuizzerApp()
        app.run("flashcards.json")
        
        # Verify complete workflow
        mock_dependencies['json_loader'].load_flashcards.assert_called_once_with("flashcards.json")
        mock_dependencies['cli_interface'].display_message.assert_called_with(
            "Successfully loaded 5 flashcards."
        )
        mock_dependencies['menu_system'].run_quiz_menu.assert_called_once_with(realistic_flashcards)
    
    @patch('pathlib.Path.exists')
    def test_error_recovery_workflow(self, mock_exists, mock_dependencies):
        """Test error recovery in realistic workflow."""
        mock_exists.return_value = True
        
        # First call fails, second succeeds
        mock_dependencies['json_loader'].load_flashcards.side_effect = [
            Exception("Network error"),
            [Flashcard("Test", "Answer")]
        ]
        
        app = FlashcardQuizzerApp()
        
        # First run should handle error
        with patch('sys.exit'):
            app.run("test_file.json")
        
        mock_dependencies['cli_interface'].display_error.assert_called_with(
            "Failed to load flashcards: Network error"
        )
        
        # Second run should succeed
        app.run("test_file.json")
        mock_dependencies['menu_system'].run_quiz_menu.assert_called_once()
    
    @patch('pathlib.Path.exists')
    def test_multiple_file_processing_workflow(self, mock_exists, mock_dependencies):
        """Test processing multiple different files in sequence."""
        mock_exists.return_value = True
        
        file1_cards = [Flashcard("Q1", "A1")]
        file2_cards = [Flashcard("Q2", "A2"), Flashcard("Q3", "A3")]
        
        mock_dependencies['json_loader'].load_flashcards.side_effect = [
            file1_cards,
            file2_cards
        ]
        
        app = FlashcardQuizzerApp()
        
        app.run("file1.json")
        app.run("file2.json")
        
        expected_calls = [
            call("file1.json"),
            call("file2.json")
        ]
        mock_dependencies['json_loader'].load_flashcards.assert_has_calls(expected_calls)
        
        expected_message_calls = [
            call("Successfully loaded 1 flashcards."),
            call("Successfully loaded 2 flashcards.")
        ]
        mock_dependencies['cli_interface'].display_message.assert_has_calls(expected_message_calls)
        
        expected_menu_calls = [
            call(file1_cards),
            call(file2_cards)
        ]
        mock_dependencies['menu_system'].run_quiz_menu.assert_has_calls(expected_menu_calls)
    
    @patch('pathlib.Path.exists')
    def test_mixed_success_and_failure_workflow(self, mock_exists, mock_dependencies):
        """Test workflow with mix of successful and failed operations."""
        mock_exists.side_effect = [True, False, True]
        mock_dependencies['json_loader'].load_flashcards.side_effect = [
            [Flashcard("Q1", "A1")],  # Success
            Exception("Should not be called"),  # File not found
            [Flashcard("Q2", "A2")]   # Success
        ]
        
        app = FlashcardQuizzerApp()
        
        # First run - success
        app.run("file1.json")
        mock_dependencies['menu_system'].run_quiz_menu.assert_called_once()
        
        # Second run - file not found
        with patch('sys.exit'):
            app.run("nonexistent.json")
        mock_dependencies['cli_interface'].display_error.assert_called()
        
        # Third run - success
        app.run("file3.json")
        assert mock_dependencies['menu_system'].run_quiz_menu.call_count == 2
    
    @patch('pathlib.Path.exists')
    def test_user_interaction_integration(self, mock_exists, mock_dependencies):
        """Test integration with realistic user interaction patterns."""
        mock_exists.return_value = True
        mock_dependencies['json_loader'].load_flashcards.return_value = [
            Flashcard("Interactive question", "Interactive answer")
        ]
        
        # Simulate user interruption during menu
        mock_dependencies['menu_system'].run_quiz_menu.side_effect = KeyboardInterrupt
        
        app = FlashcardQuizzerApp()
        
        with patch('sys.exit') as mock_exit:
            app.run("interactive.json")
        
        # Verify graceful handling
        mock_dependencies['cli_interface'].display_message.assert_called_with(
            "\nQuiz interrupted by user."
        )
        mock_exit.assert_called_with(0)
    
    @patch('pathlib.Path.exists')
    def test_unicode_content_integration_workflow(self, mock_exists, mock_dependencies):
        """Test complete workflow with unicode content."""
        mock_exists.return_value = True
        unicode_flashcards = [
            Flashcard("¿Cómo estás?", "Bien, gracias"),
            Flashcard("你好吗？", "我很好"),
            Flashcard("Как дела?", "Хорошо")
        ]
        mock_dependencies['json_loader'].load_flashcards.return_value = unicode_flashcards
        
        app = FlashcardQuizzerApp()
        app.run("unicode_cards.json")
        
        mock_dependencies['json_loader'].load_flashcards.assert_called_once_with("unicode_cards.json")
        mock_dependencies['cli_interface'].display_message.assert_called_with(
            "Successfully loaded 3 flashcards."
        )
        mock_dependencies['menu_system'].run_quiz_menu.assert_called_once_with(unicode_flashcards)