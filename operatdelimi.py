# Added operator and delimiter handling
operators = {'+', '-', '*', '/', '=', '>', '<'}
delimiters = {';', '(', ')', '{', '}', ','}

def next_token(self):
        self.skip_whitespace()
        if self.pos >= self.length:
            return None

        char = self.source[self.pos]
        if char in self.operators:
            self.pos += 1
            if char == '*':
                return ('WILDCARD', '*')
            return ('OPERATOR', char)

        elif char in self.delimiters:
            self.pos += 1
            return ('DELIMITER', char)