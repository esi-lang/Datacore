class DataCoreLexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.length = len(source)

    def skip_whitespace(self):
        while self.pos < self.length and self.source[self.pos].isspace():
            self.pos += 1
