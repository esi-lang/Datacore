import sys
from typing import List, Tuple, Union, Optional

# Defined token types for clarity
Token = Tuple[str, Union[str, int, float, None]]

class DataCoreParser:
    """
    A recursive descent parser for the DataCore language.
    Handles CRUD operations, queries, and conditional expressions.
    """

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Optional[Token]:
        """Return the current token or None if at the end of the input."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected_type: str) -> Union[str, int, float]:
        """Consume the current token and return its value if it matches the expected type."""
        token = self.current_token()
        if token is None:
            raise SyntaxError(f"Unexpected end of input, expected {expected_type}")
        token_type, token_value = token
        if token_type == expected_type:
            self.pos += 1
            return token_value
        raise SyntaxError(f"Expected {expected_type}, got {token_type}")
