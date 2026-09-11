from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    IDENTIFIER = auto()
    STRING = auto()
    CHARACTER = auto()
    NUMBER = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()

    EQUAL = auto()
    EQUAL_EQUAL = auto()
    NOT_EQUAL = auto()

    LESS = auto()
    GREATER = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()

    LOGICAL_AND = auto()
    LOGICAL_OR = auto()
    LOGICAL_NOT = auto()

    BIT_AND = auto()
    BIT_OR = auto()
    BIT_XOR = auto()
    BIT_NOT = auto()

    SHIFT_LEFT = auto()
    SHIFT_RIGHT = auto()

    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()

    COMMA = auto()
    DOT = auto()
    SEMICOLON = auto()
    COLON = auto()

    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    position: int


class Lexer:
    SYMBOLS = {
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.STAR,
        "/": TokenType.SLASH,
        "%": TokenType.PERCENT,

        "=": TokenType.EQUAL,

        "<": TokenType.LESS,
        ">": TokenType.GREATER,

        "!": TokenType.LOGICAL_NOT,

        "&": TokenType.BIT_AND,
        "|": TokenType.BIT_OR,
        "^": TokenType.BIT_XOR,
        "~": TokenType.BIT_NOT,

        "(": TokenType.LEFT_PAREN,
        ")": TokenType.RIGHT_PAREN,

        "[": TokenType.LEFT_BRACKET,
        "]": TokenType.RIGHT_BRACKET,

        "{": TokenType.LEFT_BRACE,
        "}": TokenType.RIGHT_BRACE,

        ",": TokenType.COMMA,
        ".": TokenType.DOT,
        ";": TokenType.SEMICOLON,
        ":": TokenType.COLON,
    }

    TWO_CHAR_SYMBOLS = {
        "==": TokenType.EQUAL_EQUAL,
        "!=": TokenType.NOT_EQUAL,

        "<=": TokenType.LESS_EQUAL,
        ">=": TokenType.GREATER_EQUAL,

        "&&": TokenType.LOGICAL_AND,
        "||": TokenType.LOGICAL_OR,

        "<<": TokenType.SHIFT_LEFT,
        ">>": TokenType.SHIFT_RIGHT,
    }

    def __init__(self, source):
        self.source = source
        self.position = 0
        self.tokens = []

    # ============================================================
    # HAUPT-FUNKTION
    # ============================================================

    def tokenize(self):
        while not self.is_at_end():
            self.skip_whitespace_and_comments()

            if self.is_at_end():
                break

            start = self.position
            char = self.advance()

            # ----------------------------------------------------
            # IDENTIFIER
            # ----------------------------------------------------

            if self.is_identifier_start(char):
                self.scan_identifier(start)
                continue

            # ----------------------------------------------------
            # ZAHL
            # ----------------------------------------------------

            if char.isdigit():
                self.scan_number(start)
                continue

            # ----------------------------------------------------
            # STRING
            # ----------------------------------------------------

            if char == '"':
                self.scan_string(start)
                continue

            # ----------------------------------------------------
            # CHARACTER
            # ----------------------------------------------------

            if char == "'":
                self.scan_character(start)
                continue

            # ----------------------------------------------------
            # ZWEI-ZEICHEN-OPERATOR
            # ----------------------------------------------------

            if self.position < len(self.source):
                two = char + self.source[self.position]

                if two in self.TWO_CHAR_SYMBOLS:
                    self.position += 1

                    self.tokens.append(
                        Token(
                            self.TWO_CHAR_SYMBOLS[two],
                            two,
                            start
                        )
                    )

                    continue

            # ----------------------------------------------------
            # EIN-ZEICHEN-SYMBOL
            # ----------------------------------------------------

            if char in self.SYMBOLS:
                self.tokens.append(
                    Token(
                        self.SYMBOLS[char],
                        char,
                        start
                    )
                )

                continue

            raise SyntaxError(
                f"Unbekanntes Zeichen '{char}' "
                f"an Position {start}"
            )

        self.tokens.append(
            Token(
                TokenType.EOF,
                "",
                self.position
            )
        )

        return self.tokens

    # ============================================================
    # IDENTIFIER
    # ============================================================

    def scan_identifier(self, start):
        while not self.is_at_end():
            char = self.peek()

            if char.isalnum() or char == "_":
                self.advance()
            else:
                break

        value = self.source[start:self.position]

        self.tokens.append(
            Token(
                TokenType.IDENTIFIER,
                value,
                start
            )
        )

    # ============================================================
    # ZAHLEN
    # ============================================================

    def scan_number(self, start):

        # --------------------------------------------------------
        # Binär: 0b1010
        # --------------------------------------------------------

        if (
            self.source[start] == "0"
            and self.peek().lower() == "b"
        ):
            self.advance()

            digits_start = self.position

            while not self.is_at_end():
                char = self.peek()

                if char in "01":
                    self.advance()
                else:
                    break

            if self.position == digits_start:
                raise SyntaxError(
                    f"Ungültige Binärzahl an Position {start}"
                )

            value = self.source[start:self.position]

            self.tokens.append(
                Token(
                    TokenType.NUMBER,
                    value,
                    start
                )
            )

            return

        # --------------------------------------------------------
        # Hexadezimal: 0xFF
        # --------------------------------------------------------

        if (
            self.source[start] == "0"
            and self.peek().lower() == "x"
        ):
            self.advance()

            digits_start = self.position

            while not self.is_at_end():
                char = self.peek()

                if char in "0123456789abcdefABCDEF":
                    self.advance()
                else:
                    break

            if self.position == digits_start:
                raise SyntaxError(
                    f"Ungültige Hexadezimalzahl an Position {start}"
                )

            value = self.source[start:self.position]

            self.tokens.append(
                Token(
                    TokenType.NUMBER,
                    value,
                    start
                )
            )

            return

        # --------------------------------------------------------
        # Oktal: 0o755
        # --------------------------------------------------------

        if (
            self.source[start] == "0"
            and self.peek().lower() == "o"
        ):
            self.advance()

            digits_start = self.position

            while not self.is_at_end():
                char = self.peek()

                if char in "01234567":
                    self.advance()
                else:
                    break

            if self.position == digits_start:
                raise SyntaxError(
                    f"Ungültige Oktalzahl an Position {start}"
                )

            value = self.source[start:self.position]

            self.tokens.append(
                Token(
                    TokenType.NUMBER,
                    value,
                    start
                )
            )

            return

        # --------------------------------------------------------
        # Normale Ganzzahl
        # --------------------------------------------------------

        while not self.is_at_end() and self.peek().isdigit():
            self.advance()

        # --------------------------------------------------------
        # FLOAT
        # --------------------------------------------------------

        if (
            not self.is_at_end()
            and self.peek() == "."
            and self.position + 1 < len(self.source)
            and self.source[self.position + 1].isdigit()
        ):
            self.advance()

            while (
                not self.is_at_end()
                and self.peek().isdigit()
            ):
                self.advance()

        value = self.source[start:self.position]

        self.tokens.append(
            Token(
                TokenType.NUMBER,
                value,
                start
            )
        )

    # ============================================================
    # STRING
    # ============================================================

    def scan_string(self, start):
        characters = []

        while not self.is_at_end():
            char = self.advance()

            if char == '"':
                value = "".join(characters)

                self.tokens.append(
                    Token(
                        TokenType.STRING,
                        value,
                        start
                    )
                )

                return

            if char == "\n":
                raise SyntaxError(
                    f"String darf nicht über mehrere Zeilen gehen "
                    f"(Position {start})"
                )

            if char == "\\":
                if self.is_at_end():
                    raise SyntaxError(
                        f"Unvollständige Escape-Sequenz "
                        f"an Position {self.position - 1}"
                    )

                escaped = self.advance()

                escapes = {
                    "n": "\n",
                    "r": "\r",
                    "t": "\t",
                    '"': '"',
                    "'": "'",
                    "\\": "\\",
                    "0": "\0",
                }

                if escaped not in escapes:
                    raise SyntaxError(
                        f"Unbekannte Escape-Sequenz "
                        f"'\\{escaped}'"
                    )

                characters.append(
                    escapes[escaped]
                )

            else:
                characters.append(char)

        raise SyntaxError(
            f"Unbeendeter String an Position {start}"
        )

    # ============================================================
    # CHARACTER
    # ============================================================

    def scan_character(self, start):
        if self.is_at_end():
            raise SyntaxError(
                f"Unbeendetes Zeichen an Position {start}"
            )

        char = self.advance()

        # Escape-Sequenz
        if char == "\\":
            if self.is_at_end():
                raise SyntaxError(
                    f"Unvollständige Escape-Sequenz "
                    f"an Position {self.position - 1}"
                )

            escaped = self.advance()

            escapes = {
                "n": "\n",
                "r": "\r",
                "t": "\t",
                "'": "'",
                '"': '"',
                "\\": "\\",
                "0": "\0",
            }

            if escaped not in escapes:
                raise SyntaxError(
                    f"Unbekannte Escape-Sequenz "
                    f"'\\{escaped}'"
                )

            char = escapes[escaped]

        if char == "\n":
            raise SyntaxError(
                f"Zeichen darf nicht über mehrere Zeilen gehen "
                f"(Position {start})"
            )

        if self.is_at_end() or self.peek() != "'":
            raise SyntaxError(
                f"Char-Literal muss genau ein Zeichen enthalten "
                f"(Position {start})"
            )

        self.advance()

        self.tokens.append(
            Token(
                TokenType.CHARACTER,
                char,
                start
            )
        )

    # ============================================================
    # KOMMENTARE / WHITESPACE
    # ============================================================

    def skip_whitespace_and_comments(self):
        while not self.is_at_end():

            if self.peek().isspace():
                self.advance()
                continue

            # Einzeiliger Kommentar //
            if (
                self.peek() == "/"
                and self.peek(1) == "/"
            ):
                self.advance()
                self.advance()

                while (
                    not self.is_at_end()
                    and self.peek() != "\n"
                ):
                    self.advance()

                continue

            # Mehrzeiliger Kommentar /*
            if (
                self.peek() == "/"
                and self.peek(1) == "*"
            ):
                start = self.position

                self.advance()
                self.advance()

                while not self.is_at_end():

                    if (
                        self.peek() == "*"
                        and self.peek(1) == "/"
                    ):
                        self.advance()
                        self.advance()
                        break

                    self.advance()

                else:
                    raise SyntaxError(
                        f"Unbeendeter Block-Kommentar "
                        f"an Position {start}"
                    )

                continue

            break

    # ============================================================
    # HILFSFUNKTIONEN
    # ============================================================

    def is_at_end(self):
        return self.position >= len(self.source)

    def advance(self):
        char = self.source[self.position]
        self.position += 1
        return char

    def peek(self, offset=0):
        index = self.position + offset

        if index >= len(self.source):
            return "\0"

        return self.source[index]

    @staticmethod
    def is_identifier_start(char):
        return (
            char.isalpha()
            or char == "_"
        )
