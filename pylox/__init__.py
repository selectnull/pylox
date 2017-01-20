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

        for token in tokens:
            print(token)

    def error(self, line, message):
        self.report(line, "", message)

    def report(self, line, where, message):
        text = f'[line {line}] Error {where}: {message}'
        print(text, file=sys.stderr)
        self.had_error = True
