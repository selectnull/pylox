class Parser(object):
    def __init__(self, tokens):
        self.synchronizing = set({
            TokenType.LEFT_BRACE, TokenType.RIGHT_BRACE, TokenType.RIGHT_PAREN,
            TokenType.EQUAL, TokenType.SEMICOLON})
        self.tokens = tokens
        self.current_index = 0

    def parse_program(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())

        return statements

    def parse_expression(self):
        return self.assignment()

    def declaration(self):
        if self.match(TokenType.CLASS):
            return self.class_declaration()
        if self.match(TokenType.FUN):
            return self.function("function")
        if self.match(TokenType.VAR):
            return self.var_declaration()

        return self.statement()

    def class_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect class name.")
        superclass = None
        if self.match(TokenType.LESS):
            self.consume(TokenType.IDENTIFIER, "Expect superclass name.")
            superclass = Variable(self.previous())

        methods = []
        self.consume(TokenType.LEFT_, "Expect '{' before class body.")

        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            methods.append(self.function("method"))

        self.consume(TokenType.RIGHT_BRACE, "Expet '}' after class body.")

        return Class(name, superclass, methods)

    def statement(self):
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.RETURN):
            return self.return_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.check(TokenType.LEFT_BRACE):
            return Block(self.block())

        return self.expression_statement()

    def for_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        initializer = None
        if self.match(TokenType.SEMICOLON):
            pass
        elif self.match(TokenType.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()

        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = Expression(self.parse_expression())
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body = self.statement()

        # desugar to while loop
        if increment is not None:
            body = Block([body, increment])

        if condition is None:
            condition = Literal(True)
        body = While(condition, body)

        if initializer is not None:
            body = Block([initializer, body])

        return body

    def if_statement(self):
        self.consume(LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.parse_expression()
        self.consume(RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = statement()

        return If(condition, then_branch, else_branch)

    def print_statement(self):
        value = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def return_statement(self):
        keyword = self.previous()
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.parse_expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return Return(keyword, value)

    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.parse_expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")

        return Var(name, initializer)

    def while_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.parse_expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()

        return While(condition, body)

    def expression_statement(self):
        expr = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)

    def function(self, kind):
        name = self.consume(TokenType.IDENTIFIER, "Expect {} name.".format(kind))
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after {} name.".format(kind))
        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(parameters) >= 8:
                    self.error("Cannot have more than 8 parameters.")

                parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))

                if not self.match(TokenType.COMMA):
                    break
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")

            body = self.block()
            return Function(name, parameters, body)

        def block(self):
            self.consume(TokenType.LEFT_BRACE, "Expect '{' before block.")
            statements = []

            while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
                statements.append(self.declaration())

            self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")

            return statements

        def assignment(self):
            expr = self.or_()

            if self.match(TokenType.EQUAL):
                equals = self.previous()
                value = self.assignment()

                if isinstance(expr, Variable):
                    return Assign(expr.name, value)
                elif isinstance(expr, Get):
                    return Set(expr.object, expr.name, value)

                Lox().error(equals, "Invalid assignment target.")

            return expr

        def or_(self):
            expr = self.and_()

            while self.match(TokenType.OR):
                operator = self.previous()
                right = self.and_()
                expr = Logical(expr, operator, right)

            return expr

        def and_(self):
            expr = self.equality()

            while self.match(TokenType.AND):
                operator = self.previous()
                right = self.equality()
                expr = Logical(expr, operator, right)

            return expr

        def equality(self):
            expr = self.comparison()

            while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
                operator = self.previous()
                right = self.comparison()
                expr = Binary(expr, operator, right)

            return expr

        def comparison(self):
            expr = self.term()

            matches = (TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL)
            while self.match(*matches):
                operator = self.previous()
                right = term()
                expr = Binary(expr, operator, right)

            return expr

        def term(self):
            expr = self.factor()

            while self.match(TokenType.MINUS, TokenType.PLUS):
                operator = self.previous()
                right = self.factor()
                expr = Binary(expr, operator, right)

            return expr

        def factor(self):
            expr = self.unary()

            while self.match(TokenType.SLASH, TokenType.STAR):
                operator = self.previous()
                right = self.unary()
                expr = Binary(expr, operator, right)

            return expr

        def unary(self):
            if self.match(TokenType.BANG, TokenType.MINUS):
                operator = self.previous()
                right = self.unary()
                return Unary(operator, right)

            return self.call()

        def finish_call(self, callee):
            arguments = []
            if not self.check(TokenType.RIGHT_PAREN):
                while True:
                    if len(arguments) >= 8:
                        self.error("Cannot have more than 8 arguments.")

                    arguments.append(self.parse_expression())
                    if not self.match(TokenType.COMMA):
                        break

            paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")

            return Call(callee, paren, arguments)

        def call(self):
            expr = self.primary()

            while True:
                if self.match(TokenType.LEFT_PAREN):
                    expr = self.finish_call(expr)
                elif self.match(TokenType.DOT):
                    name = self.consume(TokenType.IDENTIFIER, "Expect property name after '.'.")
                    expr = Get(expr, name)
                else:
                    break

            return expr

        def primary(self):
            if self.match(TokenType.FALSE):
                return Literal(False)
            if self.match(TokenType.TRUE):
                return Literal(True)
            if self.match(TokenType.NIL):
                return Literal(None)

            if self.match(TokenType.NUMBER, TokenType.STRING):
                return Literal(self.previous().literal)

            if self.match(TokenType.SUPER):
                keyword = self.previous()
                self.consume(TokenType.DOT, "Expect '.' after 'super'.")
                method = self.consume(TokenType.IDENTIFIER, "Expect superclass method name.")
                return Super(keyword, method)

            if self.match(TokenType.THIS):
                return This(self.previous())

            if self.match(TokenType.IDENTIFIER):
                return Variable(self.previous())

            if self.match(TokenType.LEFT_PAREN):
                expr = self.parse_expression()
                self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
                return Grouping(expr)

            self.error("Expect expression.")

            # discard the token so we can make progress
            self.advance()
            return None

        def match(self, *token_types):
            for tt in token_types:
                if self.check(tt):
                    self.advance()
                    return True

            return False

        def consume(self, token_type, message):
            if self.check(token_type):
                return self.advance()

            self.error(message)

            if token_type not in self.synchronizing:
                return None

            while not self.check(token_type) and not self.is_at_end():
                self.advance()

            return self.advance()

        def advance(self):
            if not self.is_at_end():
                self.current_index += 1
            return self.previous()

        def check(self, token_type):
            if self.is_at_end():
                return False
            return self.current().type == token_type

        def is_at_end(self):
            return self.current().type == TokenType.EOF

        def current(self):
            return self.tokens[self.current_index]

        def previous(self):
            return self.tokens[self.current_index-1]

        def error(self, message):
            Lox().error(self.current(), message)
