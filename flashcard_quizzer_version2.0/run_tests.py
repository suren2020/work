#!/usr/bin/env python3
"""
Test runner script for JSONLoader comprehensive test suite.
Provides different execution options for the test scenarios.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and display results."""
    print(f"\n{'='*60}")
    print(f"RUNNING: {description}")
    print(f"COMMAND: {' '.join(cmd)}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"\n✅ {description} - PASSED")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} - FAILED")
        print(f"Exit code: {e.returncode}")
        return False


def main():
    """Main test runner with different execution options."""
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py [option]")
        print("\nJSONLoader Test Options:")
        print("  all           - Run all JSONLoader tests")
        print("  happy         - Run JSONLoader happy path tests only")
        print("  errors        - Run JSONLoader error condition tests only")
        print("  edges         - Run JSONLoader edge case tests only")
        print("  performance   - Run JSONLoader performance tests only")
        print("  mocking       - Run JSONLoader mocking tests only")
        print("  coverage      - Run JSONLoader tests with coverage report")
        print("  quick         - Run a quick subset of tests")
        print("\nFlashcard Test Options:")
        print("  flashcard         - Run all Flashcard tests")
        print("  flashcard_happy   - Run Flashcard happy path tests")
        print("  flashcard_errors  - Run Flashcard error condition tests") 
        print("  flashcard_edges   - Run Flashcard edge case tests")
        print("  flashcard_performance - Run Flashcard performance tests")
        print("  flashcard_coverage    - Run Flashcard tests with coverage")
        print("\nAdaptiveQuizStrategy Test Options:")
        print("  adaptive          - Run all AdaptiveQuizStrategy tests")
        print("  adaptive_happy    - Run AdaptiveQuizStrategy happy path tests")
        print("  adaptive_errors   - Run AdaptiveQuizStrategy error condition tests")
        print("  adaptive_edges    - Run AdaptiveQuizStrategy edge case tests")
        print("  adaptive_mocking  - Run AdaptiveQuizStrategy mocking tests")
        print("  adaptive_integration - Run AdaptiveQuizStrategy integration tests")
        print("  adaptive_coverage - Run AdaptiveQuizStrategy tests with coverage")
        print("\nFlashcardQuizStrategy Test Options:")
        print("  flashcard_quiz          - Run all FlashcardQuizStrategy tests")
        print("  flashcard_quiz_happy    - Run FlashcardQuizStrategy happy path tests")
        print("  flashcard_quiz_errors   - Run FlashcardQuizStrategy error condition tests")
        print("  flashcard_quiz_edges    - Run FlashcardQuizStrategy edge case tests")
        print("  flashcard_quiz_mocking  - Run FlashcardQuizStrategy mocking tests")
        print("  flashcard_quiz_integration - Run FlashcardQuizStrategy integration tests")
        print("  flashcard_quiz_coverage - Run FlashcardQuizStrategy tests with coverage")
        print("\\nRandomQuizStrategy Test Options:")
        print("  random_quiz          - Run all RandomQuizStrategy tests")
        print("  random_quiz_happy    - Run RandomQuizStrategy happy path tests")
        print("  random_quiz_errors   - Run RandomQuizStrategy error condition tests")
        print("  random_quiz_edges    - Run RandomQuizStrategy edge case tests")
        print("  random_quiz_mocking  - Run RandomQuizStrategy mocking tests")
        print("  random_quiz_integration - Run RandomQuizStrategy integration tests")
        print("  random_quiz_coverage - Run RandomQuizStrategy tests with coverage")
        print("\\nQuizContext Test Options:")
        print("  quiz_context          - Run all QuizContext tests")
        print("  quiz_context_happy    - Run QuizContext happy path tests")
        print("  quiz_context_errors   - Run QuizContext error condition tests")
        print("  quiz_context_edges    - Run QuizContext edge case tests")
        print("  quiz_context_mocking  - Run QuizContext mocking tests")
        print("  quiz_context_integration - Run QuizContext integration tests")
        print("  quiz_context_coverage - Run QuizContext tests with coverage")
        print("\\nQuizStrategy Test Options:")
        print("  quiz_strategy          - Run all QuizStrategy tests")
        print("  quiz_strategy_abc      - Run QuizStrategy ABC interface tests")
        print("  quiz_strategy_compliance - Run QuizStrategy interface compliance tests")
        print("  quiz_strategy_errors   - Run QuizStrategy error condition tests")
        print("  quiz_strategy_edges    - Run QuizStrategy edge case tests")
        print("  quiz_strategy_mocking  - Run QuizStrategy mocking tests")
        print("  quiz_strategy_integration - Run QuizStrategy integration tests")
        print("  quiz_strategy_coverage - Run QuizStrategy tests with coverage")
        print("\\nCLIInterface Test Options:")
        print("  cli_interface          - Run all CLIInterface tests")
        print("  cli_interface_happy    - Run CLIInterface happy path tests")
        print("  cli_interface_errors   - Run CLIInterface error condition tests")
        print("  cli_interface_edges    - Run CLIInterface edge case tests")
        print("  cli_interface_performance - Run CLIInterface performance tests")
        print("  cli_interface_mocking  - Run CLIInterface mocking tests")
        print("  cli_interface_integration - Run CLIInterface integration tests")
        print("  cli_interface_coverage - Run CLIInterface tests with coverage")
        print("\\nMenuSystem Test Options:")
        print("  menu_system          - Run all MenuSystem tests")
        print("  menu_system_happy    - Run MenuSystem happy path tests")
        print("  menu_system_errors   - Run MenuSystem error condition tests")
        print("  menu_system_edges    - Run MenuSystem edge case tests")
        print("  menu_system_performance - Run MenuSystem performance tests")
        print("  menu_system_mocking  - Run MenuSystem mocking tests")
        print("  menu_system_integration - Run MenuSystem integration tests")
        print("  menu_system_coverage - Run MenuSystem tests with coverage")
        print("\\nFlashcardQuizzerApp Test Options:")
        print("  flashcard_app          - Run all FlashcardQuizzerApp tests")
        print("  flashcard_app_happy    - Run FlashcardQuizzerApp happy path tests")
        print("  flashcard_app_errors   - Run FlashcardQuizzerApp error condition tests")
        print("  flashcard_app_edges    - Run FlashcardQuizzerApp edge case tests")
        print("  flashcard_app_performance - Run FlashcardQuizzerApp performance tests")
        print("  flashcard_app_mocking  - Run FlashcardQuizzerApp mocking tests")
        print("  flashcard_app_integration - Run FlashcardQuizzerApp integration tests")
        print("  flashcard_app_coverage - Run FlashcardQuizzerApp tests with coverage")
        sys.exit(1)
    
    option = sys.argv[1].lower()
    base_cmd = [sys.executable, "-m", "pytest", "tests/test_json_loader.py"]
    
    test_commands = {
        "all": (
            base_cmd + ["-v"],
            "All JSONLoader Tests"
        ),
        "happy": (
            base_cmd + ["::TestJSONLoaderHappyPath", "-v"],
            "Happy Path Tests"
        ),
        "errors": (
            base_cmd + ["::TestJSONLoaderErrorConditions", "-v"],
            "Error Condition Tests"
        ),
        "edges": (
            base_cmd + ["::TestJSONLoaderEdgeCases", "-v"],
            "Edge Case Tests"
        ),
        "performance": (
            base_cmd + ["::TestJSONLoaderPerformance", "-v"],
            "Performance Tests"
        ),
        "mocking": (
            base_cmd + ["::TestJSONLoaderMocking", "-v"],
            "Mocking Tests"
        ),
        "coverage": (
            base_cmd + ["--cov=src.data.json_loader", "--cov-report=term-missing", "--cov-report=html", "-v"],
            "Tests with Coverage Report"
        ),
        "flashcard": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard.py", "-v"],
            "All Flashcard Tests"
        ),
        "flashcard_happy": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard.py::TestFlashcardHappyPath", "-v"],
            "Flashcard Happy Path Tests"
        ),
        "flashcard_errors": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard.py::TestFlashcardErrorConditions", "-v"],
            "Flashcard Error Condition Tests"
        ),
        "flashcard_edges": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard.py::TestFlashcardEdgeCases", "-v"],
            "Flashcard Edge Case Tests"
        ),
        "flashcard_performance": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard.py::TestFlashcardPerformance", "-v"],
            "Flashcard Performance Tests"
        ),
        "flashcard_coverage": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard.py", "--cov=src.models.flashcard", "--cov-report=term-missing", "--cov-report=html", "-v"],
            "Flashcard Tests with Coverage"
        ),
        "adaptive": (
            [sys.executable, "-m", "pytest", "tests/test_adaptive_quiz_strategy.py", "-v"],
            "All AdaptiveQuizStrategy Tests"
        ),
        "adaptive_happy": (
            [sys.executable, "-m", "pytest", "tests/test_adaptive_quiz_strategy.py::TestAdaptiveQuizStrategyHappyPath", "-v"],
            "AdaptiveQuizStrategy Happy Path Tests"
        ),
        "adaptive_errors": (
            [sys.executable, "-m", "pytest", "tests/test_adaptive_quiz_strategy.py::TestAdaptiveQuizStrategyErrorConditions", "-v"],
            "AdaptiveQuizStrategy Error Condition Tests"
        ),
        "adaptive_edges": (
            [sys.executable, "-m", "pytest", "tests/test_adaptive_quiz_strategy.py::TestAdaptiveQuizStrategyEdgeCases", "-v"],
            "AdaptiveQuizStrategy Edge Case Tests"
        ),
        "adaptive_mocking": (
            [sys.executable, "-m", "pytest", "tests/test_adaptive_quiz_strategy.py::TestAdaptiveQuizStrategyMocking", "-v"],
            "AdaptiveQuizStrategy Mocking Tests"
        ),
        "adaptive_integration": (
            [sys.executable, "-m", "pytest", "tests/test_adaptive_quiz_strategy.py::TestAdaptiveQuizStrategyIntegration", "-v"],
            "AdaptiveQuizStrategy Integration Tests"
        ),
        "adaptive_coverage": (
            [sys.executable, "-m", "pytest", "tests/test_adaptive_quiz_strategy.py", "--cov=src.quiz.strategies.adaptive_quiz_strategy", "--cov-report=term-missing", "--cov-report=html", "-v"],
            "AdaptiveQuizStrategy Tests with Coverage"
        ),
        "flashcard_quiz": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard_quiz_strategy.py", "-v"],
            "All FlashcardQuizStrategy Tests"
        ),
        "flashcard_quiz_happy": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard_quiz_strategy.py::TestFlashcardQuizStrategyHappyPath", "-v"],
            "FlashcardQuizStrategy Happy Path Tests"
        ),
        "flashcard_quiz_errors": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard_quiz_strategy.py::TestFlashcardQuizStrategyErrorConditions", "-v"],
            "FlashcardQuizStrategy Error Condition Tests"
        ),
        "flashcard_quiz_edges": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard_quiz_strategy.py::TestFlashcardQuizStrategyEdgeCases", "-v"],
            "FlashcardQuizStrategy Edge Case Tests"
        ),
        "flashcard_quiz_mocking": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard_quiz_strategy.py::TestFlashcardQuizStrategyMocking", "-v"],
            "FlashcardQuizStrategy Mocking Tests"
        ),
        "flashcard_quiz_integration": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard_quiz_strategy.py::TestFlashcardQuizStrategyIntegration", "-v"],
            "FlashcardQuizStrategy Integration Tests"
        ),
        "flashcard_quiz_coverage": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard_quiz_strategy.py", "--cov=src.quiz.strategies.flashcard_quiz_strategy", "--cov-report=term-missing", "--cov-report=html", "-v"],
            "FlashcardQuizStrategy Tests with Coverage"
        ),
        "random_quiz": (
            [sys.executable, "-m", "pytest", "tests/test_random_quiz_strategy.py", "-v"],
            "All RandomQuizStrategy Tests"
        ),
        "random_quiz_happy": (
            [sys.executable, "-m", "pytest", "tests/test_random_quiz_strategy.py::TestRandomQuizStrategyHappyPath", "-v"],
            "RandomQuizStrategy Happy Path Tests"
        ),
        "random_quiz_errors": (
            [sys.executable, "-m", "pytest", "tests/test_random_quiz_strategy.py::TestRandomQuizStrategyErrorConditions", "-v"],
            "RandomQuizStrategy Error Condition Tests"
        ),
        "random_quiz_edges": (
            [sys.executable, "-m", "pytest", "tests/test_random_quiz_strategy.py::TestRandomQuizStrategyEdgeCases", "-v"],
            "RandomQuizStrategy Edge Case Tests"
        ),
        "random_quiz_mocking": (
            [sys.executable, "-m", "pytest", "tests/test_random_quiz_strategy.py::TestRandomQuizStrategyMocking", "-v"],
            "RandomQuizStrategy Mocking Tests"
        ),
        "random_quiz_integration": (
            [sys.executable, "-m", "pytest", "tests/test_random_quiz_strategy.py::TestRandomQuizStrategyIntegration", "-v"],
            "RandomQuizStrategy Integration Tests"
        ),
        "random_quiz_coverage": (
            [sys.executable, "-m", "pytest", "tests/test_random_quiz_strategy.py", "--cov=src.quiz.strategies.random_quiz_strategy", "--cov-report=term-missing", "--cov-report=html", "-v"],
            "RandomQuizStrategy Tests with Coverage"
        ),
        "quiz_context": (
            [sys.executable, "-m", "pytest", "tests/test_quiz_context.py", "-v"],
            "All QuizContext Tests"
        ),
        "quiz_context_happy": (
            [sys.executable, "-m", "pytest", "tests/test_quiz_context.py::TestQuizContextHappyPath", "-v"],
            "QuizContext Happy Path Tests"
        ),
        "quiz_context_errors": (
            [sys.executable, "-m", "pytest", "tests/test_quiz_context.py::TestQuizContextErrorConditions", "-v"],
            "QuizContext Error Condition Tests"
        ),
        "quiz_context_edges": (
            [sys.executable, "-m", "pytest", "tests/test_quiz_context.py::TestQuizContextEdgeCases", "-v"],
            "QuizContext Edge Case Tests"
        ),
        "quiz_context_mocking": (
            [sys.executable, "-m", "pytest", "tests/test_quiz_context.py::TestQuizContextMocking", "-v"],
            "QuizContext Mocking Tests"
        ),
        "quiz_context_integration": (
            [sys.executable, "-m", "pytest", "tests/test_quiz_context.py::TestQuizContextIntegration", "-v"],
            "QuizContext Integration Tests"
        ),
        "quiz_context_coverage": (
            [sys.executable, "-m", "pytest", "tests/test_quiz_context.py", "--cov=src.quiz.quiz_context", "--cov-report=term-missing", "--cov-report=html", "-v"],
            "QuizContext Tests with Coverage"
        ),
        "quiz_strategy": (
            [sys.executable, "-m", "pytest", "tests/test_quiz_strategy.py", "-v"],
            "All QuizStrategy Tests"
        ),
        "quiz_strategy_abc": (
            [sys.executable, "-m", "pytest", "tests/test_quiz_strategy.py::TestQuizStrategyAbstractBaseClass", "-v"],
            "QuizStrategy ABC Interface Tests"
        ),
        "quiz_strategy_compliance": (
            [sys.executable, "-m", "pytest", "tests/test_quiz_strategy.py::TestQuizStrategyInterfaceCompliance", "-v"],
            "QuizStrategy Interface Compliance Tests"
        ),
        "quiz_strategy_errors": (
            [sys.executable, "-m", "pytest", "tests/test_quiz_strategy.py::TestQuizStrategyErrorConditions", "-v"],
            "QuizStrategy Error Condition Tests"
        ),
        "quiz_strategy_edges": (
            [sys.executable, "-m", "pytest", "tests/test_quiz_strategy.py::TestQuizStrategyEdgeCases", "-v"],
            "QuizStrategy Edge Case Tests"
        ),
        "quiz_strategy_mocking": (
            [sys.executable, "-m", "pytest", "tests/test_quiz_strategy.py::TestQuizStrategyMocking", "-v"],
            "QuizStrategy Mocking Tests"
        ),
        "quiz_strategy_integration": (
            [sys.executable, "-m", "pytest", "tests/test_quiz_strategy.py::TestQuizStrategyIntegration", "-v"],
            "QuizStrategy Integration Tests"
        ),
        "quiz_strategy_coverage": (
            [sys.executable, "-m", "pytest", "tests/test_quiz_strategy.py", "--cov=src.quiz.quiz_strategy", "--cov-report=term-missing", "--cov-report=html", "-v"],
            "QuizStrategy Tests with Coverage"
        ),
        "cli_interface": (
            [sys.executable, "-m", "pytest", "tests/test_cli_interface.py", "-v"],
            "All CLIInterface Tests"
        ),
        "cli_interface_happy": (
            [sys.executable, "-m", "pytest", "tests/test_cli_interface.py::TestCLIInterfaceHappyPath", "-v"],
            "CLIInterface Happy Path Tests"
        ),
        "cli_interface_errors": (
            [sys.executable, "-m", "pytest", "tests/test_cli_interface.py::TestCLIInterfaceErrorConditions", "-v"],
            "CLIInterface Error Condition Tests"
        ),
        "cli_interface_edges": (
            [sys.executable, "-m", "pytest", "tests/test_cli_interface.py::TestCLIInterfaceEdgeCases", "-v"],
            "CLIInterface Edge Case Tests"
        ),
        "cli_interface_performance": (
            [sys.executable, "-m", "pytest", "tests/test_cli_interface.py::TestCLIInterfacePerformance", "-v"],
            "CLIInterface Performance Tests"
        ),
        "cli_interface_mocking": (
            [sys.executable, "-m", "pytest", "tests/test_cli_interface.py::TestCLIInterfaceMocking", "-v"],
            "CLIInterface Mocking Tests"
        ),
        "cli_interface_integration": (
            [sys.executable, "-m", "pytest", "tests/test_cli_interface.py::TestCLIInterfaceIntegration", "-v"],
            "CLIInterface Integration Tests"
        ),
        "cli_interface_coverage": (
            [sys.executable, "-m", "pytest", "tests/test_cli_interface.py", "--cov=src.ui.cli_interface", "--cov-report=term-missing", "--cov-report=html", "-v"],
            "CLIInterface Tests with Coverage"
        ),
        "menu_system": (
            [sys.executable, "-m", "pytest", "tests/test_menu_system.py", "-v"],
            "All MenuSystem Tests"
        ),
        "menu_system_happy": (
            [sys.executable, "-m", "pytest", "tests/test_menu_system.py::TestMenuSystemHappyPath", "-v"],
            "MenuSystem Happy Path Tests"
        ),
        "menu_system_errors": (
            [sys.executable, "-m", "pytest", "tests/test_menu_system.py::TestMenuSystemErrorConditions", "-v"],
            "MenuSystem Error Condition Tests"
        ),
        "menu_system_edges": (
            [sys.executable, "-m", "pytest", "tests/test_menu_system.py::TestMenuSystemEdgeCases", "-v"],
            "MenuSystem Edge Case Tests"
        ),
        "menu_system_performance": (
            [sys.executable, "-m", "pytest", "tests/test_menu_system.py::TestMenuSystemPerformance", "-v"],
            "MenuSystem Performance Tests"
        ),
        "menu_system_mocking": (
            [sys.executable, "-m", "pytest", "tests/test_menu_system.py::TestMenuSystemMocking", "-v"],
            "MenuSystem Mocking Tests"
        ),
        "menu_system_integration": (
            [sys.executable, "-m", "pytest", "tests/test_menu_system.py::TestMenuSystemIntegration", "-v"],
            "MenuSystem Integration Tests"
        ),
        "menu_system_coverage": (
            [sys.executable, "-m", "pytest", "tests/test_menu_system.py", "--cov=src.ui.menu_system", "--cov-report=term-missing", "--cov-report=html", "-v"],
            "MenuSystem Tests with Coverage"
        ),
        "flashcard_app": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard_quizzer_app.py", "-v"],
            "All FlashcardQuizzerApp Tests"
        ),
        "flashcard_app_happy": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard_quizzer_app.py::TestFlashcardQuizzerAppHappyPath", "-v"],
            "FlashcardQuizzerApp Happy Path Tests"
        ),
        "flashcard_app_errors": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard_quizzer_app.py::TestFlashcardQuizzerAppErrorConditions", "-v"],
            "FlashcardQuizzerApp Error Condition Tests"
        ),
        "flashcard_app_edges": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard_quizzer_app.py::TestFlashcardQuizzerAppEdgeCases", "-v"],
            "FlashcardQuizzerApp Edge Case Tests"
        ),
        "flashcard_app_performance": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard_quizzer_app.py::TestFlashcardQuizzerAppPerformance", "-v"],
            "FlashcardQuizzerApp Performance Tests"
        ),
        "flashcard_app_mocking": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard_quizzer_app.py::TestFlashcardQuizzerAppMocking", "-v"],
            "FlashcardQuizzerApp Mocking Tests"
        ),
        "flashcard_app_integration": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard_quizzer_app.py::TestFlashcardQuizzerAppIntegration", "-v"],
            "FlashcardQuizzerApp Integration Tests"
        ),
        "flashcard_app_coverage": (
            [sys.executable, "-m", "pytest", "tests/test_flashcard_quizzer_app.py", "--cov=main", "--cov-report=term-missing", "--cov-report=html", "-v"],
            "FlashcardQuizzerApp Tests with Coverage"
        ),
        "quick": (
            [sys.executable, "-m", "pytest", 
             "tests/test_json_loader.py::TestJSONLoaderHappyPath::test_load_flashcards_with_valid_array_format_returns_flashcard_objects",
             "tests/test_json_loader.py::TestJSONLoaderErrorConditions::test_load_flashcards_with_nonexistent_file_raises_file_not_found_error",
             "tests/test_json_loader.py::TestJSONLoaderEdgeCases::test_load_flashcards_with_single_flashcard_returns_one_item",
             "-v"],
            "Quick Test Subset"
        )
    }
    
    if option not in test_commands:
        print(f"❌ Unknown option: {option}")
        print("Valid options: " + ", ".join(test_commands.keys()))
        sys.exit(1)
    
    cmd, description = test_commands[option]
    
    # Verify test file exists
    test_file = Path("tests/test_json_loader.py")
    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        sys.exit(1)
    
    # Run the tests
    success = run_command(cmd, description)
    
    if option == "coverage" and success:
        print(f"\n📊 Coverage report generated in: htmlcov/index.html")
        print("Open this file in a browser to view detailed coverage information.")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()