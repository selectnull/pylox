from enum import Enum, auto


class Resolver(object):

    class FunctionType(Enum):
        NONE = auto()
        FUNCTION = auto()
        METHOD = auto()
        INITIALIZER = auto()

    class ClassType(Enum):
        NONE = auto()
        CLASS = auto()
        SUBCLASS = auto()

    def __init__(self):
        self.scopes = Stack()
        self.locs = {}
        self.current_function = FunctionType.NONE
        self.current_class = ClassType.NONE

    def resolve(self, statements):
        for statement in statements:
            self._resolve(statement)

        return self.locs

    def visit_block_stmt(self, stmt):
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()
        return None

    def visit_class_stmt(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)

        enclosing_class = self.current_class
        self.current_class = ClassType.CLASS

        if stmt.superclass is not None:
            self.current_class = ClassType.SUBCLASS
            self._resolve(stmt.superclass)
            self.begin_scope()
            self.scopes.peek().put("super", true)

        for method in stmt.methods:
            self.begin_scope()
            self.scopes.peek().put("this", true)

            declaration = FunctionType.METHOD
            if method.name.lexeme == "init":
                declaration = FunctionType.INITIALIZER

            self.resolve_function(method, declaration)
            self.end_scope()

        if current_class == ClassType.SUBCLASS:
            self.end_scope()

        self.current_class = enclosing_class
        return None

    def visit_function_stmt(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolve_function(stmt, FunctionType.FUNCTION)
        return None

    def visit_if_stmt(self, stmt):
        self._resolve(stmt.condition)
        self._resolve(stmt.then_branch)
        if stmt.else_branch is not None:
            self._resolve(stmt.else_branch)
        return None

    def visit_print_stmt(self, stmt):
        self._resolve(stmt.expression)
        return None

    def visit_return_stmt(self, stmt):
        if self.current_function == FunctionType.NONE:
            Lox().error(stmt.keyword, "Cannot return from top-level code.")

        if stmt.value is not None:
            if self.current_function == FunctionType.INITIALIZER:
                Lox().error(stmt.keyword, "Cannot return a value from an initializer.")
            self._resolve(stmt.value)

        return None

    def visit_var_stmt(self, stmt):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self._resolve(stmt.initializer)
        self.define(stmt.name)
        return None

    def visit_while_stmt(self, stmt):
        self._resolve(stmt.condition)
        self.resolve(stmt.body)
        return None

    def visit_assign_expr(self, expr):
        self._resolve(expr.value)
        self._resolve_local(expr, expr.name)
        return None

    def visit_binary_expr(self, expr):
        self._resolve(expr.left)
        self._resolve(expr.right)
        return None

    def visit_call_expr(self, expr):
        self._resolve(expr.callee)

        for arg in expr.arguments:
            self._resolve(arg)

        return None

    def visit_get_expr(self, expr):
        self._resolve(expr.object)
        return None

    def visit_grouping_expr(self, expr):
        self._resolve(expr.expression)
        return None

    def visit_literal_expr(self, expr):
        return None

    def visit_logical_expr(self, expr):
        self._resolve(expr.left)
        self._resolve(expr.right)
        return None

    def visit_set_expr(self, expr):
        self._resolve(expr.value)
        self._resolve(expr.object)
        return None

    def visit_super_expr(self, expr):
        if self.current_class == ClassType.NONE:
            Lox().error(expr.keyword, "Cannot use 'super' outside of a class.")
        elif self.current_class is not ClassType.SUBCLASS:
            Lox().error(expr.keyword, "Cannot use 'super' in a class with no superclass.")
        else:
            self._resolve_local(expr, expr.keyword)
        return None

    def visit_this_expr(self, expr):
        if self.current_class == ClassType.NONE:
            Lox().error(expr.keyword, "Cannot use 'this' outside of a class.")
        else:
            self._resolve_local(expr, expr.keyword)
        return None

    def visit_unary_expr(self, expr):
        self._resolve(expr.right)
        return None

    def visit_variable_expr(self, expr):
        if not self.scopes.is_empty() and self.scopes.peek().get(expr.name.lexeme) == False:
            Lox().error(expr.name, "Cannot read local variable in its own initializer.")

        self._resolve_local(expr, expr.name)
        return None

    def _resolve(self, expr_or_stmt):
        expr_or_stmt.accept(self)

    def resolve_function(self, function, function_type):
        enclosing_function = self.current_function
        self.current_function = function_type

        self.begin_scope()
        for param in function.parameters:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.end_scope()

        self.current_function = enclosing_function

    def begin_scope(self):
        self.scopes.push({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name):
        if self.scopes.is_empty():
            return None

        scope = scopes.peek()
        if name.lexeme in scope:
            Lox().error(name, "Variable with this name already declared in this scope.")

        scope[name.lexeme] = False

    def define(self, name):
        if self.scopes.is_empty():
            return None

        self.scopes.peek()[name.lexeme] = True

    def _resolve_local(self, expr, name):
        i = self.scopes.size() - 1
        while i >= 0:
            if name.lexeme in self.scopes.get(i):
                self.locs[expr] = self.scopes.size() - 1 - i;
                return None

        # not found, assume it is global
