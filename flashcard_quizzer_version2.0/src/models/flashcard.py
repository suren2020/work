"""
Flashcard data model with validation.
Follows Single Responsibility Principle.
"""

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class Flashcard:
    """
    Immutable flashcard data model.
    
    Attributes:
        front: Text displayed to the user as the question
        back: Expected answer text for validation
    """
    front: str
    back: str
    
    def __post_init__(self):
        """Validate flashcard data after initialization."""
        if not isinstance(self.front, str) or not self.front.strip():
            raise ValueError("Flashcard front must be a non-empty string")
        
        if not isinstance(self.back, str) or not self.back.strip():
            raise ValueError("Flashcard back must be a non-empty string")
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Flashcard':
        """
        Create a Flashcard from a dictionary.
        
        Args:
            data: Dictionary containing 'front' and 'back' keys
            
        Returns:
            Flashcard instance
            
        Raises:
            ValueError: If required keys are missing or invalid
        """
        if not isinstance(data, dict):
            raise ValueError("Flashcard data must be a dictionary")
        
        if 'front' not in data:
            raise ValueError("Flashcard data missing 'front' field")
        
        if 'back' not in data:
            raise ValueError("Flashcard data missing 'back' field")
        
        return cls(front=str(data['front']).strip(), back=str(data['back']).strip())
    
    def matches_answer(self, user_input: str) -> bool:
        """
        Check if user input matches the flashcard answer.
        
        Args:
            user_input: User's answer attempt
            
        Returns:
            True if the answer matches (case-insensitive)
        """
        if not isinstance(user_input, str):
            return False
        
        return self.back.lower().strip() == user_input.lower().strip()