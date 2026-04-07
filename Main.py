import sys

class DataCoreLexer:
    """
    The DataCore lexer: Converts raw script into tokens for a data management language.
    .
    """

    # Keywords defined in the DataCore proposal and group notes
    keywords = {
        'ADD', 'READ', 'UPDATE', 'DELETE', 'DROP', 'SHOW', 'COUNT',
        'SELECT', 'FROM', 'WHERE', 'STUDENT', 'EMPLOYEE', 'PRODUCT', 'STATUS'
    }

    # Added '*' as a Wildcard operator for queries
    operators = {'+', '-', '*', '/', '=', '>', '<'}
    delimiters = {';', '(', ')', '{', '}', ','}

    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.length = len(source)

    def skip_whitespace(self):
        while self.pos < self.length and self.source[self.pos].isspace():
            self.pos += 1

    def next_token(self):
        self.skip_whitespace()
        if self.pos >= self.length:
            return None
        
        char = self.source[self.pos]

        # NUMBERS: Logic to 'Accept Floats'
        if char.isdigit():
            start = self.pos
            has_decimal = False
            while self.pos < self.length:
                current = self.source[self.pos]
                if current.isdigit():
                    self.pos += 1
                elif current == '.' and not has_decimal:
                    has_decimal = True # Found a decimal point
                    self.pos += 1
                else:
                    break
            
            num_str = self.source[start:self.pos]
            # Strongly Typed: Distinguishing Float from Integer
            if has_decimal:
                return ('FLOAT', float(num_str))
            return ('INTEGER', int(num_str))

        # IDENTIFIERS & KEYWORDS: Case-insensitive matching
        elif char.isalpha():
            start = self.pos
            while self.pos < self.length and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
                self.pos += 1
            ident = self.source[start:self.pos]
            
            upper_ident = ident.upper()
            if upper_ident in self.keywords:
                return (upper_ident, None) 
            else:
                return ('IDENTIFIER', ident)

        # OPERATORS & WILDCARDS
        elif char in self.operators:
            self.pos += 1
            if char == '*':
                return ('WILDCARD', '*')
            return ('OPERATOR', char)

        elif char in self.delimiters:
            self.pos += 1
            return ('DELIMITER', char)

        else:
            raise SyntaxError(f"Unexpected character '{char}' at position {self.pos}")

    def tokenize(self):
        tokens = []
        while True:
            tok = self.next_token()
            if tok is None: break
            tokens.append(tok)
        return tokens

# Convenience Function
def lex(source):
    lexer = DataCoreLexer(source)
    return lexer.tokenize()

if __name__ == "__main__":
    # Test program based on proposal syntax
    #test_program = "ADD STUDENT tracy; READ STUDENT tracy;"
    #test_program = "UPDATE STUDENT achilles STATUS 98.5; COUNT STATUS 80;"
    test_program = "SELECT * FROM STUDENT WHERE STATUS > 90;"

    try:
        print("--- DataCore Lexer Output ---")
        tokens = lex(test_program)
        for tok in tokens:
            print(tok)
    except SyntaxError as e:
        print(f"Lexical error: {e}", file=sys.stderr)