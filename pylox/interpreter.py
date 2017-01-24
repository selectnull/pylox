import time


class Interpreter(object):
    def __init__(self):
        self.globs = Environment()
        self._environment = globs
        self._locs = {}

        self.globs.define("clock", NativeFunction(0, self._clock))

    def interpret(self, statements, locs):
        self.locs = locs;

        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            Lox().runtime_error(error)

    def evaluate(self, expr):
        return expr.accept(self)

    def execute(self, stmt):
        stmt.accept(self)

    def execute_body(self, statements, environment):
        previous = self._environment
        try:
            self._environment = environment

            for statement in statements:
                self.execute(statement)
        finally:
            self._environment = previous

    def visit_block_stmt(self, stmt):
        self.execute_body(stmt.statements, self._environment.enter_scope())
        return None

    def visit_class_stmt(self, stmt):
        self._environment.declare(stmt.name)

        methods = {}
        superclass = None
        if stmt.superclass is not None:
            superclass = self.evaluate(stmt.superclass)
            if not isinstance(superclass, LoxClass):
                raise RuntimeError(stmt.name, "Superclass must be a class.")

            self._environment = self._environment.enter_scope()
            self._environment.define("super", superclass)

        for method in stmt.methods:
            function = LoxFunction(method, self._environment, method.name.lexeme == "init")
            methods[method.name.lexeme] = function

        klass = LoxClass(stmt.name.lexeme, superclass, methods)

        if superclass is not None:
            self._environment = self._environment.enclosing

        self._environment.assign(stmt.name, klass)
        return None

    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expression)
        return None

    def visit_function_stmt(self, stmt):
        self._environment.declare(stmt.name)
        function = LoxFunction(stmt, self._environment, false)
        self._environment.assign(stmt.name, function)
        return None

    def visit_if_stmt(self, stmt):
        if self._is_true(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)
        return None

    def visit_print_stmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self._stringify(value))
        return None

    def visit_return_stmt(self, stmt):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)

        raise Return(value)

    def visit_var_stmt(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self._environment.define(stmt.name.lexeme, value)
        return None

    def visit_while_stmt(self, stmt):
        while self._is_true(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None

    def visit_assign_expr(self, expr):
        value = self.evaluate(expr)

        distance = self.locs.get(expr)
        if distance is not None:
            self._environment.assign_at(distance, expr.name, value)
        else:
            self.globs.assign(expr.name, value)

        return value

    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        ot = expr.operator.type

        if ot == TokenType.BANG_EQUAL:
            return not self._is_equal(left, right)
        elif ot == TokenType.EQUAL_EQUAL:
            return self._is_equal(left, right)
        elif ot == TokenType.GREATER:
            self._check_number_operands(expr.operator, left, right)
            return left > right
        elif ot == TokenType.GREATER_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return left >= right
        elif ot == TokenType.LESS:
            self._check_number_operands(expr.operator, left, right)
            return left < right
        elif ot == TokenType.LESS_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return left <= right
        elif ot == TokenType.MINUS:
            self._check_number_operands(expr.operator, left, right)
            return left - right
        elif ot == TokenType.PLUS:
            # we should check for types here
            # works for both numbers and strings
            # TODO should raise a RuntimeError in case of wrong types
            # eg, string + number
            return left + right
        elif ot == TokenType.SLASH:
            self._check_number_operands(expr.operator, left, right)
            return left / right
        elif ot == TokenType.STAR:
            self._check_number_operands(expr.operator, left, right)
            return left * right

        # unreachable
        return None

    def visit_call_expr(self, expr):
        callee = self.evaluate(expr.callee)

        arguments = []
        for arg in expr.arguments:
            arguments.append(self.evaluate(arg))

        # TODO so far we have ignored Callable interface
        # but it's necessary here
        """
        if not isinstance(callee, Callable):
            raise RuntimeError(expr.paren, "Can only call functions and classes.")
        """

        function = callee
        if len(arguments) < function.required_arguments:
            raise RuntimeError(expr.paren, "Not enough arguments.")

        return function(*arguments)

    def visit_get_expr(self, expr):
        obj = self.evaluate(expr.object)
        if isinstance(obj, LoxInstance):
            return ob.get_property(expr.name)

        raise RuntimeError(expr.name, "Only instances have properties.")

    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)

    def visit_literal_expr(self, expr):
        return expr.value

    def visit_logical_expr(self, expr):
        left = self.evaluate(expr.left)

        if expr.operator.type == TokenType.OR and self._is_true(left):
            return left

        if expr.operator.type == TokenType.AND and not self._is_true(left):
            return left

        return self.evaluate(expr.right)

    def visit_set_expr(self, expr):
        value = self.evaluate(expr.value)
        obj = self.evaluate(expr.object)

        if isinstance(obj, LoxInstance):
            obj.fields[expr.name.lexeme, value]
            return value

        raise RuntimeError(expr.name, "Only instances have fields.")

    def visit_super_expr(self, expr):
        distance = self.locs.get(expr)
        superclass = self._environment.get_at(distance, "super")

        # "this" is always one level nearer than "super"'s environment.
        receiver = self._environment.get_at(distance - 1, "this")

        method = superclass.find_method(receiver, expr.method.lexeme)
        if method is None:
            raise RuntimeError(expr.method, "Undefined property '{}'.".format(expr.method.lexeme))

        return method

    def visit_this_expr(self, expr):
        return self._lookup_variable(expr.keyword, expr)

    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)

        ot = expr.operator.type
        if ot == TokenType.BANG:
            return not self._is_true(right)
        elif ot == TokenType.MINUS:
            self._check_number_operand(expr.operator, right)
            return -right

        # unreachable
        return None

    def visit_variable_expr(self, expr):
        return self._lookup_variable(expr.name, expr)

    def _lookup_variable(self, name, expr):
        distance = self.locs.get(expr)
        if distance is not None:
            return self._environment.get_at(distance, name.lexeme)
        else:
            return self.globs.get(name)

    def _check_number_operands(self, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return True

        raise RuntimeError(operator, "Operands must be numbers.")

    def _check_number_operand(self, left):
        # TODO for consistency, parameter "left" should be named "right"
        if isinstance(left, float):
            return True

        raise RuntimeError(operator, "Operand must be a number.")

    def _print(self, argument):
        print(self._stringify(argument))
        return argument

    def _clock(self, arguments):
        return time.time() * 1000

    def _is_true(self, obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def _is_equal(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def _stringify(self, obj):
        if obj is None:
            return "nil"

        return str(obj)
