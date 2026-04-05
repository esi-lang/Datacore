 def next_token(self):
        self.skip_whitespace()
        if self.pos >= self.length:
            return None
        
        char = self.source[self.pos]

        
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
        
            if has_decimal:
                return ('FLOAT', float(num_str))
            return ('INTEGER', int(num_str))