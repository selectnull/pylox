class RuntimeError(Exception):
    def __init__(self, token, message):
        super(message)
        self.token = token
