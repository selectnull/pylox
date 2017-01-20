import string

from .token import Token
from .tokentype import TokenType


class Scanner(object):
    def __init__(self, source):
        self.source = source
        self.tokens = []

        self._start = 0
        self._current = 0
        self._line = 1
        self.keywords = {
            'and': TokenType.AND,
            'class': TokenType.CLASS,
            'else': TokenType.ELSE,
            'false': TokenType.FALSE,
            'for': TokenType.FOR,
            'fun': TokenType.FUN,
            'if': TokenType.IF,
            'nil': TokenType.NIL,
            'or': TokenType.OR,
            'print': TokenType.PRINT,
            'return': TokenType.RETURN,
            'super': TokenType.SUPER,
            'this': TokenType.THIS,
            'true': TokenType.TRUE,
            'var': TokenType.VAR,
            'while': TokenType.WHILE
        }

    def _is_at_end(self):
        return self._current >= len(self.source)

    def scan_tokens(self):
        while not self._is_at_end():
            self._start = self._current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, '', None, self._line))
        return self.tokens

    def scan_token(self):
        c = self._advance()
        if c == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.add_token(TokenType.COMMA)
        elif c == '.':
            self.add_token(TokenType.DOT)
        elif c == '-':
            self.add_token(TokenType.MINUS)
        elif c == '+':
            self.add_token(TokenType.PLUS)
        elif c == ';':
            self.add_token(TokenType.SEMICOLON)
        elif c == '*':
            self.add_token(TokenType.STAR)
        elif c == '!':
            self.add_token(
                TokenType.BANG_EQUAL if self._match('=') else TokenType.BANG)
        elif c == '=':
            self.add_token(
                TokenType.EQUAL_EQUAL if self._match('=') else TokenType.EQUAL)
        elif c == '<':
            self.add_token(
                TokenType.LESS_EQUAL if self._match('=') else TokenType.LESS)
        elif c == '>':
            self.add_token(
                TokenType.GREATER_EQUAL if self._match('=') else TokenType.GREATER)
        elif c == '/':
            if self._match('/'):
                while (self._peek() != '\n' and not self._is_at_end()):
                    self._advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c in [' ', '\r', '\t']:
            pass
        elif c == '\n':
            self._line += 1
        elif c == '"':
            self.string()
        elif self._is_digit(c):
            self.number()
        elif self._is_alpha(c):
            self.identifier()
        else:
            Lox().error(line, "Unexpected character.");

    def identifier(self):
        while self._is_alpha_numeric(self._peek()):
            self._advance()
        text = self.source[self._start:self._current]
        token_type = self.keywords.get(text)
        if token_type is None:
            token_type = TokenType.IDENTIFIER

        self.add_token(token_type)

    def number(self):
        while self._is_digit(self._peek()):
            self._advance()

        if self._peek() == '.' and self._is_digit(self._peek_next()):
            # consume the dot
            self._advance()
            while self._is_digit(self._peek()):
                self._advance()

        self.add_token(
            TokenType.NUMBER, float(self.source[self._start:self._current]))

    def string(self):
        while self._peek() != '"' and not self._is_at_end():
            if self._peek == '\n':
                self._line += 1
            self._advance()

        # unterminated string
        if self._is_at_end():
            Lox().error(line, "Unterminated string.")

        self._advance()
        value = self.source[self._start+1:self._current-1]
        self.add_token(TokenType.STRING, value)

    def _is_digit(self, c):
        return '0' <= c <= '9'

    def _is_alpha(self, c):
        return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or c == '_'

    def _is_alpha_numeric(self, c):
        return self._is_alpha(c) or self._is_digit(c)

    def _match(self, expected):
        if self._is_at_end():
            return False

        if self.source[self._current] != expected:
            return False

        self._current += 1
        return True

    def _peek(self):
        if self._current >= len(self.source):
            return '\0'
        return self.source[self._current]

    def _peek_next(self):
        if (self._current + 1) >= len(self.source):
            return '\0'
        return self.source[self._current+1]

    def _advance(self):
        self._current += 1
        return self.source[self._current-1]

    def add_token(self, token_type, literal=None):
        text = self.source[self._start:self._current]
        self.tokens.append(Token(token_type, text, literal, self._line))
