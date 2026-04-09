"""
    Test 1: Core CRUD Operations
    This confirms your basic keywords like ADD and READ are working.
    We Changed test_program to:
    test_program = "ADD STUDENT tracy; READ STUDENT tracy;"

   This  proves: our  lexer recognizes Reserved command words and Data categories (Entities).

"""

"""

Test 2: Static Typing (Float vs. Integer)
This is a critical part where we change ;
Change test_program to:

Python

test_program = "UPDATE STUDENT achilles STATUS 98.5; COUNT STATUS 80;"

What it proves: It shows the lexer "Accepts Floats" (98.5) and distinguishes them from integers (80), supporting your Strongly Typed requirement

"""

"""

Test 3: Query & Wildcard Syntax
This tests the SQL-like features our  proposal of using the wildcard *.

Change test_program to:

Python

test_program = "SELECT * FROM STUDENT WHERE STATUS > 90;"

This it proves and  confirms the lexer can handle the Wildcard (*) and Operators (>) needed for data retrieval.
"""