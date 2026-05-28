"""
JSON data loader with validation.
Follows Single Responsibility Principle for data ingestion.
"""

import json
from pathlib import Path
from typing import List

from ..models.flashcard import Flashcard


class JSONLoader:
    """Handles loading and validation of flashcard data from JSON files."""
    
    def load_flashcards(self, file_path: str) -> List[Flashcard]:
        """
        Load flashcards from a JSON file with comprehensive validation.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            List of validated Flashcard objects
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the JSON is malformed
            ValueError: If the data structure is invalid
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"JSON file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                raw_data = json.load(file)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Malformed JSON in {file_path}: {e.msg}",
                e.doc,
                e.pos
            )
        
        return self._validate_and_parse_flashcards(raw_data, file_path)
    
    def _validate_and_parse_flashcards(self, raw_data, file_path: Path) -> List[Flashcard]:
        """
        Validate raw JSON data and convert to Flashcard objects.
        Supports both array format [{"front":...}] and object format {"cards": [...]}
        
        Args:
            raw_data: Parsed JSON data
            file_path: Path for error reporting
            
        Returns:
            List of Flashcard objects
            
        Raises:
            ValueError: If data structure is invalid
        """
        # Handle object format: {"cards": [...]}
        if isinstance(raw_data, dict):
            if 'cards' not in raw_data:
                raise ValueError(
                    f"JSON file {file_path} contains an object but missing 'cards' field. "
                    f"Expected format: {{\"cards\": [...]}}"
                )
            cards_data = raw_data['cards']
            
            if not isinstance(cards_data, list):
                raise ValueError(
                    f"JSON file {file_path}: 'cards' field must be a list, "
                    f"but found {type(cards_data).__name__}"
                )
        # Handle array format: [{"front":...}]
        elif isinstance(raw_data, list):
            cards_data = raw_data
        else:
            raise ValueError(
                f"JSON file {file_path} must contain either a list of flashcards "
                f"or an object with 'cards' field, but found {type(raw_data).__name__}"
            )
        
        if not cards_data:
            raise ValueError(f"JSON file {file_path} contains no flashcards")
        
        flashcards = []
        for index, card_data in enumerate(cards_data):
            try:
                flashcard = Flashcard.from_dict(card_data)
                flashcards.append(flashcard)
            except ValueError as e:
                raise ValueError(
                    f"Invalid flashcard data at index {index} in {file_path}: {e}"
                )
        
        return flashcards