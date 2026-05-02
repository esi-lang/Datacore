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

    def parse(self) -> List[dict]:
        """Parse the entire input and return a list of parsed statements."""
        statements = []
        while self.current_token() is not None:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self) -> dict:
        """Parse a single statement (ADD, READ, UPDATE, DELETE, SELECT)."""
        token = self.current_token()
        if token is None:
            raise SyntaxError("Unexpected end of input")

        token_type, _ = token
        if token_type == "ADD":
            return self.parse_add()
        elif token_type == "READ":
            return self.parse_read()
        elif token_type == "UPDATE":
            return self.parse_update()
        elif token_type == "DELETE":
            return self.parse_delete()
        elif token_type == "SELECT":
            return self.parse_select()
        else:
            raise SyntaxError(f"Unexpected statement type: {token_type}")

    def parse_add(self) -> dict:
        """Parse an ADD statement."""
        self.consume("ADD")
        entity = self.consume("IDENTIFIER").upper()
        name = self.consume("IDENTIFIER")
        self.consume("DELIMITER")  # Consume ';'
        return {"type": "ADD", "entity": entity, "name": name}

    def parse_read(self) -> dict:
        """Parse a READ statement."""
        self.consume("READ")
        entity = self.consume("IDENTIFIER").upper()
        name = self.consume("IDENTIFIER")
        self.consume("DELIMITER")  # Consume ';'
        return {"type": "READ", "entity": entity, "name": name}

    def parse_update(self) -> dict:
        """Parse an UPDATE statement."""
        self.consume("UPDATE")
        entity = self.consume("IDENTIFIER").upper()
        name = self.consume("IDENTIFIER")
        self.consume("STATUS")
        value = self.consume("FLOAT")
        self.consume("DELIMITER")  # Consume ';'
        return {"type": "UPDATE", "entity": entity, "name": name, "value": value}

    def parse_delete(self) -> dict:
        """Parse a DELETE statement."""
        self.consume("DELETE")
        entity = self.consume("IDENTIFIER").upper()
        name = self.consume("IDENTIFIER")
        self.consume("DELIMITER")  # Consume ';'
        return {"type": "DELETE", "entity": entity, "name": name}

    def parse_select(self) -> dict:
        """Parse a SELECT statement with optional WHERE clause."""
        self.consume("SELECT")
        fields = []
        if self.current_token()[0] == "WILDCARD":
            fields.append(self.consume("WILDCARD"))
        else:
            fields.append(self.consume("IDENTIFIER"))

        self.consume("FROM")
        entity = self.consume("IDENTIFIER").upper()

        where_clause = None
        if self.current_token() and self.current_token()[0] == "WHERE":
            self.consume("WHERE")
            field = self.consume("IDENTIFIER")
            operator = self.consume("OPERATOR")
            value = self.consume("FLOAT")
            where_clause = {"field": field, "operator": operator, "value": value}

        self.consume("DELIMITER")  # Consume ';'
        return {
            "type": "SELECT",
            "fields": fields,
            "entity": entity,
            "where": where_clause
        }

# Example usage
if __name__ == "__main__":
    # Example tokens from your lexer
    tokens = [
        ("SELECT", None), ("WILDCARD", "*"), ("FROM", None), ("IDENTIFIER", "STUDENT"), ("DELIMITER", ";"),
        ("SELECT", None), ("IDENTIFIER", "name"), ("FROM", None), ("IDENTIFIER", "STUDENT"), ("DELIMITER", ";")
    ]

    parser = DataCoreParser(tokens)
    try:
        parsed = parser.parse()
        import pprint
        pprint.pprint(parsed)
    except SyntaxError as e:
        print(f"Syntax error: {e}", file=sys.stderr)
        
                 
