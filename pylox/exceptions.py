class RuntimeError(Exception):
    def __init__(self, token, message):
        super(message)
        self.token = token


class Return(Exception):
    def __init__(self, value):
        self.value = value
