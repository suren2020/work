# CLIInterface Test Scenarios Documentation

## Test Categories Overview

### 1. Happy Path Scenarios (Normal Display and Operations)

#### 1.1 Basic Message Display
- **Test**: `test_display_message_outputs_to_stdout`
- **Purpose**: Verify display_message outputs correctly to stdout
- **Input**: Simple text message
- **Expected**: Message printed to stdout exactly as provided

#### 1.2 Error Message Display
- **Test**: `test_display_error_outputs_to_stderr`
- **Purpose**: Verify display_error outputs correctly to stderr with error prefix
- **Input**: Error message string
- **Expected**: "Error: {message}" printed to stderr

#### 1.3 Basic Card Front Display
- **Test**: `test_display_card_front_with_basic_parameters`
- **Purpose**: Test display_card_front with basic parameters
- **Input**: Front text, card number, total cards
- **Expected**: "Card {number}/{total}: {text}" format

#### 1.4 Card Front Display with Phase
- **Test**: `test_display_card_front_with_phase_name`
- **Purpose**: Test display_card_front with phase name parameter
- **Input**: Front text, card number, total cards, phase name
- **Expected**: "[{phase}] Card {number}/{total}: {text}" format

#### 1.5 User Input Collection
- **Test**: `test_get_user_input_returns_stripped_input`
- **Purpose**: Verify get_user_input returns stripped input
- **Input**: Input with leading/trailing whitespace
- **Expected**: Whitespace stripped from result

#### 1.6 Custom Prompt Input
- **Test**: `test_get_user_input_with_custom_prompt`
- **Purpose**: Test get_user_input with custom prompt
- **Input**: Custom prompt string and user response
- **Expected**: Custom prompt used, response returned

#### 1.7 Correct Answer Feedback
- **Test**: `test_display_correct_feedback_shows_positive_message`
- **Purpose**: Verify display_correct_feedback shows positive message
- **Input**: Method call only
- **Expected**: "Correct" displayed

#### 1.8 Incorrect Answer Feedback
- **Test**: `test_display_incorrect_feedback_shows_correct_answer`
- **Purpose**: Test display_incorrect_feedback shows the correct answer
- **Input**: Correct answer string
- **Expected**: "Incorrect (correct answer: {answer})" format

#### 1.9 Separator Display
- **Test**: `test_display_separator_shows_dashes`
- **Purpose**: Verify display_separator shows proper separator
- **Input**: Method call only
- **Expected**: 40 dashes printed

#### 1.10 Perfect Score Quiz Summary
- **Test**: `test_display_quiz_summary_with_perfect_score`
- **Purpose**: Test display_quiz_summary with perfect score
- **Input**: 100% accuracy, no missed cards
- **Expected**: Perfect score message, complete summary format

#### 1.11 Quiz Summary with Missed Cards
- **Test**: `test_display_quiz_summary_with_missed_cards`
- **Purpose**: Test display_quiz_summary with missed cards
- **Input**: Mixed results with specific missed cards
- **Expected**: Complete summary with missed cards list

### 2. Error Conditions (Incorrect Inputs and Malformed Data)

#### 2.1 None Input to Display Message
- **Test**: `test_display_message_with_none_input_raises_error`
- **Purpose**: Verify display_message with None input raises appropriate error
- **Input**: None as message parameter
- **Expected**: TypeError raised

#### 2.2 None Input to Display Error
- **Test**: `test_display_error_with_none_input_raises_error`
- **Purpose**: Verify display_error with None input raises appropriate error
- **Input**: None as error message parameter
- **Expected**: TypeError raised

#### 2.3 Invalid Card Number Type
- **Test**: `test_display_card_front_with_invalid_card_number_type`
- **Purpose**: Test display_card_front with invalid card number type
- **Input**: String instead of integer for card number
- **Expected**: TypeError raised

#### 2.4 Negative Card Number
- **Test**: `test_display_card_front_with_negative_card_number`
- **Purpose**: Test display_card_front with negative card number
- **Input**: Negative integer for card number
- **Expected**: Displays with negative number (unusual but not breaking)

#### 2.5 Zero Total Cards
- **Test**: `test_display_card_front_with_zero_total_cards`
- **Purpose**: Test display_card_front with zero total cards
- **Input**: Zero for total cards parameter
- **Expected**: Displays "Card {n}/0" format

#### 2.6 EOF Error Handling
- **Test**: `test_get_user_input_handles_eof_error_gracefully`
- **Purpose**: Test get_user_input handles EOFError (Ctrl+D) gracefully
- **Input**: EOFError exception during input
- **Expected**: Graceful termination message, sys.exit(0)

#### 2.7 Empty String Input
- **Test**: `test_get_user_input_with_empty_string_returns_empty`
- **Purpose**: Test get_user_input with empty string returns empty string
- **Input**: Empty string from input
- **Expected**: Empty string returned

#### 2.8 Empty Correct Answer
- **Test**: `test_display_incorrect_feedback_with_empty_answer`
- **Purpose**: Test display_incorrect_feedback with empty correct answer
- **Input**: Empty string as correct answer
- **Expected**: "Incorrect (correct answer: )" format

#### 2.9 None Missed Cards
- **Test**: `test_display_quiz_summary_with_none_missed_cards`
- **Purpose**: Test display_quiz_summary with None missed cards
- **Input**: None for missed_cards parameter
- **Expected**: TypeError raised

#### 2.10 Invalid Accuracy Format
- **Test**: `test_display_quiz_summary_with_invalid_accuracy_format`
- **Purpose**: Test display_quiz_summary with invalid accuracy format
- **Input**: float('inf') for accuracy percentage
- **Expected**: "Accuracy: inf%" displayed (graceful handling)

#### 2.11 Very Long Strategy Name
- **Test**: `test_display_quiz_summary_with_very_long_strategy_name`
- **Purpose**: Test display_quiz_summary with very long strategy name
- **Input**: 1000 character strategy name
- **Expected**: Long name handled correctly in output

### 3. Edge Cases (Boundary Conditions)

#### 3.1 Very Long Content Display
- **Test**: `test_display_card_front_with_very_long_content`
- **Purpose**: Test display_card_front with very long front text
- **Input**: 10,000 character front text
- **Expected**: Long text displayed correctly

#### 3.2 Unicode Content Display
- **Test**: `test_display_card_front_with_unicode_content`
- **Purpose**: Test display_card_front with unicode content
- **Input**: Text with unicode characters and emojis
- **Expected**: Unicode content displayed correctly

#### 3.3 Maximum Card Numbers
- **Test**: `test_display_card_front_with_maximum_card_numbers`
- **Purpose**: Test display_card_front with very large card numbers
- **Input**: 999,999 for card number and total
- **Expected**: Large numbers displayed correctly

#### 3.4 Unicode User Input
- **Test**: `test_get_user_input_with_unicode_input`
- **Purpose**: Test get_user_input with unicode input
- **Input**: Unicode characters in user response
- **Expected**: Unicode input handled correctly

#### 3.5 Very Long User Input
- **Test**: `test_get_user_input_with_very_long_input`
- **Purpose**: Test get_user_input with very long input
- **Input**: 10,000 character user response
- **Expected**: Long input handled correctly

#### 3.6 Explicitly Empty Missed Cards
- **Test**: `test_display_quiz_summary_with_empty_missed_cards_list`
- **Purpose**: Test display_quiz_summary with explicitly empty missed cards list
- **Input**: Empty list for missed cards with zero scores
- **Expected**: Perfect score message displayed

#### 3.7 Single Missed Card
- **Test**: `test_display_quiz_summary_with_single_missed_card`
- **Purpose**: Test display_quiz_summary with exactly one missed card
- **Input**: Single flashcard in missed cards list
- **Expected**: "Terms you missed (1):" with single card display

#### 3.8 Zero Accuracy Calculation
- **Test**: `test_display_quiz_summary_with_zero_accuracy_calculation`
- **Purpose**: Test display_quiz_summary with zero accuracy
- **Input**: 0% accuracy with zero correct answers
- **Expected**: Zero accuracy displayed correctly

#### 3.9 Very Large Card Count
- **Test**: `test_display_quiz_summary_with_very_large_card_count`
- **Purpose**: Test display_quiz_summary with very large numbers of cards
- **Input**: 999,999 total cards
- **Expected**: Large numbers handled correctly

### 4. Performance Tests (Repeated Operations)

#### 4.1 Repeated Message Display Performance
- **Test**: `test_display_message_performance_with_repeated_calls`
- **Purpose**: Test performance of display_message with many repeated calls
- **Input**: 1000 message display operations
- **Expected**: Completion within 1 second

#### 4.2 Repeated Card Display Performance
- **Test**: `test_display_card_front_performance_with_repeated_calls`
- **Purpose**: Test performance of display_card_front with many repeated calls
- **Input**: 1000 card display operations
- **Expected**: Completion within 1 second

#### 4.3 Repeated Input Collection Performance
- **Test**: `test_get_user_input_performance_with_repeated_calls`
- **Purpose**: Test performance of get_user_input with many repeated calls
- **Input**: 1000 input collection operations
- **Expected**: Completion within 1 second

#### 4.4 Large Missed Cards Performance
- **Test**: `test_display_quiz_summary_performance_with_large_missed_cards`
- **Purpose**: Test performance of display_quiz_summary with large missed cards list
- **Input**: 500 missed cards in summary
- **Expected**: Completion within 2 seconds

### 5. Mocking Tests (I/O Behavior Verification)

#### 5.1 Print Call Verification
- **Test**: `test_display_message_calls_print_with_correct_parameters`
- **Purpose**: Verify display_message calls print with correct parameters
- **Input**: Test message string
- **Expected**: print() called once with exact message

#### 5.2 Stderr Print Verification
- **Test**: `test_display_error_calls_print_with_stderr`
- **Purpose**: Verify display_error calls print with stderr parameter
- **Input**: Test error message
- **Expected**: print() called with file=sys.stderr

#### 5.3 Input Call Verification
- **Test**: `test_get_user_input_calls_input_with_correct_prompt`
- **Purpose**: Verify get_user_input calls input with correct prompt
- **Input**: Custom prompt and mock response
- **Expected**: input() called with exact prompt

#### 5.4 Output Format Construction
- **Test**: `test_display_card_front_constructs_correct_output_format`
- **Purpose**: Verify display_card_front constructs correct output format
- **Input**: Card data with phase name
- **Expected**: print() called with exact formatted string

#### 5.5 Exact Message Verification
- **Test**: `test_display_correct_feedback_calls_print_with_exact_message`
- **Purpose**: Verify display_correct_feedback calls print with exact message
- **Input**: Method call only
- **Expected**: print() called with "Correct"

#### 5.6 Message Formatting Verification
- **Test**: `test_display_incorrect_feedback_formats_message_correctly`
- **Purpose**: Verify display_incorrect_feedback formats message correctly
- **Input**: Correct answer string
- **Expected**: print() called with formatted incorrect message

### 6. Integration Tests (Realistic Workflows)

#### 6.1 Complete Card Display Workflow
- **Test**: `test_complete_card_display_workflow`
- **Purpose**: Test complete workflow of displaying cards with feedback
- **Input**: Multiple cards with mixed correct/incorrect responses
- **Expected**: Complete sequence with proper formatting and separators

#### 6.2 Realistic Quiz Summary
- **Test**: `test_quiz_summary_with_realistic_data`
- **Purpose**: Test quiz summary with realistic mixed results
- **Input**: Realistic quiz results with some missed cards
- **Expected**: Comprehensive summary with correct statistics and formatting

#### 6.3 Unicode Content Integration
- **Test**: `test_unicode_content_integration_workflow`
- **Purpose**: Test complete workflow with unicode content
- **Input**: Unicode flashcards throughout full workflow
- **Expected**: Unicode content handled correctly in all display operations

#### 6.4 Error Handling Integration
- **Test**: `test_error_handling_workflow_integration`
- **Purpose**: Test integration of error handling across multiple methods
- **Input**: Mix of error and normal operations
- **Expected**: Errors to stderr, normal output to stdout

#### 6.5 EOF Handling Integration
- **Test**: `test_user_input_integration_with_eof_handling`
- **Purpose**: Test user input integration with EOF handling
- **Input**: EOF error during input collection
- **Expected**: Graceful termination with user message

## Test Execution Commands

### Run All CLIInterface Tests
```bash
python -m pytest tests/test_cli_interface.py -v
```

### Run Specific Test Categories
```bash
# Happy path tests
python -m pytest tests/test_cli_interface.py::TestCLIInterfaceHappyPath -v

# Error condition tests
python -m pytest tests/test_cli_interface.py::TestCLIInterfaceErrorConditions -v

# Edge case tests
python -m pytest tests/test_cli_interface.py::TestCLIInterfaceEdgeCases -v

# Performance tests
python -m pytest tests/test_cli_interface.py::TestCLIInterfacePerformance -v

# Mocking tests
python -m pytest tests/test_cli_interface.py::TestCLIInterfaceMocking -v

# Integration tests
python -m pytest tests/test_cli_interface.py::TestCLIInterfaceIntegration -v
```

### Run with Coverage
```bash
python -m pytest tests/test_cli_interface.py --cov=src.ui.cli_interface --cov-report=html
```

### Using Test Runner Script
```bash
# All tests
python run_tests.py cli_interface

# Specific categories
python run_tests.py cli_interface_happy
python run_tests.py cli_interface_errors
python run_tests.py cli_interface_edges
python run_tests.py cli_interface_performance
python run_tests.py cli_interface_mocking
python run_tests.py cli_interface_integration

# With coverage
python run_tests.py cli_interface_coverage
```

## Testing Strategy for UI Components

### I/O Stream Testing
UI component testing requires careful I/O stream management:
- **stdout Redirection**: Using StringIO to capture print output
- **stderr Redirection**: Separate capture for error messages
- **Input Mocking**: Mock builtins.input for user input simulation
- **Stream Verification**: Ensure correct stream usage (stdout vs stderr)

### Output Format Verification
CLI interface testing focuses on output format:
- **Exact String Matching**: Verify precise output formatting
- **Template Verification**: Check parameterized output construction
- **Unicode Handling**: Test international character support
- **Length Handling**: Verify behavior with very long content

### Mock Strategy for CLI Testing
CLI components require comprehensive I/O mocking:
- **Print Function Mocking**: Capture all print() calls with parameters
- **Input Function Mocking**: Control user input simulation
- **System Exit Mocking**: Handle graceful termination scenarios
- **Stream Object Mocking**: Control stdout/stderr redirection

## Expected Test Results

- **Total Tests**: 32 comprehensive test methods
- **Coverage**: 100% line and branch coverage of CLIInterface class
- **Performance**: All tests complete within reasonable time limits
- **I/O Validation**: All print and input interactions properly verified
- **Error Handling**: All error conditions properly tested and verified
- **Unicode Support**: Complete international character handling validation

## Key Testing Features

### Comprehensive I/O Testing
- Complete stdout/stderr stream verification
- User input collection with prompt customization
- EOF handling and graceful termination
- Print function call verification with exact parameters

### Output Format Validation
- Message formatting with parameters
- Card display with progress information
- Quiz summary with comprehensive statistics
- Error message formatting with proper prefixes

### Performance Validation
- Efficient handling of repeated operations (1000+ calls)
- Large content processing verification
- Batch operation performance testing
- Memory efficiency with large datasets

### Error Handling Verification
- Graceful EOF handling with user termination
- Invalid parameter type handling
- None value handling with appropriate errors
- Edge case boundary condition handling

### Integration Testing
- Complete workflow validation
- Realistic user interaction patterns
- Unicode content handling throughout workflow
- Mixed operation scenarios (errors + normal operations)

The test suite provides enterprise-grade validation ensuring the CLIInterface class correctly handles all user interface responsibilities, maintains performance standards, properly manages I/O streams, and integrates seamlessly with the broader flashcard quiz system.