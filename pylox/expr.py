class Expr(object):
    pass

class Assign(Expr):
    def __init__(self, name, value):
        """ name is Token, value is Expr"""
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign_expr(self)


class Binary(Expr):
    def __init__(self, left, operator, right):
        """ left and right are Expr, operator is Token"""
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)


class Call(Expr):
    def __init__(self, callee, paren, arguments):
        """ callee is Expr, paren is Token, arguments is list of Expr"""
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_call_expr(self)


class Get(Expr):
    def __init__(self, obj, name):
        """ obj is Expr, name is Token"""
        self.object = obj
        self.name = name

    def accept(self, visitor):
        return visitor.visit_get_expr(self)


class Grouping(Expr):
    def __init__(self, expression):
        """ expression is Expr"""
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)


class Literal(Expr):
    def __init__(self, value):
        """ value is object"""
        self.value = values

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)


class Logical(Expr):
    def __init__(self, left, operator, right):
        """ left and right are Expr, operator is Token"""
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_logical_expr(self)


class Set(Expr):
    def __init__(self, obj, name, value):
        """ obj is Expr, name is Token, value is Expr"""
        self.object = obj
        self.name = name
        self.value = values

    def accept(self, visitor):
        return visitor.visit_set_expr(self)


class Super(Expr):
    def __init__(self, keyword, method):
        """ keyword and method are Token"""
        self.keyword = keyword
        self.method = method

    def accept(self, visitor):
        return visitor.visit_super_expr(self)


class This(Expr):
    def __init__(self, keyword):
        """ keyword is Token"""
        self.keyword = keyword

    def accept(self, visitor):
        return visitor.visit_this_expr(self)


class Unary(Expr):
    def __init__(self, operator, right):
        """ operator is Token, right is Expr"""
        self.operator = operator
        self.right right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)


class Variable(Expr):
    def __init__(self, name):
        """ name is Token"""
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)
