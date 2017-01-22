class NativeFunction(object):
    # should implement Callable

    def __init__(self, required_arguments, function):
        self.required_arguments = required_arguments
        self.function = function

    def call(self, interpreter, arguments):
        return function.call(arguments)
