# RandomQuizStrategy Test Scenarios Documentation

## Test Categories Overview

### 1. Happy Path Scenarios (Normal Card Processing)

#### 1.1 Basic Randomized Quiz Execution
- **Test**: `test_execute_quiz_with_normal_flashcards_shuffles_and_processes_correctly`
- **Purpose**: Verify basic quiz execution with flashcard shuffling
- **Input**: List of regular flashcard objects
- **Expected**: random.shuffle called, all cards processed, correct UI method calls

#### 1.2 Original Order Preservation
- **Test**: `test_execute_quiz_preserves_original_flashcard_order`
- **Purpose**: Verify original flashcard list order remains unchanged after quiz
- **Input**: Flashcards with known order
- **Expected**: Original list order preserved after execution

#### 1.3 Perfect Score Scenario
- **Test**: `test_execute_quiz_with_all_correct_answers_returns_empty_missed_list`
- **Purpose**: Verify perfect performance results in no missed cards
- **Input**: All correct user answers
- **Expected**: Empty missed cards list returned, 100% accuracy

#### 1.4 Mixed Performance Tracking
- **Test**: `test_execute_quiz_with_mixed_answers_returns_correct_missed_cards`
- **Purpose**: Verify correct tracking of missed cards with mixed answers
- **Input**: Mix of correct and incorrect answers
- **Expected**: Only incorrect answers tracked in missed cards

#### 1.5 Accuracy Calculation Verification
- **Test**: `test_execute_quiz_calculates_accuracy_percentage_correctly`
- **Purpose**: Verify accuracy percentage is calculated correctly
- **Input**: Known correct/incorrect answer pattern (3/5 = 60%)
- **Expected**: Correct percentage calculation in summary

#### 1.6 Card Index Display Verification
- **Test**: `test_execute_quiz_displays_correct_card_index_and_total`
- **Purpose**: Verify card numbering is displayed correctly during quiz
- **Input**: Multiple flashcards
- **Expected**: Correct index (1-based) and total count passed to UI

#### 1.7 Summary Display Verification
- **Test**: `test_display_quiz_summary_called_with_correct_parameters`
- **Purpose**: Verify summary is displayed with correct statistics
- **Input**: Completed quiz with known results
- **Expected**: Summary called with "Random Quiz", correct statistics

### 2. Error Conditions (Exception Handling and Malformed Responses)

#### 2.1 CLI Interface Exception Propagation
- **Tests**: 
  - `test_execute_quiz_with_cli_interface_get_user_input_raises_exception_propagates_error`
  - `test_execute_quiz_with_cli_interface_display_methods_raise_exception_propagates_error`
- **Purpose**: Verify exceptions from CLI interface are properly handled
- **Input**: CLI methods that raise RuntimeError
- **Expected**: Exceptions propagated to caller

#### 2.2 Flashcard Exception Propagation
- **Test**: `test_execute_quiz_with_flashcard_matches_answer_raises_exception_propagates_error`
- **Purpose**: Verify exceptions from flashcard methods are properly handled
- **Input**: Flashcard.matches_answer that raises ValueError
- **Expected**: Exception propagated to caller

#### 2.3 Empty User Input Handling
- **Test**: `test_execute_quiz_with_empty_user_input_handles_correctly`
- **Purpose**: Verify empty user input is treated as incorrect answer
- **Input**: Empty string responses from user
- **Expected**: All cards marked as missed

#### 2.4 Very Long Input Handling
- **Test**: `test_execute_quiz_with_very_long_user_input_handles_correctly`
- **Purpose**: Verify very long user input doesn't break the system
- **Input**: 10,000 character user response
- **Expected**: Response handled gracefully (marked incorrect)

#### 2.5 Unicode Input Support
- **Test**: `test_execute_quiz_with_unicode_user_input_handles_correctly`
- **Purpose**: Verify unicode characters in user input work correctly
- **Input**: Unicode characters in answers (Chinese characters)
- **Expected**: Correct matching with unicode content

#### 2.6 Special Character Support
- **Test**: `test_execute_quiz_with_special_characters_in_user_input_handles_correctly`
- **Purpose**: Verify special characters in user input work correctly
- **Input**: Special symbols and punctuation
- **Expected**: Correct matching with special characters

### 3. Edge Cases (Boundary Conditions and Special Situations)

#### 3.1 Empty Input Handling
- **Test**: `test_execute_quiz_with_empty_flashcard_list_handles_gracefully`
- **Purpose**: Verify empty flashcard list is handled gracefully
- **Input**: Empty list of flashcards
- **Expected**: No crashes, proper summary display with 0 cards

#### 3.2 Single Card Processing
- **Test**: `test_execute_quiz_with_single_flashcard_works_correctly`
- **Purpose**: Verify single flashcard quiz works correctly
- **Input**: List with exactly one flashcard
- **Expected**: Proper processing and UI interaction

#### 3.3 Duplicate Card Handling
- **Test**: `test_execute_quiz_with_duplicate_flashcards_handles_correctly`
- **Purpose**: Verify duplicate flashcards don't cause issues
- **Input**: Multiple instances of same flashcard
- **Expected**: Duplicates handled correctly in missed list

#### 3.4 Very Large Content Handling
- **Test**: `test_execute_quiz_with_very_large_flashcard_content_handles_correctly`
- **Purpose**: Verify large flashcard content is handled correctly
- **Input**: Flashcards with 5,000+ character content
- **Expected**: Content displayed and processed correctly

#### 3.5 Division by Zero Prevention
- **Test**: `test_execute_quiz_accuracy_calculation_with_zero_cards_handles_division_by_zero`
- **Purpose**: Verify accuracy calculation doesn't crash with zero cards
- **Input**: Empty flashcard list
- **Expected**: Graceful handling of 0/0 calculation

#### 3.6 Whitespace-Only Input Handling
- **Test**: `test_execute_quiz_with_whitespace_only_user_input_handles_correctly`
- **Purpose**: Verify whitespace-only input is handled correctly
- **Input**: User responses with only spaces/tabs/newlines
- **Expected**: Treated as answers, processed by flashcard logic

#### 3.7 Randomization Verification
- **Test**: `test_execute_quiz_randomization_produces_different_orders`
- **Purpose**: Verify randomization actually produces different card orders
- **Input**: Multiple quiz runs with same flashcards
- **Expected**: Different display orders across multiple executions

#### 3.8 Large Dataset Performance
- **Test**: `test_execute_quiz_with_very_large_card_set_handles_correctly`
- **Purpose**: Verify large datasets are processed efficiently
- **Input**: 100 flashcards
- **Expected**: Completion within reasonable time (< 2 seconds)

### 4. Mocking Tests (Internal Behavior Verification)

#### 4.1 Randomization Method Verification
- **Test**: `test_execute_quiz_calls_random_shuffle_exactly_once`
- **Purpose**: Verify random.shuffle is called exactly once with correct data
- **Input**: Normal flashcards with mocked shuffle
- **Expected**: shuffle called once with flashcard copy

#### 4.2 Flashcard Interaction Verification
- **Test**: `test_execute_quiz_calls_each_flashcard_matches_answer_exactly_once`
- **Purpose**: Verify each flashcard's matches_answer is called exactly once
- **Input**: Mocked flashcards
- **Expected**: matches_answer called once per flashcard with user input

#### 4.3 CLI Display Method Verification
- **Test**: `test_execute_quiz_calls_all_required_cli_interface_methods`
- **Purpose**: Verify all required CLI methods are called
- **Input**: Mocked CLI interface
- **Expected**: All display methods called with correct counts

#### 4.4 Summary Method Parameter Verification
- **Test**: `test_display_quiz_summary_receives_correct_missed_cards_list`
- **Purpose**: Verify summary receives correct missed cards
- **Input**: Quiz with known missed cards
- **Expected**: Summary called with exact missed cards list

### 5. Integration Tests (Realistic Workflow Testing)

#### 5.1 Complete Workflow Simulation
- **Test**: `test_random_quiz_complete_workflow_with_realistic_scenario`
- **Purpose**: Test complete random quiz workflow with realistic user interaction
- **Input**: Mixed flashcards, varied user responses (70% accuracy)
- **Expected**: Proper execution flow, correct missed card tracking, accurate summary

#### 5.2 Performance with Realistic Dataset
- **Test**: `test_random_quiz_performance_with_realistic_dataset`
- **Purpose**: Test performance with realistic flashcard deck size
- **Input**: 50 flashcards with 70% accuracy simulation
- **Expected**: Completion within 2 seconds, correct statistics

#### 5.3 Multi-Type Flashcard Integration
- **Test**: `test_random_quiz_with_different_flashcard_types_integration`
- **Purpose**: Test integration with different types of flashcard content
- **Input**: Mix of simple, unicode, math, long, and special character flashcards
- **Expected**: All types processed correctly, proper feedback for each

## Test Execution Commands

### Run All RandomQuizStrategy Tests
```bash
python -m pytest tests/test_random_quiz_strategy.py -v
```

### Run Specific Test Categories
```bash
# Happy path tests
python -m pytest tests/test_random_quiz_strategy.py::TestRandomQuizStrategyHappyPath -v

# Error condition tests
python -m pytest tests/test_random_quiz_strategy.py::TestRandomQuizStrategyErrorConditions -v

# Edge case tests
python -m pytest tests/test_random_quiz_strategy.py::TestRandomQuizStrategyEdgeCases -v

# Mocking tests
python -m pytest tests/test_random_quiz_strategy.py::TestRandomQuizStrategyMocking -v

# Integration tests
python -m pytest tests/test_random_quiz_strategy.py::TestRandomQuizStrategyIntegration -v
```

### Run with Coverage
```bash
python -m pytest tests/test_random_quiz_strategy.py --cov=src.quiz.strategies.random_quiz_strategy --cov-report=html
```

### Using Test Runner Script
```bash
# All tests
python run_tests.py random_quiz

# Specific categories
python run_tests.py random_quiz_happy
python run_tests.py random_quiz_errors
python run_tests.py random_quiz_edges
python run_tests.py random_quiz_mocking
python run_tests.py random_quiz_integration

# With coverage
python run_tests.py random_quiz_coverage
```

## Mock Strategy

### Random Module Mocking
Random functionality is mocked for predictable testing:
- `random.shuffle()` - For controlling card order in tests
- Verification that shuffling occurs exactly once per quiz
- Testing with and without shuffle to verify randomization behavior

### CLI Interface Mocking
All CLI interface methods are mocked to isolate RandomQuizStrategy logic:
- `display_message()` - For intro and transition messages
- `display_card_front()` - For flashcard presentation with index/total
- `get_user_input()` - For simulating user responses
- `display_correct_feedback()` / `display_incorrect_feedback()` - For response feedback
- `display_separator()` - For UI formatting between cards
- `display_quiz_summary()` - For final results display

### Flashcard Mocking
Flashcard behavior is mocked when testing internal logic:
- `matches_answer()` method for testing answer evaluation
- Card properties (`front`, `back`) for display verification
- Various content types (normal, unicode, special characters)

### Test Data Fixtures
Comprehensive fixtures provide different flashcard types:
- `normal_flashcards`: Standard text-based flashcards
- `unicode_flashcards`: International characters and emojis
- `large_content_flashcards`: Very long content for stress testing
- `single_flashcard`: Single card for boundary testing
- `empty_flashcards`: Empty list for edge case testing

## Expected Test Results

- **Total Tests**: 31 comprehensive test methods
- **Coverage**: 100% line and branch coverage of RandomQuizStrategy class
- **Performance**: All tests complete within reasonable time limits
- **Error Handling**: All error conditions properly tested and verified
- **Mock Verification**: All external interactions properly mocked and verified
- **Randomization**: Multiple execution verification to ensure shuffle works

## Key Testing Features

### Comprehensive Error Handling
- Exception propagation from dependencies (CLI, flashcards, random module)
- Graceful handling of malformed input (empty, whitespace, unicode)
- Edge case boundary condition testing

### Performance Validation
- Large dataset processing verification (100+ flashcards)
- Time-based performance assertions (<2 seconds for 100 cards)
- Memory efficiency with realistic workloads

### Behavioral Verification
- Randomized quiz execution logic
- Original list preservation during shuffling
- Correct missed card tracking
- Accurate percentage calculation
- Proper UI method call sequencing

### Randomization Testing
- Verification that random.shuffle is called
- Testing that multiple executions produce different orders
- Control over randomization for predictable testing
- Performance testing with large randomized datasets

### Integration Testing
- Complete workflow validation
- Realistic user interaction patterns
- Multi-type flashcard content handling
- End-to-end randomized quiz validation

The test suite provides enterprise-grade validation ensuring the RandomQuizStrategy class functions correctly under all conditions, maintains performance standards, properly implements randomization, and integrates seamlessly with the broader flashcard quiz system.