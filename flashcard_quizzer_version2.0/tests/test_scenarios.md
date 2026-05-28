# JSONLoader Test Scenarios Documentation

## Test Categories Overview

### 1. Happy Path Scenarios (Normal File Processing)

#### 1.1 Valid Array Format Loading
- **Test**: `test_load_flashcards_with_valid_array_format_returns_flashcard_objects`
- **Purpose**: Verify correct loading of standard array format JSON
- **Input**: `[{"front": "...", "back": "..."}]`
- **Expected**: List of Flashcard objects with correct data

#### 1.2 Valid Object Format Loading
- **Test**: `test_load_flashcards_with_valid_object_format_returns_flashcard_objects`
- **Purpose**: Verify correct loading of object wrapper format JSON
- **Input**: `{"cards": [{"front": "...", "back": "..."}]}`
- **Expected**: List of Flashcard objects with correct data

#### 1.3 Whitespace Handling
- **Test**: `test_load_flashcards_with_whitespace_trims_correctly`
- **Purpose**: Ensure extra whitespace is properly trimmed
- **Input**: Data with leading/trailing spaces, tabs, newlines
- **Expected**: Clean flashcard data without whitespace

#### 1.4 Unicode Character Support
- **Test**: `test_load_flashcards_with_unicode_characters_handles_correctly`
- **Purpose**: Verify proper handling of international characters and emojis
- **Input**: Unicode characters, Chinese text, mathematical symbols, emojis
- **Expected**: Correct preservation of Unicode data

### 2. Error Conditions (Incorrect JSON Format, Non-existent Files)

#### 2.1 File Not Found
- **Test**: `test_load_flashcards_with_nonexistent_file_raises_file_not_found_error`
- **Purpose**: Verify proper error when file doesn't exist
- **Input**: Non-existent file path
- **Expected**: FileNotFoundError with descriptive message

#### 2.2 Malformed JSON
- **Test**: `test_load_flashcards_with_malformed_json_raises_json_decode_error`
- **Purpose**: Handle invalid JSON syntax gracefully
- **Input**: JSON with syntax errors
- **Expected**: JSONDecodeError with file path information

#### 2.3 Invalid Root Data Type
- **Test**: `test_load_flashcards_with_invalid_root_type_raises_value_error`
- **Purpose**: Reject JSON that isn't array or object format
- **Input**: String, number, or other primitive types at root
- **Expected**: ValueError explaining valid formats

#### 2.4 Missing 'cards' Field
- **Test**: `test_load_flashcards_with_object_missing_cards_field_raises_value_error`
- **Purpose**: Validate object format has required 'cards' field
- **Input**: `{"flashcards": [...]}` or other field names
- **Expected**: ValueError with format guidance

#### 2.5 Invalid 'cards' Field Type
- **Test**: `test_load_flashcards_with_cards_field_not_list_raises_value_error`
- **Purpose**: Ensure 'cards' field contains a list
- **Input**: `{"cards": "string"}` or other non-list types
- **Expected**: ValueError specifying list requirement

#### 2.6 Invalid Flashcard Data
- **Test**: `test_load_flashcards_with_invalid_flashcard_data_raises_value_error_with_index`
- **Purpose**: Provide clear error messages for invalid card data
- **Input**: Missing 'front' or 'back' fields
- **Expected**: ValueError with specific index and field information

#### 2.7 Empty Field Validation
- **Tests**: 
  - `test_load_flashcards_with_empty_front_field_raises_value_error`
  - `test_load_flashcards_with_empty_back_field_raises_value_error`
- **Purpose**: Prevent empty or whitespace-only fields
- **Input**: Empty strings or whitespace-only content
- **Expected**: ValueError about non-empty string requirement

### 3. Edge Cases (Single Item, No Items, Boundary Conditions)

#### 3.1 Empty Collections
- **Tests**:
  - `test_load_flashcards_with_empty_array_raises_value_error`
  - `test_load_flashcards_with_empty_cards_array_raises_value_error`
- **Purpose**: Handle empty flashcard collections
- **Input**: `[]` or `{"cards": []}`
- **Expected**: ValueError about no flashcards

#### 3.2 Single Flashcard
- **Test**: `test_load_flashcards_with_single_flashcard_returns_one_item`
- **Purpose**: Verify handling of minimal valid dataset
- **Input**: Single flashcard in array or object format
- **Expected**: Exactly one Flashcard object

#### 3.3 Type Conversion
- **Test**: `test_load_flashcards_with_numeric_values_converts_to_strings`
- **Purpose**: Ensure non-string values are converted properly
- **Input**: Numeric values for front/back fields
- **Expected**: String representation of numbers

#### 3.4 Null Value Handling
- **Test**: `test_load_flashcards_with_null_values_raises_value_error`
- **Purpose**: Reject null values in required fields
- **Input**: `null` values in front or back fields
- **Expected**: ValueError about non-empty string requirement

### 4. Performance Scenarios (Large Data Sets)

#### 4.1 Large Dataset Performance
- **Test**: `test_load_flashcards_with_large_dataset_completes_within_reasonable_time`
- **Purpose**: Ensure acceptable performance with large files
- **Input**: 1000 flashcard entries
- **Expected**: Completion within 2 seconds

#### 4.2 Large Dataset Data Integrity
- **Test**: `test_load_flashcards_with_large_dataset_maintains_data_integrity`
- **Purpose**: Verify all data is correctly processed in large files
- **Input**: 1000 flashcard entries with sequential numbering
- **Expected**: All 1000 items present with correct data

### 5. Mocking Tests (External Dependency Isolation)

#### 5.1 File System Interaction
- **Test**: `test_load_flashcards_with_path_exists_check_called`
- **Purpose**: Verify file existence checking behavior
- **Mock**: Path.exists() method
- **Expected**: Proper file existence validation

#### 5.2 File Opening
- **Test**: `test_load_flashcards_with_file_opened_with_correct_encoding`
- **Purpose**: Ensure files are opened with UTF-8 encoding
- **Mock**: Built-in open() function
- **Expected**: UTF-8 encoding parameter used

#### 5.3 JSON Parsing
- **Test**: `test_load_flashcards_with_json_load_called_correctly`
- **Purpose**: Verify JSON parsing is called with correct parameters
- **Mock**: json.load() function
- **Expected**: Correct file handle passed to json.load()

## Test Execution Commands

### Run All Tests
```bash
python -m pytest tests/test_json_loader.py -v
```

### Run Specific Test Categories
```bash
# Happy path tests only
python -m pytest tests/test_json_loader.py::TestJSONLoaderHappyPath -v

# Error condition tests only  
python -m pytest tests/test_json_loader.py::TestJSONLoaderErrorConditions -v

# Edge case tests only
python -m pytest tests/test_json_loader.py::TestJSONLoaderEdgeCases -v

# Performance tests only
python -m pytest tests/test_json_loader.py::TestJSONLoaderPerformance -v

# Mocking tests only
python -m pytest tests/test_json_loader.py::TestJSONLoaderMocking -v
```

### Run with Coverage
```bash
python -m pytest tests/test_json_loader.py --cov=src.data.json_loader --cov-report=html
```

## Expected Test Results

- **Total Tests**: 23 comprehensive test methods
- **Coverage**: 100% line and branch coverage of JSONLoader class
- **Performance**: All tests should complete within seconds
- **Error Handling**: Every error condition properly tested and documented