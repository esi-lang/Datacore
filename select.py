 # --- : SELECT Statement Parsing (Fields & Entity) ---
    def parse_select(self) -> dict:
        """
        Parse a SELECT statement, focusing on fields and entity.
        Example: SELECT * FROM STUDENT;
        """
        self.consume("SELECT")  # Consume the SELECT keyword
        fields = []
        if self.current_token()[0] == "WILDCARD":
            fields.append(self.consume("WILDCARD"))  # Consume the wildcard
        else:
            fields.append(self.consume("IDENTIFIER"))  # Consume the field name

        self.consume("FROM")  # Consume the FROM keyword
        entity = self.consume("IDENTIFIER").upper()  # Consume the entity type

        
        where_clause = None
        if self.current_token() and self.current_token()[0] == "WHERE":
            where_clause = self._parse_where_clause()  # Delegate to Role 6

        self.consume("DELIMITER")  # Consume the semicolon
        return {"type": "SELECT", "fields": fields, "entity": entity, "where": where_clause}