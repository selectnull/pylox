class LoxFunction(object):
    # should implement Callable

    def __init__(self, declaration, closure, is_initializer):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def bind(self, lox_instance):
        environment = self.closure.enter_scope()
        environment.define("this", lox_instance)
        return LoxFunction(declaration, environment, is_initializer)

    def __str__(self):
        return self.declaration.name.lexeme

    def required_arguments(self):
        return len(self.declaration.parameters)

    def call(self, interpreter, arguments):
        result = None

        try:
            environment = self.closure.enter_scope()
            for i in range(len(self.declaration.parameters)):
                environment.define(self.declaration.parameters.get(i).lexeme, arguments.get(i))

            interpreter.execute_body(self.declaration.body, environment)
        except (Return return_value):
            result = return_value.value:

        return self.closure.get_at(0, "this") if self.is_initializer else result;
