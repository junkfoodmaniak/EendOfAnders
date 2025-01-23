#wajow
#!/usr/bin/env python3


class LambdaTerm:
    """Abstract Base Class for lambda terms."""

    def fromstring(self):
        """Construct a lambda term from a string."""
        raise NotImplementedError

    def substitute(self, rules):
        """Substitute values for keys where they occur."""
        raise NotImplementedError

    def reduce(self):
        """Beta-reduce."""
        raise NotImplementedError


class Variable(LambdaTerm):
    """Represents a variable."""

    def __init__(self, symbol):
        self.symbol=symbol

    def __repr__(self): raise NotImplementedError

    def __str__(self):
        return f'Variable({self.symbol})'

    def substitute(self, rules): raise NotImplementedError


class Abstraction(LambdaTerm):
    """Represents a lambda term of the form (λx.M)."""

    def __init__(self, variable, body):
        self.variable=variable
        self.body=body

    def __repr__(self): raise NotImplementedError

    def __str__(self):
        return f'Abstraction({self.variable},{self.body})'

    def __call__(self, argument): raise NotImplementedError

    def substitute(self, rules): raise NotImplementedError


class Application(LambdaTerm):
    """Represents a lambda term of the form (M N)."""

    def __init__(self, function, argument):
        self.function=function
        self.argument=argument

    def __repr__(self): raise NotImplementedError

    def __str__(self):
        return f'Application({self.function},{self.argument})'

    def substitute(self, rules):
        if type(self.function)!=Abstraction: #the function has to be an abstraction, or else substitution is not possible
            raise TypeError
        else:
            for i in range(len(function.body)):
                if self.function.body[i]==self.argument:
                    self.function[i]=self.argument
                    


    def reduce(self): raise NotImplementedError

    
    term=[[x], [], []]
    #(lambda x.[] y)

    #example:
    #[lambda[x], [x], [y]] gives y