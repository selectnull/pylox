class AstPrinter(object):
    def print(self, obj):
        """obj can be Stmt or Expr"""
        return obj.accept(self)

    def visit_block_stmt(self, stmt):
        return self._join("block", stmt.statements)

    def visit_class_stmt(self, stmt):
        s = []
        s.append("(class {}".format(stmt.name.lexeme))

        if stmt.superclass is not None:
            s.append(" < {}".format(self.print(stmt.superclass)))

        for method in stmt.methods:
            s.append(" " + self.print(method))

        s.append(")")

        return s.join("")

    def visit_function_stmt(self, stmt):
        s = []
        s.append("(fun {}(".format(stmt.name.lexeme))

        for param in stmt.parameters:
            if param != stmt.parameters.get(0):
                s.append(" ")
            s.append(param.lexeme)

        s.append(") {})".format(self._join(stmt.body)))
        return s.join("")

    def visit_if_stmt(self, stmt):
        if stmt.else_branch is None:
            return self._join("if", stmd.condition, "then", stmt.then_branch)
        return self._join("if", stmd.condition, "then", stmt.then_branch,
                          "else", stmt.else_branch)

    def visit_print_stmt(self, stmt):
        return self._join("print", stmt.expression)

    def visit_return_stmt(self, stmt):
        if stmt.value is None:
            return "(return)"
        return self._join("return", stmt.value)

    def visit_var_stmt(self, stmt):
        if stmt.initializer is None:
            return self._join("var", stmt.name.lexeme)
        return self._join("var", stmt.name.lexeme, "=", stmt.initializer)

    def visit_while_stmt(self, stmt):
        return self._join("while", stmt.condition, stmd.body)

    def vitit_assign_expr(self, expr):
        return self._join("=", expr.name.lexeme, expr.value)

    def visit_binary_expr(self, expr):
        return self._join(expr.operator, expr.left, expr.right)

    def visit_call_expr(self, expr):
        return self._join("call", expr.callee, expr.arguments)

    def visit_get_expr(self, expr):
        return self._join(".", expr.object, expr.name.lexeme)

    def visit_grouping_expr(self, expr):
        return self._join("group", expr.expression)

    def visit_literal_expr(self, expr):
        if isinstance(expr.value, str):
            escaped = expr.value.replace("\"", "\\\"")
            return "\"{}\"".format(escaped)
        return str(expr.value)

    def visit_logical_expr(self, expr):
        return self._join(expr.operator, expr.left, expr.right)

    def visit_set_expr(self, expr):
        return self._join("=", expr.object, expr.name.lexeme, expr.value)

    def visit_super_expr(self, expr):
        return self._join("super", expr.method)

    def visit_this_expr(self, expr):
        return "this"

    def visit_unary_expr(self, expr):
        return self._join(expr.operator, expr.right)

    def visit_variable_expr(self, expr):
        return expr.name.lexeme

    def _join(self, *parts):
        return ["(", self._add_parts(s, parts), ")"].join("")

    def _add_parts(self, builder, parts):
        for part  in parts:
            if len(builder) > 1 and builder[-1] != " ":
                builder.append(" ")

            if isinstance(part, (Stmt, Expr)):
                builder.append(self.print(part))
            elif isinstance(part, Token):
                builder.append(part.lexeme)
            elif isinstance(part, list):
                # TODO we should check for any iterable 
                # except string here. list is just quick hack
                self._add_parts(builder, part)
            else:
                builder.append(part)
