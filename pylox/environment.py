from runtimeerror import RuntimeError


class Environment(object)
    def __init__(self, enclosing=None):
        self.enclosing = enclosing
        self.values = {}

    def declare(self, token_name):
        if token_name.lexeme not in self.values:
            self.values[token_name.lexeme] = None

    def get(self, token_name):
        if token_name.lexeme in self.values:
            return values[token_name.lexeme]

        if self.enclosing is not None:
            return self.enclosing.get(token_name)

        raise RuntimeError(token_name, "Undefined variable '{}'.".format(token_name.lexeme))

    def assign(self, token_name, value):
        if token_name.lexeme in self.values:
            self.values[token_name.lexeme] = value
            return None

        if self.enclosing is not None:
            self.enclosing.assign(token_name, value)
            return None

        raise RuntimeError("Undefined variable '{}'".format(token_name.lexeme))

    def define(self, name, value):
        self.values[name] = value

    def get_at(self, distance, name):
        environment = self
        for i in range(distance):
            environment = environment.enclosing
        return environment.values.get(name)

    def assign_at(self, distance, token_name, value):
        environment = self
        for i in range(distance):
            environment = environment.enclosing
        environment.values[token_name.lexeme] = value

    def enter_scope(self):
        return Environment(self)

    def __str__(self):
        result = str(self.values)
        if self.enclosing is not None:
            result += " -> {}".format(str(self.enclosing))

        return result
