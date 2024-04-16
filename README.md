# Parser-Building
 Lexical Analysis and Abstract Syntax Tree (AST) construction

**For example, statement in the language x = 5 + 3 matches the following Grammar rule:**
* expression -> variable ’=’ arithmetic expression.
* arithmetic expression -> term ((’+’ | ’-’) term) *
* term -> factor ((’*’ | ’/’) factor) *
* factor -> number

The file parser_1.py contains lexer and parser classes which can be used to invoke the parse function to retrieve the AST representation of the program code.

The output matchs the pre-order traversal of the AST for each statement in the programming
language. 

Used a caconical form as below:

  For a statement a = 10 + 20

  The parser emits : ('=', 'a', ('+', 10, 20))

  ('+', 10, 20) - first the operator, then LHS and RHS.

  The same logic applies for a = 10 + 20 expression.