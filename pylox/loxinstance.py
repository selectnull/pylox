from .exceptions import RuntimeError


class LoxInstance(object):
    def __init__(self, klass):
        self.fields = {}
        self._klass = klass

    def get_property(self, token_name):
        if token_name.lexeme in self.fields:
            return self.fields[token_name.lexeme]

        method = self._klass.find_method(self, token_name.lexeme)
        if method is not None:
            return method

        raise RuntimeError("Undefined property '{}'.".format(token_name.lexeme))

    def __str__(self):
        return self._klass.name + " instance"
