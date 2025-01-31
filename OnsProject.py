#wajow
#!/usr/bin/env python3


class LambdaTerm:
    """Abstract Base Class for lambda terms."""

    def fromstring(self):
        """Construct a lambda term from a string."""
        raise NotImplementedError

    def substitute(self, rules):
        """Substitute values for keys where they occur."""
        #we don't have to implement this one because all possible forms of lambdaterm heb a substitute function of their own so if all goes well, this function never gets called.
        raise NotImplementedError

    def reduce(self):
        """Beta-reduce."""
        #Same thing as for substitution
        raise NotImplementedError

class Variable(LambdaTerm):
    """Represents a variable."""

    def __init__(self, symbol):
        self.symbol=symbol

    def __repr__(self):
        return f'Variable({self.symbol})'

    def __str__(self):
        return f'{self.symbol}'

    def substitute(self, rules):
        if self.symbol in rules:
            self.symbol=rules[self.symbol]
        return self
    
    def reduce(self):
        return self
    


class Abstraction(LambdaTerm):
    """Represents a lambda term of the form (λx.M)."""

    def __init__(self, variable, body):
        self.variable=variable
        self.body=body

    def __repr__(self):
        return f'Abstraction({repr(self.variable)},{repr(self.body)})'

    def __str__(self):
        return f'(λ{self.variable}.{self.body})'

    def __call__(self, argument):
        rules={self.variable:argument}
        self2=self.body.substitute(rules)
        return

    def substitute(self, rules):
        if self.variable in rules:
            return self
        else:
            self2=Abstraction(self.variable,self.body.subtitute(rules))
            return self2
    
    def reduce(self):
        self2=Abstraction(self.variable, self.body.reduce())
        return self2
        



class Application(LambdaTerm):
    """Represents a lambda term of the form (M N)."""

    def __init__(self, function, argument):
        self.function=function
        self.argument=argument

    def __repr__(self):
        return f'Application({repr(self.function)},{repr(self.argument)})'

    def __str__(self):
        return f'({self.function} {self.argument})'

    def substitute(self, rules):
        self2=Application(self.function.substitute(rules),self.argument.substitute(rules))
        return self2
    
    def reduce(self):
        self2=Application(self.function.reduce(),self.argument.reduce())
        if type(self2.function)==Abstraction:
            rules={self2.function.variable:self2.argument}
            self3=self2.function.body.substitute(rules)
            return self3
        else:
            return self2
        

print(Application(Abstraction(Variable("x"),Variable("x")),Variable("x")).reduce())