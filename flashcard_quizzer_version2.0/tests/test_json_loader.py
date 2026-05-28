"""
Comprehensive test suite for JSONLoader class.
Tests happy path scenarios, error conditions, edge cases, and performance.
"""

import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open

from src.data.json_loader import JSONLoader
from src.models.flashcard import Flashcard


class TestJSONLoaderFixtures:
    """Test fixtures for JSONLoader testing."""
    
    @pytest.fixture
    def json_loader(self):
        """Create a JSONLoader instance for testing."""
        return JSONLoader()
    
    @pytest.fixture
    def valid_array_data(self):
        """Valid flashcard data in array format."""
        return [
            {"front": "What is Python?", "back": "Programming language"},
            {"front": "What is 2+2?", "back": "4"},
            {"front": "Capital of France?", "back": "Paris"}
        ]
    
    @pytest.fixture
    def valid_object_data(self):
        """Valid flashcard data in object format."""
        return {
            "cards": [
                {"front": "What is Python?", "back": "Programming language"},
                {"front": "What is 2+2?", "back": "4"}
            ]
        }
    
    @pytest.fixture
    def single_card_data(self):
        """Single flashcard data for edge case testing."""
        return [{"front": "Single question", "back": "Single answer"}]
    
    @pytest.fixture
    def large_dataset(self):
        """Large dataset for performance testing."""
        return [
            {"front": f"Question {i}", "back": f"Answer {i}"}
            for i in range(1, 1001)
        ]
    
    @pytest.fixture
    def temp_json_file(self):
        """Create a temporary JSON file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            yield f
        # Cleanup
        Path(f.name).unlink(missing_ok=True)


class TestJSONLoaderHappyPath(TestJSONLoaderFixtures):
    """Happy path test scenarios for normal file processing."""
    
    def test_load_flashcards_with_valid_array_format_returns_flashcard_objects(
        self, json_loader, valid_array_data, temp_json_file
    ):
        """Test loading valid array format JSON returns correct Flashcard objects."""
        # Arrange
        json.dump(valid_array_data, temp_json_file)
        temp_json_file.flush()
        
        # Act
        flashcards = json_loader.load_flashcards(temp_json_file.name)
        
        # Assert
        assert len(flashcards) == 3
        assert all(isinstance(card, Flashcard) for card in flashcards)
        assert flashcards[0].front == "What is Python?"
        assert flashcards[0].back == "Programming language"
        assert flashcards[1].front == "What is 2+2?"
        assert flashcards[1].back == "4"
        assert flashcards[2].front == "Capital of France?"
        assert flashcards[2].back == "Paris"
    
    def test_load_flashcards_with_valid_object_format_returns_flashcard_objects(
        self, json_loader, valid_object_data, temp_json_file
    ):
        """Test loading valid object format JSON returns correct Flashcard objects."""
        # Arrange
        json.dump(valid_object_data, temp_json_file)
        temp_json_file.flush()
        
        # Act
        flashcards = json_loader.load_flashcards(temp_json_file.name)
        
        # Assert
        assert len(flashcards) == 2
        assert all(isinstance(card, Flashcard) for card in flashcards)
        assert flashcards[0].front == "What is Python?"
        assert flashcards[0].back == "Programming language"
        assert flashcards[1].front == "What is 2+2?"
        assert flashcards[1].back == "4"
    
    def test_load_flashcards_with_whitespace_trims_correctly(
        self, json_loader, temp_json_file
    ):
        """Test that flashcard data with extra whitespace is trimmed correctly."""
        # Arrange
        data_with_whitespace = [
            {"front": "  Whitespace question  ", "back": "  Whitespace answer  "},
            {"front": "\tTab question\t", "back": "\nNewline answer\n"}
        ]
        json.dump(data_with_whitespace, temp_json_file)
        temp_json_file.flush()
        
        # Act
        flashcards = json_loader.load_flashcards(temp_json_file.name)
        
        # Assert
        assert len(flashcards) == 2
        assert flashcards[0].front == "Whitespace question"
        assert flashcards[0].back == "Whitespace answer"
        assert flashcards[1].front == "Tab question"
        assert flashcards[1].back == "Newline answer"
    
    def test_load_flashcards_with_unicode_characters_handles_correctly(
        self, json_loader, temp_json_file
    ):
        """Test loading flashcards with Unicode characters."""
        # Arrange
        unicode_data = [
            {"front": "What is 你好?", "back": "Hello in Chinese"},
            {"front": "Math: ∑", "back": "Summation symbol"},
            {"front": "Emoji test 🎯", "back": "Target emoji"}
        ]
        json.dump(unicode_data, temp_json_file, ensure_ascii=False)
        temp_json_file.flush()
        
        # Act
        flashcards = json_loader.load_flashcards(temp_json_file.name)
        
        # Assert
        assert len(flashcards) == 3
        assert flashcards[0].front == "What is 你好?"
        assert flashcards[1].front == "Math: ∑"
        assert flashcards[2].front == "Emoji test 🎯"


class TestJSONLoaderErrorConditions(TestJSONLoaderFixtures):
    """Error condition test scenarios for incorrect JSON format and file issues."""
    
    def test_load_flashcards_with_nonexistent_file_raises_file_not_found_error(
        self, json_loader
    ):
        """Test that loading a non-existent file raises FileNotFoundError."""
        # Arrange
        nonexistent_path = "/path/that/does/not/exist.json"
        
        # Act & Assert
        with pytest.raises(FileNotFoundError) as exc_info:
            json_loader.load_flashcards(nonexistent_path)
        
        assert "JSON file not found" in str(exc_info.value)
        assert nonexistent_path in str(exc_info.value)
    
    def test_load_flashcards_with_malformed_json_raises_json_decode_error(
        self, json_loader, temp_json_file
    ):
        """Test that malformed JSON raises JSONDecodeError with descriptive message."""
        # Arrange
        temp_json_file.write('{"invalid": json, content}')
        temp_json_file.flush()
        
        # Act & Assert
        with pytest.raises(json.JSONDecodeError) as exc_info:
            json_loader.load_flashcards(temp_json_file.name)
        
        assert "Malformed JSON" in str(exc_info.value)
        assert temp_json_file.name in str(exc_info.value)
    
    def test_load_flashcards_with_invalid_root_type_raises_value_error(
        self, json_loader, temp_json_file
    ):
        """Test that invalid root data type raises ValueError."""
        # Arrange
        json.dump("invalid_root_string", temp_json_file)
        temp_json_file.flush()
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            json_loader.load_flashcards(temp_json_file.name)
        
        assert "must contain either a list of flashcards or an object with 'cards' field" in str(exc_info.value)
        assert "str" in str(exc_info.value)
    
    def test_load_flashcards_with_object_missing_cards_field_raises_value_error(
        self, json_loader, temp_json_file
    ):
        """Test that object format without 'cards' field raises ValueError."""
        # Arrange
        invalid_object = {"flashcards": [{"front": "Q", "back": "A"}]}
        json.dump(invalid_object, temp_json_file)
        temp_json_file.flush()
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            json_loader.load_flashcards(temp_json_file.name)
        
        assert "missing 'cards' field" in str(exc_info.value)
        assert 'Expected format: {"cards": [...]}' in str(exc_info.value)
    
    def test_load_flashcards_with_cards_field_not_list_raises_value_error(
        self, json_loader, temp_json_file
    ):
        """Test that 'cards' field not being a list raises ValueError."""
        # Arrange
        invalid_cards = {"cards": "not_a_list"}
        json.dump(invalid_cards, temp_json_file)
        temp_json_file.flush()
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            json_loader.load_flashcards(temp_json_file.name)
        
        assert "'cards' field must be a list" in str(exc_info.value)
        assert "str" in str(exc_info.value)
    
    def test_load_flashcards_with_invalid_flashcard_data_raises_value_error_with_index(
        self, json_loader, temp_json_file
    ):
        """Test that invalid flashcard data includes index in error message."""
        # Arrange
        invalid_data = [
            {"front": "Valid question", "back": "Valid answer"},
            {"front": "Invalid question"},  # Missing 'back' field
            {"front": "Another question", "back": "Another answer"}
        ]
        json.dump(invalid_data, temp_json_file)
        temp_json_file.flush()
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            json_loader.load_flashcards(temp_json_file.name)
        
        assert "Invalid flashcard data at index 1" in str(exc_info.value)
        assert "missing 'back' field" in str(exc_info.value)
    
    def test_load_flashcards_with_empty_front_field_raises_value_error(
        self, json_loader, temp_json_file
    ):
        """Test that empty front field raises ValueError."""
        # Arrange
        data_with_empty_front = [{"front": "", "back": "Valid answer"}]
        json.dump(data_with_empty_front, temp_json_file)
        temp_json_file.flush()
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            json_loader.load_flashcards(temp_json_file.name)
        
        assert "front must be a non-empty string" in str(exc_info.value)
    
    def test_load_flashcards_with_empty_back_field_raises_value_error(
        self, json_loader, temp_json_file
    ):
        """Test that empty back field raises ValueError."""
        # Arrange
        data_with_empty_back = [{"front": "Valid question", "back": "   "}]
        json.dump(data_with_empty_back, temp_json_file)
        temp_json_file.flush()
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            json_loader.load_flashcards(temp_json_file.name)
        
        assert "back must be a non-empty string" in str(exc_info.value)


class TestJSONLoaderEdgeCases(TestJSONLoaderFixtures):
    """Edge case test scenarios for boundary conditions."""
    
    def test_load_flashcards_with_empty_array_raises_value_error(
        self, json_loader, temp_json_file
    ):
        """Test that empty array raises ValueError."""
        # Arrange
        json.dump([], temp_json_file)
        temp_json_file.flush()
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            json_loader.load_flashcards(temp_json_file.name)
        
        assert "contains no flashcards" in str(exc_info.value)
    
    def test_load_flashcards_with_empty_cards_array_raises_value_error(
        self, json_loader, temp_json_file
    ):
        """Test that object with empty cards array raises ValueError."""
        # Arrange
        empty_cards = {"cards": []}
        json.dump(empty_cards, temp_json_file)
        temp_json_file.flush()
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            json_loader.load_flashcards(temp_json_file.name)
        
        assert "contains no flashcards" in str(exc_info.value)
    
    def test_load_flashcards_with_single_flashcard_returns_one_item(
        self, json_loader, single_card_data, temp_json_file
    ):
        """Test loading single flashcard returns exactly one item."""
        # Arrange
        json.dump(single_card_data, temp_json_file)
        temp_json_file.flush()
        
        # Act
        flashcards = json_loader.load_flashcards(temp_json_file.name)
        
        # Assert
        assert len(flashcards) == 1
        assert isinstance(flashcards[0], Flashcard)
        assert flashcards[0].front == "Single question"
        assert flashcards[0].back == "Single answer"
    
    def test_load_flashcards_with_numeric_values_converts_to_strings(
        self, json_loader, temp_json_file
    ):
        """Test that numeric values are properly converted to strings."""
        # Arrange
        numeric_data = [
            {"front": 123, "back": 456},
            {"front": "Question", "back": 789}
        ]
        json.dump(numeric_data, temp_json_file)
        temp_json_file.flush()
        
        # Act
        flashcards = json_loader.load_flashcards(temp_json_file.name)
        
        # Assert
        assert len(flashcards) == 2
        assert flashcards[0].front == "123"
        assert flashcards[0].back == "456"
        assert flashcards[1].front == "Question"
        assert flashcards[1].back == "789"
    
    def test_load_flashcards_with_null_values_converts_to_string_none(
        self, json_loader, temp_json_file
    ):
        """Test that null values are converted to string 'None'."""
        # Arrange
        null_data = [{"front": "Valid question", "back": None}]
        json.dump(null_data, temp_json_file)
        temp_json_file.flush()
        
        # Act
        flashcards = json_loader.load_flashcards(temp_json_file.name)
        
        # Assert
        # Null values get converted to string "None" by str(None)
        assert len(flashcards) == 1
        assert flashcards[0].front == "Valid question"
        assert flashcards[0].back == "None"
    
    def test_load_flashcards_with_truly_empty_string_raises_value_error(
        self, json_loader, temp_json_file
    ):
        """Test that actual empty string fields raise ValueError."""
        # Arrange
        empty_string_data = [{"front": "Valid question", "back": ""}]
        json.dump(empty_string_data, temp_json_file)
        temp_json_file.flush()
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            json_loader.load_flashcards(temp_json_file.name)
        
        assert "back must be a non-empty string" in str(exc_info.value)


class TestJSONLoaderPerformance(TestJSONLoaderFixtures):
    """Performance test scenarios for large datasets."""
    
    def test_load_flashcards_with_large_dataset_completes_within_reasonable_time(
        self, json_loader, large_dataset, temp_json_file
    ):
        """Test that loading large dataset completes within reasonable time."""
        import time
        
        # Arrange
        json.dump(large_dataset, temp_json_file)
        temp_json_file.flush()
        
        # Act
        start_time = time.time()
        flashcards = json_loader.load_flashcards(temp_json_file.name)
        end_time = time.time()
        
        # Assert
        assert len(flashcards) == 1000
        assert all(isinstance(card, Flashcard) for card in flashcards)
        # Should complete within 2 seconds for 1000 items
        assert (end_time - start_time) < 2.0
    
    def test_load_flashcards_with_large_dataset_maintains_data_integrity(
        self, json_loader, large_dataset, temp_json_file
    ):
        """Test that large dataset maintains data integrity."""
        # Arrange
        json.dump(large_dataset, temp_json_file)
        temp_json_file.flush()
        
        # Act
        flashcards = json_loader.load_flashcards(temp_json_file.name)
        
        # Assert
        assert len(flashcards) == 1000
        # Check first and last items
        assert flashcards[0].front == "Question 1"
        assert flashcards[0].back == "Answer 1"
        assert flashcards[-1].front == "Question 1000"
        assert flashcards[-1].back == "Answer 1000"
        # Check random middle item
        assert flashcards[499].front == "Question 500"
        assert flashcards[499].back == "Answer 500"


class TestJSONLoaderMocking(TestJSONLoaderFixtures):
    """Test scenarios using mocks to isolate dependencies."""
    
    @patch('src.data.json_loader.Path')
    def test_load_flashcards_with_path_exists_check_called(
        self, mock_path, json_loader
    ):
        """Test that Path.exists() is called during file validation."""
        # Arrange
        mock_path_instance = mock_path.return_value
        mock_path_instance.exists.return_value = False
        
        # Act & Assert
        with pytest.raises(FileNotFoundError):
            json_loader.load_flashcards("test.json")
        
        mock_path.assert_called_once_with("test.json")
        mock_path_instance.exists.assert_called_once()
    
    @patch('builtins.open', new_callable=mock_open, read_data='{"cards": []}')
    @patch('src.data.json_loader.Path')
    def test_load_flashcards_with_file_opened_with_correct_encoding(
        self, mock_path, mock_file, json_loader
    ):
        """Test that file is opened with UTF-8 encoding."""
        # Arrange
        mock_path_instance = mock_path.return_value
        mock_path_instance.exists.return_value = True
        
        # Act & Assert
        with pytest.raises(ValueError):  # Empty cards array
            json_loader.load_flashcards("test.json")
        
        mock_file.assert_called_once_with(mock_path_instance, 'r', encoding='utf-8')
    
    @patch('src.data.json_loader.json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.data.json_loader.Path')
    def test_load_flashcards_with_json_load_called_correctly(
        self, mock_path, mock_file, mock_json_load, json_loader
    ):
        """Test that json.load is called with the correct file handle."""
        # Arrange
        mock_path_instance = mock_path.return_value
        mock_path_instance.exists.return_value = True
        mock_json_load.return_value = [{"front": "Q", "back": "A"}]
        
        # Act
        json_loader.load_flashcards("test.json")
        
        # Assert
        mock_json_load.assert_called_once()
        # Verify json.load was called with the file handle
        call_args = mock_json_load.call_args[0]
        assert len(call_args) == 1  # Should be called with one argument (file handle)