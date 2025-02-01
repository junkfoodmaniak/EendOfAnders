#wajow
#!/usr/bin/env python3


class LambdaTerm:
    """Abstract Base Class for lambda terms."""
    def fromstring(self):

        easierlist=[] #remove the lambda from the start of the lambda term (self)
        for i in range(len(self)):
            if self[i]=='λ': #if the element of lambda in self is i,
                self=self[(i+1):] #change self into a list with only the indexes greater than i,
                break #so that the lambda will be removed.
            else:
                pass #here, easierlist will be a list that looks like ['Variable', 'Function(body)', 'Argument'].

        firstelement='' #this loop will create the first element, the variable, of the lambda term
        dotindex=-1 #(if dotindex stays -1, there isn't any dot in the lambda term so it is only a variable)
        for j in range(len(self)):
            if self[j]!='.': #from the (new) start of self to the first dot will be the variable
                firstelement+=self[j] #so every element found between start and dot will be added to
            elif self[j]=='.':
                dotindex=j #the first element of the list that will be appended to easierlist (as the variable)
                self=self[(j+1):] #if self[j] is a dot, then self will be changed into a list with only
                break #the indexes greater than j.
        if dotindex!=-1:
            easierlist.append(firstelement) #In this last step, if there was a dot in the lambdaterm,
        else: #so if dotindex==-1, the first element is just appended to easierlist.
            easierlist.append(self) #But if there wasn't a dot, self can already be seen as a variable,
            self='' #so then self is appended to easierlist instead of firstelement
        

        spaceindex=-1 #Most confusing step of all! <3
        openingbracketindex=-1
        closingbracketindex=-1 #From the end of the list to the start of the list, this loop will
        for k in range(len(self)-1,-1,-1): #try to find spaces, so that everything before this space is the
            if self[k]=='(': #function, or body, and everything after this space is the argument
                openingbracketindex=k
            elif self[k]==')': #There was the problem that the argument in a lambda term can have a space
                closingbracketindex=k #hidden inside of it. An argument that looks like (x x), for example.
            elif self[k]==' ' and (k<openingbracketindex or closingbracketindex==-1):
                spaceindex=k #that is why I also added thingies that note down the latest opening- and closing
                break #bracket indexes. Now a new space index will only be "noted" if this index is smaller
            else: #than the index of the latest '(' or if there isn't any ')' to be found, so if it isn't
                pass #possible for the space to be between brackets.

        secondelement=''
        thirdelement=''
        if spaceindex!=-1: #If spaceindex!=-1, so if there is a space in the lambda term
            for l in range(0,spaceindex): #from the start of self to the spaceindex,
                secondelement+=self[l] #add each element to the second element
            for m in range(spaceindex+1,len(self)): #from the spaceindex to the end of self,
                thirdelement+=self[m] #add each element to the third element
        else: #if spaceindex==-1, so if there isn't any space in the lambdaterm,
            for n in range(len(self)): 
                secondelement+=self[n] #Add each element of self to the second element
        easierlist.append(secondelement)
        easierlist.append(thirdelement) #add both elements to easierlist, even if they are empty

        if ' ' in easierlist[0]: #if the "variable" has the form (x y), return
            easierlist[0]=easierlist[0].strip('()').split(" ") #Application(Variable('x'),Variable('y'))
            return f'Application(Variable({easierlist[0][0]}),Variable({easierlist[0][1]}))'

        if len(easierlist[0])!=0 and len(easierlist[1])==0 and len(easierlist[2])==0:
            return f'Variable({easierlist[0]})'
        elif len(easierlist[0])!=0 and len(easierlist[1])!=0 and len(easierlist[2])==0:
            return f'Abstraction({LambdaTerm.fromstring(easierlist[0])},{LambdaTerm.fromstring(easierlist[1])})'
        elif len(easierlist[0])!=0 and len(easierlist[1])!=0 and len(easierlist[2])!=0:
            return f'Application(Abstraction({LambdaTerm.fromstring(easierlist[0])},{LambdaTerm.fromstring(easierlist[1])}),{LambdaTerm.fromstring(easierlist[2])})'
        #this last part is a recursive formula, which I explained in WhatsApp

    def substitute(self, rules):
        """Substitute values for keys where they occur."""
        #we don't have to implement this one because all possible forms of lambdaterm heb a substitute function of their own so if all goes well, this function never gets called.
        raise NotImplementedError

    def reduce(self):
        """Beta-reduce."""
        #Same thing as for substitution.
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
        return f'λ{self.variable}.{self.body}'

    def __call__(self, argument):
        rules={self.variable:argument}
        self2=self.body.substitute(rules)
        return self2

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
        self2=Application(self.function.reduce(),self.argument)
        if type(self2.function)==Abstraction:
            rules={self2.function.variable:self2.argument}
            self3=self2.function.body.substitute(rules)
            self3.reduce()
            return self3
        else:
            self3=Application(self2.function,self.argument.reduce())
            return self3