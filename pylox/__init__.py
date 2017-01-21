__version__ = '0.0.1'
import sys

from .scanner import Scanner


class Lox(object):
    def __init__(self):
        self.had_error = False

    def error_code(self):
        return 1 if self.had_error else 0

    def run_file(self, filename):
        with open(filename, 'r') as f:
            self.run(f.read())
            if self.had_error:
                sys.exit(65)

    def run_prompt(self):
        while True:
            s = input("> ")
            self.run(s)
            self.had_error = False

    def run(self, source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        # for token in tokens:
            # print(token)

        parser = Parser(tokens)
        statements = parser.parse_program()

        if self.had_error:
            return None

        resolver = Resolver()
        _locals = resolver.resolve(statements)

        if self.had_error:
            return None

        interpreter.interpret(statements, _locals)

    def error(self, line_or_token, message):
        if isinstance(line_or_token, int):
            self.report(line, "", message)
        if isinstance(line_or_token, Token):
            if line_or_token.token_type == TokenType.EOF:
                self.report(line_or_token.line, " at end", message)
            else:
                self.report(line_or_token.line, " at '{}'".format(line_or_token.lexeme), message)

    def report(self, line, where, message):
        text = f'[line {line}] Error {where}: {message}'
        print(text, file=sys.stderr)
        self.had_error = True

    def runtime_error(self, error):
        print("{}\n[line {}]".format(error.get_message()), error.token.line)
        self.had_runtime_error = True
