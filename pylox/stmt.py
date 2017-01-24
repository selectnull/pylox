class Stmt(object):
    pass


class Block(Stmt):
    def __init__(self, statement):
        """ statements is list of Stmt"""
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)


class Class(Stmt):
    def __init__(self, name, superclass, methods):
        """ name is Token, superclass is Expr, methods is list of Function"""
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def accept(self, visitor):
        return visitor.visit_class_stmt(self)


class Expression(Stmt):
    def __init__(self, expression):
        """ expression is Expr"""
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)


class Function(Stmt):
    def __init__(self, name, parameters, body):
        """ name is Token, parameters is list of Tokens, body is list of Stmt"""
        self.name = name
        self.parameters = parameters
        self.body = body

    def accept(self, visitor):
        return visitor.visit_function_stmt(self)


class If(Stmt):
    def __init__(self, condition, then_branch, else_branch):
        """ condition is Expr, then_branch and else_branch are Stmt"""
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if_stmt(self)


class Print(Stmt):
    def __init__(self, expression):
        """ expression is Expr"""
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)


class Return(Stmt):
    def __init__(self, keyword, value):
        """ keyword is Token, value is Expr"""
        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        return visitor.visit_return_stmt(self)


class Var(Stmt):
    def __init__(self, name, initializer):
        """ name is Token, initializer is Expr"""
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_var_stmt(self)


class While(Stmt):
    def __init__(self, condition, body):
        """ condition is Expr, body is list of Stmt"""
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_stmt(self)
