from loxinstance import LoxInstance


class LoxClass(object):
    # should implement Callable interface
    def __init__(self, name, superclass, methods):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def find_method(self, instance, name):
        klass = self
        while (klass is not None):
            if name in klass.methods:
                return klass.methods[name].bind(instance)

            klass = klass.superclass

        return None

    def __str__(self):
        return self.name

    def required_arguments(self):
        initializer = self.methods.get('init')
        if initializer is None:
            return 0
        return initializer.required_arguments()

    def call(interpreter, arguments):
        instance = LoxInstance(self)

        initializer = self.methods.get('init')
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)

        return instance
