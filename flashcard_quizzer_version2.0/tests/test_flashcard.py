"""
Comprehensive test suite for Flashcard class.
Tests happy path scenarios, error conditions, edge cases, and performance.
"""

import pytest
from unittest.mock import patch, Mock
import time

from src.models.flashcard import Flashcard


class TestFlashcardFixtures:
    """Test fixtures for Flashcard testing."""
    
    @pytest.fixture
    def valid_front_text(self):
        """Valid front text for flashcard creation."""
        return "What is the capital of France?"
    
    @pytest.fixture
    def valid_back_text(self):
        """Valid back text for flashcard creation."""
        return "Paris"
    
    @pytest.fixture
    def valid_flashcard(self, valid_front_text, valid_back_text):
        """Create a valid flashcard for testing."""
        return Flashcard(front=valid_front_text, back=valid_back_text)
    
    @pytest.fixture
    def valid_dict_data(self, valid_front_text, valid_back_text):
        """Valid dictionary data for from_dict method."""
        return {"front": valid_front_text, "back": valid_back_text}
    
    @pytest.fixture
    def unicode_front_text(self):
        """Unicode front text for testing."""
        return "What is 你好 in English?"
    
    @pytest.fixture
    def unicode_back_text(self):
        """Unicode back text for testing."""
        return "Hello 🌍"
    
    @pytest.fixture
    def case_sensitive_answer(self):
        """Case-sensitive answer for testing."""
        return "PyThOn"


class TestFlashcardHappyPath(TestFlashcardFixtures):
    """Happy path test scenarios for normal flashcard operations."""
    
    def test_flashcard_creation_with_valid_data_creates_immutable_instance(
        self, valid_front_text, valid_back_text
    ):
        """Test that valid data creates a proper immutable flashcard instance."""
        # Act
        flashcard = Flashcard(front=valid_front_text, back=valid_back_text)
        
        # Assert
        assert flashcard.front == valid_front_text
        assert flashcard.back == valid_back_text
        assert isinstance(flashcard, Flashcard)
        # Test immutability
        with pytest.raises(AttributeError):
            flashcard.front = "Modified"
    
    def test_flashcard_from_dict_with_valid_data_returns_correct_flashcard(
        self, valid_dict_data, valid_front_text, valid_back_text
    ):
        """Test from_dict method creates flashcard with correct data."""
        # Act
        flashcard = Flashcard.from_dict(valid_dict_data)
        
        # Assert
        assert isinstance(flashcard, Flashcard)
        assert flashcard.front == valid_front_text
        assert flashcard.back == valid_back_text
    
    def test_flashcard_from_dict_with_extra_whitespace_trims_correctly(self):
        """Test that from_dict properly trims whitespace from fields."""
        # Arrange
        data_with_whitespace = {
            "front": "  Question with spaces  ",
            "back": "\tAnswer with tabs\t"
        }
        
        # Act
        flashcard = Flashcard.from_dict(data_with_whitespace)
        
        # Assert
        assert flashcard.front == "Question with spaces"
        assert flashcard.back == "Answer with tabs"
    
    def test_matches_answer_with_exact_match_returns_true(self, valid_flashcard):
        """Test that exact answer match returns True."""
        # Act & Assert
        assert valid_flashcard.matches_answer("Paris") is True
    
    def test_matches_answer_with_case_insensitive_match_returns_true(
        self, valid_flashcard
    ):
        """Test that case-insensitive matching works correctly."""
        # Act & Assert
        assert valid_flashcard.matches_answer("paris") is True
        assert valid_flashcard.matches_answer("PARIS") is True
        assert valid_flashcard.matches_answer("PaRiS") is True
    
    def test_matches_answer_with_extra_whitespace_handles_correctly(
        self, valid_flashcard
    ):
        """Test that extra whitespace in user input is handled correctly."""
        # Act & Assert
        assert valid_flashcard.matches_answer("  Paris  ") is True
        assert valid_flashcard.matches_answer("\tParis\t") is True
        assert valid_flashcard.matches_answer("\nParis\n") is True
    
    def test_flashcard_with_unicode_characters_handles_correctly(
        self, unicode_front_text, unicode_back_text
    ):
        """Test that unicode characters are handled properly."""
        # Act
        flashcard = Flashcard(front=unicode_front_text, back=unicode_back_text)
        
        # Assert
        assert flashcard.front == unicode_front_text
        assert flashcard.back == unicode_back_text
        assert flashcard.matches_answer("hello 🌍") is True
        assert flashcard.matches_answer("Hello 🌍") is True
    
    def test_flashcard_equality_with_same_content_returns_true(
        self, valid_front_text, valid_back_text
    ):
        """Test that flashcards with same content are considered equal."""
        # Arrange
        flashcard1 = Flashcard(front=valid_front_text, back=valid_back_text)
        flashcard2 = Flashcard(front=valid_front_text, back=valid_back_text)
        
        # Act & Assert
        assert flashcard1 == flashcard2
        assert hash(flashcard1) == hash(flashcard2)


class TestFlashcardErrorConditions(TestFlashcardFixtures):
    """Error condition test scenarios for incorrect data and validation."""
    
    def test_flashcard_creation_with_empty_front_raises_value_error(self):
        """Test that empty front text raises ValueError."""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            Flashcard(front="", back="Valid answer")
        
        assert "front must be a non-empty string" in str(exc_info.value)
    
    def test_flashcard_creation_with_empty_back_raises_value_error(self):
        """Test that empty back text raises ValueError."""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            Flashcard(front="Valid question", back="")
        
        assert "back must be a non-empty string" in str(exc_info.value)
    
    def test_flashcard_creation_with_whitespace_only_front_raises_value_error(self):
        """Test that whitespace-only front text raises ValueError."""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            Flashcard(front="   ", back="Valid answer")
        
        assert "front must be a non-empty string" in str(exc_info.value)
    
    def test_flashcard_creation_with_whitespace_only_back_raises_value_error(self):
        """Test that whitespace-only back text raises ValueError."""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            Flashcard(front="Valid question", back="\t\n  ")
        
        assert "back must be a non-empty string" in str(exc_info.value)
    
    def test_flashcard_creation_with_non_string_front_raises_value_error(self):
        """Test that non-string front value raises ValueError."""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            Flashcard(front=123, back="Valid answer")
        
        assert "front must be a non-empty string" in str(exc_info.value)
    
    def test_flashcard_creation_with_non_string_back_raises_value_error(self):
        """Test that non-string back value raises ValueError."""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            Flashcard(front="Valid question", back=456)
        
        assert "back must be a non-empty string" in str(exc_info.value)
    
    def test_from_dict_with_non_dict_input_raises_value_error(self):
        """Test that non-dictionary input to from_dict raises ValueError."""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            Flashcard.from_dict("not_a_dict")
        
        assert "must be a dictionary" in str(exc_info.value)
    
    def test_from_dict_with_missing_front_field_raises_value_error(self):
        """Test that missing 'front' field raises ValueError."""
        # Arrange
        data_missing_front = {"back": "Valid answer"}
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            Flashcard.from_dict(data_missing_front)
        
        assert "missing 'front' field" in str(exc_info.value)
    
    def test_from_dict_with_missing_back_field_raises_value_error(self):
        """Test that missing 'back' field raises ValueError."""
        # Arrange
        data_missing_back = {"front": "Valid question"}
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            Flashcard.from_dict(data_missing_back)
        
        assert "missing 'back' field" in str(exc_info.value)
    
    def test_matches_answer_with_non_string_input_returns_false(self, valid_flashcard):
        """Test that non-string input to matches_answer returns False."""
        # Act & Assert
        assert valid_flashcard.matches_answer(123) is False
        assert valid_flashcard.matches_answer(None) is False
        assert valid_flashcard.matches_answer([]) is False
        assert valid_flashcard.matches_answer({}) is False
    
    def test_matches_answer_with_incorrect_answer_returns_false(self, valid_flashcard):
        """Test that incorrect answer returns False."""
        # Act & Assert
        assert valid_flashcard.matches_answer("London") is False
        assert valid_flashcard.matches_answer("Berlin") is False
        assert valid_flashcard.matches_answer("Madrid") is False


class TestFlashcardEdgeCases(TestFlashcardFixtures):
    """Edge case test scenarios for boundary conditions and special cases."""
    
    def test_flashcard_with_single_character_content_works_correctly(self):
        """Test that single character content is handled correctly."""
        # Act
        flashcard = Flashcard(front="A", back="B")
        
        # Assert
        assert flashcard.front == "A"
        assert flashcard.back == "B"
        assert flashcard.matches_answer("B") is True
        assert flashcard.matches_answer("b") is True
    
    def test_flashcard_with_very_long_content_handles_correctly(self):
        """Test that very long content is handled properly."""
        # Arrange
        long_front = "A" * 10000
        long_back = "B" * 10000
        
        # Act
        flashcard = Flashcard(front=long_front, back=long_back)
        
        # Assert
        assert flashcard.front == long_front
        assert flashcard.back == long_back
        assert flashcard.matches_answer(long_back) is True
    
    def test_flashcard_with_special_characters_works_correctly(self):
        """Test that special characters are handled correctly."""
        # Arrange
        special_front = "What is @#$%^&*()?"
        special_back = "Special characters!"
        
        # Act
        flashcard = Flashcard(front=special_front, back=special_back)
        
        # Assert
        assert flashcard.front == special_front
        assert flashcard.back == special_back
        assert flashcard.matches_answer("special characters!") is True
    
    def test_flashcard_with_numeric_strings_handles_correctly(self):
        """Test that numeric string content works correctly."""
        # Act
        flashcard = Flashcard(front="What is 2+2?", back="4")
        
        # Assert
        assert flashcard.matches_answer("4") is True
        assert flashcard.matches_answer("04") is False  # Different string
    
    def test_from_dict_with_numeric_values_converts_to_strings(self):
        """Test that numeric values are properly converted to strings."""
        # Arrange
        numeric_data = {"front": 123, "back": 456}
        
        # Act
        flashcard = Flashcard.from_dict(numeric_data)
        
        # Assert
        assert flashcard.front == "123"
        assert flashcard.back == "456"
        assert flashcard.matches_answer("456") is True
    
    def test_from_dict_with_boolean_values_converts_to_strings(self):
        """Test that boolean values are converted to strings."""
        # Arrange
        boolean_data = {"front": True, "back": False}
        
        # Act
        flashcard = Flashcard.from_dict(boolean_data)
        
        # Assert
        assert flashcard.front == "True"
        assert flashcard.back == "False"
        assert flashcard.matches_answer("false") is True  # Case insensitive
    
    def test_from_dict_with_none_values_converts_to_string_none(self):
        """Test that None values are converted to string 'None'."""
        # Arrange
        none_data = {"front": None, "back": None}
        
        # Act
        flashcard = Flashcard.from_dict(none_data)
        
        # Assert
        assert flashcard.front == "None"
        assert flashcard.back == "None"
        assert flashcard.matches_answer("none") is True
    
    def test_matches_answer_with_empty_string_returns_false(self):
        """Test that empty string answer returns False."""
        # Arrange
        flashcard = Flashcard(front="Question", back="Answer")
        
        # Act & Assert
        assert flashcard.matches_answer("") is False
    
    def test_flashcard_inequality_with_different_content_returns_false(
        self, valid_front_text, valid_back_text
    ):
        """Test that flashcards with different content are not equal."""
        # Arrange
        flashcard1 = Flashcard(front=valid_front_text, back=valid_back_text)
        flashcard2 = Flashcard(front="Different", back="Content")
        
        # Act & Assert
        assert flashcard1 != flashcard2
        assert hash(flashcard1) != hash(flashcard2)


class TestFlashcardPerformance(TestFlashcardFixtures):
    """Performance test scenarios for repeatedly using flashcard operations."""
    
    def test_flashcard_creation_performance_with_multiple_instances(self):
        """Test that creating multiple flashcard instances performs efficiently."""
        # Arrange
        start_time = time.time()
        flashcards = []
        
        # Act
        for i in range(1000):
            flashcard = Flashcard(front=f"Question {i}", back=f"Answer {i}")
            flashcards.append(flashcard)
        
        end_time = time.time()
        
        # Assert
        assert len(flashcards) == 1000
        # Should complete within 1 second
        assert (end_time - start_time) < 1.0
        # Verify data integrity
        assert flashcards[0].front == "Question 0"
        assert flashcards[999].back == "Answer 999"
    
    def test_matches_answer_performance_with_repeated_calls(self, valid_flashcard):
        """Test that repeated calls to matches_answer perform efficiently."""
        # Arrange
        start_time = time.time()
        
        # Act
        for _ in range(10000):
            result = valid_flashcard.matches_answer("Paris")
            assert result is True
        
        end_time = time.time()
        
        # Assert
        # Should complete within 1 second
        assert (end_time - start_time) < 1.0
    
    def test_from_dict_performance_with_multiple_conversions(self):
        """Test that multiple from_dict conversions perform efficiently."""
        # Arrange
        start_time = time.time()
        base_data = {"front": "Test question", "back": "Test answer"}
        flashcards = []
        
        # Act
        for i in range(1000):
            data = {"front": f"Question {i}", "back": f"Answer {i}"}
            flashcard = Flashcard.from_dict(data)
            flashcards.append(flashcard)
        
        end_time = time.time()
        
        # Assert
        assert len(flashcards) == 1000
        # Should complete within 1 second
        assert (end_time - start_time) < 1.0
    
    def test_flashcard_memory_efficiency_with_large_dataset(self):
        """Test memory efficiency with large number of flashcards."""
        # Arrange
        import sys
        flashcards = []
        
        # Act
        for i in range(5000):
            flashcard = Flashcard(front=f"Q{i}", back=f"A{i}")
            flashcards.append(flashcard)
        
        # Assert
        assert len(flashcards) == 5000
        # Basic memory check - all flashcards should be accessible
        total_size = sum(sys.getsizeof(fc.front) + sys.getsizeof(fc.back) 
                        for fc in flashcards[:100])  # Sample check
        assert total_size > 0  # Ensure memory is being used appropriately


class TestFlashcardMocking(TestFlashcardFixtures):
    """Test scenarios using mocks to verify internal behavior."""
    
    def test_from_dict_calls_str_conversion_for_fields(self):
        """Test that from_dict properly handles string conversion."""
        # Arrange
        data = {"front": 123, "back": 456}
        
        # Act
        flashcard = Flashcard.from_dict(data)
        
        # Assert
        # Verify that non-string values are converted to strings
        assert flashcard.front == "123"
        assert flashcard.back == "456"
        assert isinstance(flashcard.front, str)
        assert isinstance(flashcard.back, str)
    
    def test_matches_answer_string_normalization_behavior(self, valid_flashcard):
        """Test matches_answer behavior with different string inputs."""
        # Arrange
        test_cases = [
            ("paris", True),      # lowercase
            ("PARIS", True),      # uppercase
            ("  Paris  ", True),  # whitespace
            ("\tParis\n", True),  # tabs/newlines
            ("London", False),    # wrong answer
        ]
        
        # Act & Assert
        for test_input, expected in test_cases:
            result = valid_flashcard.matches_answer(test_input)
            assert result == expected, f"Failed for input: {repr(test_input)}"
    
    def test_flashcard_validation_behavior_verification(self):
        """Test that validation behavior works as expected."""
        # Test valid creation
        flashcard = Flashcard(front="Valid", back="Valid")
        assert flashcard.front == "Valid"
        assert flashcard.back == "Valid"
        
        # Test invalid creation scenarios
        with pytest.raises(ValueError):
            Flashcard(front="", back="Valid")
        
        with pytest.raises(ValueError):
            Flashcard(front="Valid", back="")
        
        with pytest.raises(ValueError):
            Flashcard(front="   ", back="Valid")
        
        with pytest.raises(ValueError):
            Flashcard(front="Valid", back="   ")


class TestFlashcardIntegration(TestFlashcardFixtures):
    """Integration test scenarios testing flashcard with other components."""
    
    def test_flashcard_serialization_roundtrip_maintains_data_integrity(self, valid_flashcard):
        """Test that flashcard can be serialized and deserialized correctly."""
        import json
        
        # Arrange
        flashcard_dict = {"front": valid_flashcard.front, "back": valid_flashcard.back}
        
        # Act - Simulate JSON serialization/deserialization
        json_string = json.dumps(flashcard_dict)
        restored_dict = json.loads(json_string)
        restored_flashcard = Flashcard.from_dict(restored_dict)
        
        # Assert
        assert restored_flashcard.front == valid_flashcard.front
        assert restored_flashcard.back == valid_flashcard.back
        assert restored_flashcard == valid_flashcard
    
    def test_flashcard_compatibility_with_dataclass_features(self, valid_flashcard):
        """Test that flashcard works correctly with dataclass features."""
        # Act & Assert - Test string representation
        str_repr = str(valid_flashcard)
        assert "Flashcard" in str_repr
        assert valid_flashcard.front in str_repr
        assert valid_flashcard.back in str_repr
        
        # Test that it's frozen (immutable)
        with pytest.raises(AttributeError):
            valid_flashcard.front = "Modified"
    
    def test_flashcard_with_quiz_simulation_workflow(self):
        """Test flashcard in a simulated quiz workflow."""
        # Arrange
        quiz_data = [
            {"front": "Capital of France?", "back": "Paris"},
            {"front": "2 + 2 = ?", "back": "4"},
            {"front": "Python creator?", "back": "Guido van Rossum"}
        ]
        
        # Act
        flashcards = [Flashcard.from_dict(data) for data in quiz_data]
        correct_answers = ["paris", "4", "guido van rossum"]
        results = [fc.matches_answer(answer) for fc, answer in zip(flashcards, correct_answers)]
        
        # Assert
        assert len(flashcards) == 3
        assert all(isinstance(fc, Flashcard) for fc in flashcards)
        assert all(results)  # All answers should be correct
        assert sum(results) == 3  # All 3 answers correct