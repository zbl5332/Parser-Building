# Lexer
class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        if self.code:
            self.current_char = self.code[self.position]    # Set to the first character
        else:
            self.current_char = None    

    # Advance to the next position and update current_char
    def advance(self):
        self.position += 1
        if self.position < len(self.code):
            self.current_char = self.code[self.position]
        else:
            self.current_char = None

    # Skip whitespace characters by advancing past them
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    # Tokenize a number
    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return ("NUMBER", int(result)) # Return a tuple representing a number token
    
    # Tokenize identifiers and condition keywords
    def identifier(self):
        result = ''
        # Identifiers contain alphabetic characters, digits, and underscores
        while self.current_char is not None and (self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        # Match identifiers to condition keywords or return as a general identifier
        if result == 'if':
            return ("IF", result)
        elif result == 'then':
            return ("THEN", result)
        elif result == 'else':
            return ("ELSE", result)
        elif result == 'while':
            return ("WHILE", result)
        elif result == 'do':
            return ("DO", result)
        else:
            return ("ID", result)

    # Move the lexer position and identify next possible tokens
    def get_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()

            if self.current_char == '+':
                self.advance()
                return ("PLUS", '+')

            if self.current_char == '-':
                self.advance()
                return ("MINUS", '-')

            if self.current_char == '*':
                self.advance()
                return ("MULTIPLY", '*')

            if self.current_char == '/':
                self.advance()
                return ("DIVISION", '/')

            if self.current_char == '(':
                self.advance()
                return ("LPAREN", '(')

            if self.current_char == ')':
                self.advance()
                return ("RPAREN", ')')

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return ("EQ", '==') # Equality operator
                return ("ASSIGN", '=')  # Assignment operator
            
            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return ("GE", '>=') # Greater than or equal to
                return ("GT", '>')  # Greater than

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return ("LE", '<=') # Less than or equal to
                return ("LT", '<')  # Less than

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return ("NEQ", '!=')    # Not equal to

        return ("EOF", None)    # End of file token when there are no more characters to read

# Parser
# Input : lexer object
# Output: AST program representation.

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_token() # Get the first token from the lexer

    # Raise an error if error happened
    def error(self, message = "Invalid syntax"):
        raise Exception(message)

    # Consume a token of the expected type and advance to the next token
    def eat(self, token_type):
        if self.current_token[0] == token_type:
            self.advance()  # Move to next token if token matches expected type
        else:
            self.error(f"Expected token {token_type}, got {self.current_token[0]}") # If token does not match, raise an error

    # Function to parse the entire program
    def parse(self):
        return self.program()
    
    # Move to the next token
    def advance(self):
        self.current_token = self.lexer.get_token()

    # Parse the one or multiple statements
    def program(self):
        nodes = []  # Create a list to hold all the parsed statements
        while self.current_token[0] != "EOF":
            nodes.append(self.statement())  # Parse and add each statement to the list
        return nodes
    
    # Parse if, while, assignment statement
    def statement(self):
        # Determine the type of statement based on the current token and parse accordingly
        if self.current_token[0] == "ID":
            node = self.assignment()
        elif self.current_token[0] == "IF":
            node = self.if_statement()
        elif self.current_token[0] == "WHILE":
            node = self.while_loop()
        else:
            self.error("Unrecognized statement")    # If it is an unrecognized statement type, raise an error
        return node

    # Parse assignment statements
    def assignment(self):
        var_name = self.current_token[1]    # Get the variable name being assigned to
        self.eat("ID")
        self.eat("ASSIGN")
        expr = self.arithmetic_expression() # Parse the expression on the right-hand side
        return ("=", var_name, expr)    # Return a tuple representing the assignment

    # Parse arithmetic experssions
    def arithmetic_expression(self):
        node = self.term()  # Start by parsing a term
        while self.current_token[0] in ("PLUS", "MINUS"):
            op = self.current_token[1]  # Get the operator
            self.eat(self.current_token[0])  # Advance past the operator
            node = (op, node, self.term())  # Construct a tuple with the operator and operands
        return node
   
    # Parse a term to handle multiplication and division
    def term(self):
        node = self.factor()    # Start by parsing a factor
        while self.current_token[0] in ("MULTIPLY", "DIVISION"):
            op = self.current_token[1]  # Operator
            self.eat(self.current_token[0])  # Advance past the operator
            node = (op, node, self.factor())    # Construct a tuple with the operator and operands
        return node

    # Parse number, variable, or parenthesized expression
    def factor(self):
        token = self.current_token
        if token[0] == "NUMBER":
            self.eat("NUMBER")
            return token[1] # Return the number directly
        elif token[0] == "LPAREN":
            self.eat("LPAREN")
            node = self.arithmetic_expression() # Parse the expression inside parentheses
            self.eat("RPAREN")
            return node
        elif token[0] == "ID":
            self.eat("ID")
            return token[1] # Return the variable name directly
        else:
            self.error()    # Raise an error if it is unexpected token type

    # Parse if statement, you can handle then and else part here
    # You also have to check for condition
    def if_statement(self):
        self.eat("IF")
        condition = self.condition()    # Parse the condition

        self.eat("THEN")
        then_branch = self.statement()  # Parse the then branch

        else_branch = None
        if self.current_token[0] == "ELSE":
            self.eat("ELSE")
            else_branch = self.statement()  # Parse else branch when if present
        # Construct and return a tuple representing if statement
        if else_branch:
            return ("if", condition, then_branch, else_branch)
        else:
            return ("if", condition, then_branch)
    
    # Implement while statment, check for condition
    # Possibly make a call to statement?
    def while_loop(self):
        self.eat("WHILE")
        condition = self.condition()    # Parse the condition

        self.eat("DO")
        body = []
        body.append(self.statement())   # Append the first statement to the body list

        return ("while", condition, body)   # Construct and return a tuple representing while loop

    # Parse a condition for if and while statements
    def condition(self):
        left_expr = self.arithmetic_expression()  # Parse the left-hand side expression
        # Find comparison operator and parse the right-hand side expression
        if self.current_token[0] in ("EQ", "NEQ", "LT", "GT", "LE", "GE"):
            op_token = self.current_token
            self.eat(op_token[0])  # Move past the operator token
            right_expr = self.arithmetic_expression()
        
            return (op_token[1], left_expr, right_expr) # Return a tuple representing the condition which are operator, LHS, RHS
        else:
            self.error("Expected comparison operator in condition") # Raise an error if found something else 