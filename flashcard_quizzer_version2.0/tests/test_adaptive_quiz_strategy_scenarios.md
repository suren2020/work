# AdaptiveQuizStrategy Test Scenarios Documentation

## Test Categories Overview

### 1. Happy Path Scenarios (Normal Card Processing)

#### 1.1 Strategy Initialization
- **Test**: `test_adaptive_strategy_initialization_creates_empty_missed_cards_list`
- **Purpose**: Verify proper initialization of AdaptiveQuizStrategy
- **Input**: New AdaptiveQuizStrategy instance
- **Expected**: Empty initial_missed_cards list

#### 1.2 Missed Cards Management
- **Test**: `test_set_initial_missed_cards_stores_cards_correctly`
- **Purpose**: Verify initial missed cards are stored correctly
- **Input**: List of missed flashcard objects
- **Expected**: Cards properly stored in initial_missed_cards

#### 1.3 Quiz Execution Without Review Phase
- **Test**: `test_execute_quiz_with_no_initial_missed_cards_runs_main_quiz_only`
- **Purpose**: Verify quiz runs main phase only when no initial missed cards
- **Input**: Regular flashcards, no initial missed cards
- **Expected**: Main quiz executed, no review phase messages

#### 1.4 Quiz Execution With Review Phase
- **Test**: `test_execute_quiz_with_initial_missed_cards_runs_review_then_main_quiz`
- **Purpose**: Verify quiz runs review phase first when initial missed cards exist
- **Input**: Regular flashcards + initial missed cards
- **Expected**: Review phase executed first, then main quiz

#### 1.5 Perfect Score Scenario
- **Test**: `test_execute_quiz_with_all_correct_answers_returns_empty_missed_list`
- **Purpose**: Verify perfect performance results in no missed cards
- **Input**: All correct user answers
- **Expected**: Empty missed cards list returned

#### 1.6 Mixed Performance Tracking
- **Test**: `test_execute_quiz_with_mixed_answers_returns_correct_missed_cards`
- **Purpose**: Verify correct tracking of missed cards with mixed answers
- **Input**: Mix of correct and incorrect answers
- **Expected**: Only incorrect answers tracked in missed cards

#### 1.7 UI Method Sequence Verification
- **Test**: `test_execute_quiz_calls_display_methods_in_correct_sequence`
- **Purpose**: Verify UI methods are called in proper sequence
- **Input**: Regular quiz execution
- **Expected**: Display methods called in logical order

### 2. Error Conditions (Incorrect Responses and Bad Formats)

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
- **Input**: Flashcard.matches_answer that raises exception
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
- **Expected**: No crashes, proper summary display

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

#### 3.4 Review Phase Duplicate Prevention
- **Test**: `test_execute_quiz_with_review_phase_duplicate_prevention_works_correctly`
- **Purpose**: Verify cards aren't duplicated between review and main phases
- **Input**: Same card in initial missed and main quiz, both answered incorrectly
- **Expected**: Card appears only once in final missed list

#### 3.5 Empty Initial Missed Cards
- **Test**: `test_set_initial_missed_cards_with_empty_list_works_correctly`
- **Purpose**: Verify setting empty initial missed cards works
- **Input**: Empty list for initial missed cards
- **Expected**: Empty list properly stored

#### 3.6 Missed Cards List Replacement
- **Test**: `test_set_initial_missed_cards_replaces_previous_list`
- **Purpose**: Verify new missed cards list replaces previous one
- **Input**: Two different lists of missed cards
- **Expected**: Second list replaces first list completely

#### 3.7 Division by Zero Prevention
- **Test**: `test_execute_quiz_accuracy_calculation_with_zero_cards_handles_division_by_zero`
- **Purpose**: Verify accuracy calculation doesn't crash with zero cards
- **Input**: Empty flashcard list
- **Expected**: 0% accuracy, no division by zero error

#### 3.8 Large Dataset Performance
- **Test**: `test_quiz_card_set_with_very_large_card_set_handles_correctly`
- **Purpose**: Verify large datasets are processed efficiently
- **Input**: 100 flashcards
- **Expected**: Completion within reasonable time (< 5 seconds)

### 4. Mocking Tests (Internal Behavior Verification)

#### 4.1 Method Call Verification
- **Test**: `test_execute_quiz_calls_quiz_card_set_with_correct_parameters`
- **Purpose**: Verify internal method calls use correct parameters
- **Mock**: _quiz_card_set method
- **Expected**: Method called with correct flashcards and phase name

#### 4.2 Two-Phase Execution Verification
- **Test**: `test_execute_quiz_with_initial_missed_cards_calls_quiz_card_set_twice`
- **Purpose**: Verify two-phase execution when initial missed cards exist
- **Mock**: _quiz_card_set method
- **Expected**: Method called twice with different parameters

#### 4.3 Flashcard Interaction Verification
- **Test**: `test_quiz_card_set_calls_flashcard_matches_answer_for_each_card`
- **Purpose**: Verify each flashcard's matches_answer is called
- **Mock**: Flashcard.matches_answer method
- **Expected**: Method called once per flashcard

#### 4.4 Summary Display Verification
- **Test**: `test_display_quiz_summary_called_with_correct_parameters`
- **Purpose**: Verify summary is displayed with correct statistics
- **Mock**: CLI interface display_quiz_summary
- **Expected**: Correct parameters passed to summary display

### 5. Integration Tests (Realistic Workflow Testing)

#### 5.1 Complete Workflow Simulation
- **Test**: `test_adaptive_quiz_complete_workflow_with_realistic_scenario`
- **Purpose**: Test complete adaptive quiz workflow with realistic user interaction
- **Input**: Mixed flashcards, review phase, varied user responses
- **Expected**: Proper phase execution, correct missed card tracking

#### 5.2 Multiple Rounds Simulation
- **Test**: `test_adaptive_quiz_multiple_rounds_simulation`
- **Purpose**: Simulate multiple quiz rounds with adaptive learning
- **Input**: Multiple quiz sessions using previous missed cards
- **Expected**: Progressive improvement simulation, proper missed card carryover

#### 5.3 Performance with Realistic Dataset
- **Test**: `test_adaptive_quiz_performance_with_realistic_dataset`
- **Purpose**: Test performance with realistic flashcard deck size
- **Input**: 50 flashcards with 70% accuracy simulation
- **Expected**: Completion within 3 seconds, correct statistics

## Test Execution Commands

### Run All AdaptiveQuizStrategy Tests
```bash
python -m pytest tests/test_adaptive_quiz_strategy.py -v
```

### Run Specific Test Categories
```bash
# Happy path tests
python -m pytest tests/test_adaptive_quiz_strategy.py::TestAdaptiveQuizStrategyHappyPath -v

# Error condition tests
python -m pytest tests/test_adaptive_quiz_strategy.py::TestAdaptiveQuizStrategyErrorConditions -v

# Edge case tests
python -m pytest tests/test_adaptive_quiz_strategy.py::TestAdaptiveQuizStrategyEdgeCases -v

# Mocking tests
python -m pytest tests/test_adaptive_quiz_strategy.py::TestAdaptiveQuizStrategyMocking -v

# Integration tests
python -m pytest tests/test_adaptive_quiz_strategy.py::TestAdaptiveQuizStrategyIntegration -v
```

### Run with Coverage
```bash
python -m pytest tests/test_adaptive_quiz_strategy.py --cov=src.quiz.strategies.adaptive_quiz_strategy --cov-report=html
```

## Mock Strategy

### CLI Interface Mocking
All CLI interface methods are mocked to isolate AdaptiveQuizStrategy logic:
- `display_message()` - For phase transition messages
- `display_card_front()` - For flashcard presentation
- `get_user_input()` - For simulating user responses
- `display_correct_feedback()` / `display_incorrect_feedback()` - For response feedback
- `display_separator()` - For UI formatting
- `display_quiz_summary()` - For final results display

### Flashcard Mocking
Flashcard behavior is mocked when testing internal logic:
- `matches_answer()` method for testing answer evaluation
- Card properties (`front`, `back`) for display verification

### Internal Method Mocking
Internal methods are mocked to verify call patterns:
- `_quiz_card_set()` for testing execution flow
- `_display_quiz_summary()` for testing parameter passing

## Expected Test Results

- **Total Tests**: 25 comprehensive test methods
- **Coverage**: 100% line and branch coverage of AdaptiveQuizStrategy class
- **Performance**: All tests complete within reasonable time limits
- **Error Handling**: All error conditions properly tested and verified
- **Mock Verification**: All external interactions properly mocked and verified

## Key Testing Features

### Comprehensive Error Handling
- Exception propagation from dependencies
- Graceful handling of malformed input
- Edge case boundary condition testing

### Performance Validation
- Large dataset processing verification
- Time-based performance assertions
- Memory efficiency with realistic workloads

### Behavioral Verification
- Two-phase quiz execution logic
- Duplicate prevention mechanisms
- Accuracy calculation correctness

### Integration Testing
- Multi-round adaptive learning simulation
- Realistic user interaction patterns
- End-to-end workflow validation

The test suite provides enterprise-grade validation ensuring the AdaptiveQuizStrategy class functions correctly under all conditions, maintains performance standards, and integrates properly with the broader flashcard quiz system.