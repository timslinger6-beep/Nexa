from dataclasses import dataclass
from lexer import TokenType, Token


@dataclass
class NumberExpression:
    value: str


@dataclass
class StringExpression:
    value: str


@dataclass
class CharacterExpression:
    value: str


@dataclass
class BooleanExpression:
    value: bool


@dataclass
class NullExpression:
    pass


@dataclass
class ArrayExpression:
    elements: list


@dataclass
class VariableExpression:
    name: str


@dataclass
class IndexExpression:
    target: object
    index: object


@dataclass
class MemberExpression:
    target: object
    member: str


@dataclass
class UnaryExpression:
    operator: TokenType
    operand: object


@dataclass
class BinaryExpression:
    left: object
    operator: TokenType
    right: object


@dataclass
class CallExpression:
    name: str
    arguments: list


@dataclass
class ExpressionStatement:
    expression: object


@dataclass
class PrintStatement:
    expression: object


@dataclass
class VariableDeclaration:
    name: str
    variable_type: str
    expression: object


@dataclass
class AssignmentStatement:
    name: str
    expression: object


@dataclass
class IndexAssignmentStatement:
    target: object
    index: object
    expression: object


@dataclass
class MemberAssignmentStatement:
    target: object
    member: str
    expression: object


@dataclass
class IfStatement:
    condition: object
    then_branch: list
    else_branch: object


@dataclass
class WhileStatement:
    condition: object
    body: list


@dataclass
class ForStatement:
    initializer: object
    condition: object
    increment: object
    body: list


@dataclass
class BreakStatement:
    pass


@dataclass
class ContinueStatement:
    pass


@dataclass
class ReturnStatement:
    expression: object


@dataclass
class FunctionDeclaration:
    name: str
    parameters: list
    body: list


@dataclass
class StructField:
    name: str
    variable_type: str


@dataclass
class StructDeclaration:
    name: str
    fields: list


@dataclass
class Program:
    statements: list


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        statements = []

        while not self.check(TokenType.EOF):
            statements.append(self.parse_statement())

        return Program(statements)

    def parse_statement(self):

        if self.check_identifier("print"):
            return self.parse_print()

        if (
            self.check_identifier("int")
            or self.check_identifier("float")
            or self.check_identifier("string")
            or self.check_identifier("char")
            or self.check_identifier("bool")
        ):
            return self.parse_variable_declaration()

        if self.check_identifier("struct"):
            return self.parse_struct()

        if self.check_identifier("if"):
            return self.parse_if()

        if self.check_identifier("while"):
            return self.parse_while()

        if self.check_identifier("for"):
            return self.parse_for()

        if self.check_identifier("break"):
            self.advance()
            self.consume(TokenType.SEMICOLON, "Nach 'break' wird ';' erwartet")
            return BreakStatement()

        if self.check_identifier("continue"):
            self.advance()
            self.consume(TokenType.SEMICOLON, "Nach 'continue' wird ';' erwartet")
            return ContinueStatement()

        if self.check_identifier("return"):
            return self.parse_return()

        if self.check_identifier("function"):
            return self.parse_function()

        return self.parse_expression_or_assignment()

    def parse_print(self):
        self.advance()

        self.consume(
            TokenType.LEFT_PAREN,
            "Nach 'print' wird '(' erwartet"
        )

        expression = self.parse_expression()

        self.consume(
            TokenType.RIGHT_PAREN,
            "Nach dem print-Ausdruck wird ')' erwartet"
        )

        self.consume(
            TokenType.SEMICOLON,
            "Nach 'print(...)' wird ';' erwartet"
        )

        return PrintStatement(expression)

    def parse_variable_declaration(self):
        type_token = self.advance()
        variable_type = type_token.value

        if self.match(TokenType.LEFT_BRACKET):
            self.consume(
                TokenType.RIGHT_BRACKET,
                "Nach '[' wird ']' erwartet"
            )
            variable_type += "[]"

        name = self.consume_identifier(
            "Nach dem Datentyp wird ein Variablenname erwartet"
        )

        self.consume(
            TokenType.EQUAL,
            "Nach dem Variablennamen wird '=' erwartet"
        )

        expression = self.parse_expression()

        self.consume(
            TokenType.SEMICOLON,
            "Nach der Variablendeklaration wird ';' erwartet"
        )

        return VariableDeclaration(
            name,
            variable_type,
            expression
        )

    def parse_struct(self):
        self.advance()

        name = self.consume_identifier(
            "Nach 'struct' wird ein Name erwartet"
        )

        self.consume(
            TokenType.LEFT_BRACE,
            "Nach dem Struct-Namen wird '{' erwartet"
        )

        fields = []

        while not self.check(TokenType.RIGHT_BRACE):

            variable_type = self.consume_identifier(
                "Im Struct wird ein Datentyp erwartet"
            )

            if self.match(TokenType.LEFT_BRACKET):
                self.consume(
                    TokenType.RIGHT_BRACKET,
                    "Nach '[' wird ']' erwartet"
                )
                variable_type += "[]"

            field_name = self.consume_identifier(
                "Nach dem Datentyp wird ein Feldname erwartet"
            )

            self.consume(
                TokenType.SEMICOLON,
                "Nach dem Struct-Feld wird ';' erwartet"
            )

            fields.append(
                StructField(
                    field_name,
                    variable_type
                )
            )

        self.consume(
            TokenType.RIGHT_BRACE,
            "Nach den Struct-Feldern wird '}' erwartet"
        )

        return StructDeclaration(
            name,
            fields
        )

    def parse_if(self):
        self.advance()

        self.consume(
            TokenType.LEFT_PAREN,
            "Nach 'if' wird '(' erwartet"
        )

        condition = self.parse_expression()

        self.consume(
            TokenType.RIGHT_PAREN,
            "Nach der if-Bedingung wird ')' erwartet"
        )

        then_branch = self.parse_block()
        else_branch = None

        if self.check_identifier("else"):
            self.advance()

            if self.check_identifier("if"):
                else_branch = [self.parse_if()]
            else:
                else_branch = self.parse_block()

        return IfStatement(
            condition,
            then_branch,
            else_branch
        )

    def parse_while(self):
        self.advance()

        self.consume(
            TokenType.LEFT_PAREN,
            "Nach 'while' wird '(' erwartet"
        )

        condition = self.parse_expression()

        self.consume(
            TokenType.RIGHT_PAREN,
            "Nach der while-Bedingung wird ')' erwartet"
        )

        body = self.parse_block()

        return WhileStatement(
            condition,
            body
        )

    def parse_for(self):
        self.advance()

        self.consume(
            TokenType.LEFT_PAREN,
            "Nach 'for' wird '(' erwartet"
        )

        initializer = None

        if not self.check(TokenType.SEMICOLON):

            if (
                self.check_identifier("int")
                or self.check_identifier("float")
                or self.check_identifier("string")
                or self.check_identifier("char")
                or self.check_identifier("bool")
            ):
                initializer = self.parse_variable_declaration()
            else:
                initializer = self.parse_assignment_without_semicolon()

        else:
            self.advance()

        condition = None

        if not self.check(TokenType.SEMICOLON):
            condition = self.parse_expression()

        self.consume(
            TokenType.SEMICOLON,
            "Im for-Block wird ';' erwartet"
        )

        increment = None

        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.parse_assignment_without_semicolon()

        self.consume(
            TokenType.RIGHT_PAREN,
            "Nach dem for-Kopf wird ')' erwartet"
        )

        body = self.parse_block()

        return ForStatement(
            initializer,
            condition,
            increment,
            body
        )

    def parse_return(self):
        self.advance()

        if self.check(TokenType.SEMICOLON):
            self.advance()
            return ReturnStatement(None)

        expression = self.parse_expression()

        self.consume(
            TokenType.SEMICOLON,
            "Nach 'return' wird ';' erwartet"
        )

        return ReturnStatement(expression)

    def parse_function(self):
        self.advance()

        name = self.consume_identifier(
            "Nach 'function' wird ein Funktionsname erwartet"
        )

        self.consume(
            TokenType.LEFT_PAREN,
            "Nach dem Funktionsnamen wird '(' erwartet"
        )

        parameters = []

        if not self.check(TokenType.RIGHT_PAREN):

            while True:

                parameters.append(
                    self.consume_identifier(
                        "Als Funktionsparameter wird ein Name erwartet"
                    )
                )

                if not self.match(TokenType.COMMA):
                    break

        self.consume(
            TokenType.RIGHT_PAREN,
            "Nach den Funktionsparametern wird ')' erwartet"
        )

        body = self.parse_block()

        return FunctionDeclaration(
            name,
            parameters,
            body
        )

    def parse_block(self):
        self.consume(
            TokenType.LEFT_BRACE,
            "Ein Block muss mit '{' beginnen"
        )

        statements = []

        while (
            not self.check(TokenType.RIGHT_BRACE)
            and not self.check(TokenType.EOF)
        ):
            statements.append(
                self.parse_statement()
            )

        self.consume(
            TokenType.RIGHT_BRACE,
            "Ein Block muss mit '}' enden"
        )

        return statements

    def parse_expression_or_assignment(self):
        expression = self.parse_expression()

        if self.match(TokenType.EQUAL):

            value = self.parse_expression()

            self.consume(
                TokenType.SEMICOLON,
                "Nach der Zuweisung wird ';' erwartet"
            )

            if isinstance(expression, VariableExpression):
                return AssignmentStatement(
                    expression.name,
                    value
                )

            if isinstance(expression, IndexExpression):
                return IndexAssignmentStatement(
                    expression.target,
                    expression.index,
                    value
                )

            if isinstance(expression, MemberExpression):
                return MemberAssignmentStatement(
                    expression.target,
                    expression.member,
                    value
                )

            raise SyntaxError(
                "Dieser Ausdruck kann nicht beschrieben werden"
            )

        self.consume(
            TokenType.SEMICOLON,
            "Nach dem Ausdruck wird ';' erwartet"
        )

        return ExpressionStatement(expression)

    def parse_assignment_without_semicolon(self):
        expression = self.parse_expression()

        if not self.match(TokenType.EQUAL):
            return ExpressionStatement(expression)

        value = self.parse_expression()

        if isinstance(expression, VariableExpression):
            return AssignmentStatement(
                expression.name,
                value
            )

        if isinstance(expression, IndexExpression):
            return IndexAssignmentStatement(
                expression.target,
                expression.index,
                value
            )

        if isinstance(expression, MemberExpression):
            return MemberAssignmentStatement(
                expression.target,
                expression.member,
                value
            )

        raise SyntaxError(
            "Dieser Ausdruck kann nicht beschrieben werden"
        )

    def parse_expression(self):
        return self.parse_logical_or()

    def parse_logical_or(self):
        expression = self.parse_logical_and()

        while self.match(TokenType.LOGICAL_OR):
            operator = self.previous().type
            right = self.parse_logical_and()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    def parse_logical_and(self):
        expression = self.parse_comparison()

        while self.match(TokenType.LOGICAL_AND):
            operator = self.previous().type
            right = self.parse_comparison()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    def parse_comparison(self):
        expression = self.parse_bit_or()

        while self.match(
            TokenType.EQUAL_EQUAL,
            TokenType.NOT_EQUAL,
            TokenType.LESS,
            TokenType.GREATER,
            TokenType.LESS_EQUAL,
            TokenType.GREATER_EQUAL
        ):
            operator = self.previous().type
            right = self.parse_bit_or()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    def parse_bit_or(self):
        expression = self.parse_bit_xor()

        while self.match(TokenType.BIT_OR):
            operator = self.previous().type
            right = self.parse_bit_xor()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    def parse_bit_xor(self):
        expression = self.parse_bit_and()

        while self.match(TokenType.BIT_XOR):
            operator = self.previous().type
            right = self.parse_bit_and()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    def parse_bit_and(self):
        expression = self.parse_shift()

        while self.match(TokenType.BIT_AND):
            operator = self.previous().type
            right = self.parse_shift()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    def parse_shift(self):
        expression = self.parse_addition()

        while self.match(
            TokenType.SHIFT_LEFT,
            TokenType.SHIFT_RIGHT
        ):
            operator = self.previous().type
            right = self.parse_addition()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    def parse_addition(self):
        expression = self.parse_multiplication()

        while self.match(
            TokenType.PLUS,
            TokenType.MINUS
        ):
            operator = self.previous().type
            right = self.parse_multiplication()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    def parse_multiplication(self):
        expression = self.parse_unary()

        while self.match(
            TokenType.STAR,
            TokenType.SLASH,
            TokenType.PERCENT
        ):
            operator = self.previous().type
            right = self.parse_unary()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    def parse_unary(self):

        if self.match(
            TokenType.MINUS,
            TokenType.LOGICAL_NOT,
            TokenType.BIT_NOT
        ):
            operator = self.previous().type
            operand = self.parse_unary()

            return UnaryExpression(
                operator,
                operand
            )

        return self.parse_postfix()

    def parse_postfix(self):
        expression = self.parse_factor()

        while True:

            if self.match(TokenType.LEFT_BRACKET):

                index = self.parse_expression()

                self.consume(
                    TokenType.RIGHT_BRACKET,
                    "Nach dem Array-Index wird ']' erwartet"
                )

                expression = IndexExpression(
                    expression,
                    index
                )

                continue

            if self.match(TokenType.DOT):

                member = self.consume_identifier(
                    "Nach '.' wird ein Member-Name erwartet"
                )

                expression = MemberExpression(
                    expression,
                    member
                )

                continue

            break

        return expression

    def parse_factor(self):

        if self.match(TokenType.NUMBER):
            return NumberExpression(
                self.previous().value
            )

        if self.match(TokenType.STRING):
            return StringExpression(
                self.previous().value
            )

        if self.match(TokenType.CHARACTER):
            return CharacterExpression(
                self.previous().value
            )

        if self.match(TokenType.IDENTIFIER):

            name = self.previous().value

            if name == "true":
                return BooleanExpression(True)

            if name == "false":
                return BooleanExpression(False)

            if name == "null":
                return NullExpression()

            if self.match(TokenType.LEFT_PAREN):

                arguments = []

                if not self.check(TokenType.RIGHT_PAREN):

                    while True:

                        arguments.append(
                            self.parse_expression()
                        )

                        if not self.match(TokenType.COMMA):
                            break

                self.consume(
                    TokenType.RIGHT_PAREN,
                    "Nach den Funktionsargumenten wird ')' erwartet"
                )

                return CallExpression(
                    name,
                    arguments
                )

            return VariableExpression(name)

        if self.match(TokenType.LEFT_BRACKET):

            elements = []

            if not self.check(TokenType.RIGHT_BRACKET):

                while True:

                    elements.append(
                        self.parse_expression()
                    )

                    if not self.match(TokenType.COMMA):
                        break

            self.consume(
                TokenType.RIGHT_BRACKET,
                "Nach dem Array wird ']' erwartet"
            )

            return ArrayExpression(elements)

        if self.match(TokenType.LEFT_PAREN):

            expression = self.parse_expression()

            self.consume(
                TokenType.RIGHT_PAREN,
                "Nach dem Ausdruck wird ')' erwartet"
            )

            return expression

        token = self.peek()

        raise SyntaxError(
            f"Unerwarteter Token '{token.value}' "
            f"an Position {token.position}"
        )

    def peek(self):
        return self.tokens[self.position]

    def previous(self):
        return self.tokens[self.position - 1]

    def advance(self):
        if not self.check(TokenType.EOF):
            self.position += 1

        return self.previous()

    def check(self, token_type):
        return self.peek().type == token_type

    def check_identifier(self, name):
        return (
            self.check(TokenType.IDENTIFIER)
            and self.peek().value == name
        )

    def match(self, *token_types):

        for token_type in token_types:

            if self.check(token_type):
                self.advance()
                return True

        return False

    def consume(self, token_type, message):

        if self.check(token_type):
            return self.advance()

        token = self.peek()

        raise SyntaxError(
            f"{message} (Position {token.position})"
        )

    def consume_identifier(self, message):

        if self.check(TokenType.IDENTIFIER):
            return self.advance().value

        token = self.peek()

        raise SyntaxError(
            f"{message} (Position {token.position})"
        )
