"""
Pytest configuration and shared fixtures for all tests.
"""

import pytest
import tempfile
import json
from pathlib import Path


@pytest.fixture(scope="session")
def test_data_dir():
    """Create a temporary directory for test data files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_valid_array_json(test_data_dir):
    """Create a sample valid array format JSON file."""
    data = [
        {"front": "Test question 1", "back": "Test answer 1"},
        {"front": "Test question 2", "back": "Test answer 2"}
    ]
    file_path = test_data_dir / "valid_array.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    return file_path


@pytest.fixture
def sample_valid_object_json(test_data_dir):
    """Create a sample valid object format JSON file."""
    data = {
        "cards": [
            {"front": "Test question 1", "back": "Test answer 1"},
            {"front": "Test question 2", "back": "Test answer 2"}
        ]
    }
    file_path = test_data_dir / "valid_object.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    return file_path


@pytest.fixture
def sample_malformed_json(test_data_dir):
    """Create a sample malformed JSON file."""
    file_path = test_data_dir / "malformed.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('{"invalid": json content}')
    return file_path


@pytest.fixture
def cli_interface():
    """Create a CLIInterface instance for testing."""
    from src.ui.cli_interface import CLIInterface
    return CLIInterface()


@pytest.fixture
def sample_flashcards():
    """Create sample flashcard objects for testing."""
    from src.models.flashcard import Flashcard
    return [
        Flashcard("What is Python?", "A programming language"),
        Flashcard("What is a variable?", "A storage location"),
        Flashcard("What is a function?", "A reusable code block")
    ]


@pytest.fixture
def unicode_flashcards():
    """Create sample flashcard objects with unicode content."""
    from src.models.flashcard import Flashcard
    return [
        Flashcard("¿Cómo estás?", "Bien, gracias"),
        Flashcard("你好吗？", "我很好"),
        Flashcard("Как дела?", "Хорошо")
    ]


@pytest.fixture
def mock_cli_interface():
    """Create a mock CLIInterface for testing."""
    from unittest.mock import Mock
    mock = Mock()
    mock.display_message = Mock()
    mock.display_error = Mock()
    mock.get_user_input = Mock()
    mock.display_card_front = Mock()
    mock.display_correct_feedback = Mock()
    mock.display_incorrect_feedback = Mock()
    mock.display_separator = Mock()
    mock.display_quiz_summary = Mock()
    return mock


@pytest.fixture
def menu_system(mock_cli_interface):
    """Create a MenuSystem instance with mocked CLI interface."""
    from src.ui.menu_system import MenuSystem
    return MenuSystem(mock_cli_interface)


@pytest.fixture
def empty_flashcards():
    """Create an empty flashcards list for testing."""
    return []


@pytest.fixture
def single_flashcard():
    """Create a single flashcard for testing."""
    from src.models.flashcard import Flashcard
    return [Flashcard("Single question", "Single answer")]


@pytest.fixture
def large_flashcard_set():
    """Create a large flashcard set for performance testing."""
    from src.models.flashcard import Flashcard
    return [Flashcard(f"Question {i}", f"Answer {i}") for i in range(1000)]


@pytest.fixture
def mock_quiz_strategy():
    """Create a mock QuizStrategy for testing."""
    from unittest.mock import Mock
    mock = Mock()
    mock.execute_quiz = Mock(return_value=[])
    return mock


@pytest.fixture
def quiz_context(mock_quiz_strategy):
    """Create a QuizContext instance with mocked strategy."""
    from src.quiz.quiz_context import QuizContext
    return QuizContext(mock_quiz_strategy)


@pytest.fixture
def normal_flashcards():
    """Create normal flashcards for testing (alias for sample_flashcards)."""
    from src.models.flashcard import Flashcard
    return [
        Flashcard("What is Python?", "A programming language"),
        Flashcard("What is a variable?", "A storage location"),
        Flashcard("What is a function?", "A reusable code block")
    ]


@pytest.fixture
def alternative_mock_strategy():
    """Create an alternative mock QuizStrategy for testing strategy switching."""
    from unittest.mock import Mock
    mock = Mock()
    mock.execute_quiz = Mock(return_value=[])
    return mock


@pytest.fixture
def valid_concrete_strategy():
    """Create a valid concrete QuizStrategy implementation for testing."""
    from src.quiz.strategies.flashcard_quiz_strategy import FlashcardQuizStrategy
    return FlashcardQuizStrategy()


@pytest.fixture
def mock_concrete_strategy():
    """Create a mock concrete strategy for testing."""
    from unittest.mock import Mock
    from src.quiz.quiz_strategy import QuizStrategy
    mock = Mock(spec=QuizStrategy)
    mock.execute_quiz = Mock(return_value=[])
    return mock


@pytest.fixture
def random_quiz_strategy():
    """Create a RandomQuizStrategy instance for testing."""
    from src.quiz.strategies.random_quiz_strategy import RandomQuizStrategy
    return RandomQuizStrategy()


@pytest.fixture
def large_content_flashcards():
    """Create flashcards with very large content for testing."""
    from src.models.flashcard import Flashcard
    large_front = "A" * 1000  # Very long question
    large_back = "B" * 1000   # Very long answer
    return [Flashcard(large_front, large_back)]