def next_token(self):
        self.skip_whitespace()
        if self.pos >= self.length:
            return None

        char = self.source[self.pos]
        if char.isalpha():
            start = self.pos
            while self.pos < self.length and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
                self.pos += 1
            ident = self.source[start:self.pos]
            return ('IDENTIFIER', ident)

        elif char == '*':
            self.pos += 1
            return ('WILDCARD', '*')