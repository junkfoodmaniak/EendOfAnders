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
        def splitintolist(self): #make a list containing the variable, the function and the argument of the input
            easierlist=[]
            for i in range(len(self)):
                if self[i]=='λ': #if any element in the input term is labda:
                    self=self[(i+1):]
                break

            firstelement=''
            for j in range(len(self)):
                if self[j]!='.':
                    firstelement+=self[j]
                else:
                    easierlist.append(firstelement)
                    self=self[(j+1):]
                    break

            spaceindex=-1
            openingbracketindex=-1
            closingbracketindex=-1
            for k in range(len(self)-1,-1,-1):
                if self[k]=='(':
                    openingbracketindex=k
                elif self[k]==')':
                    closingbracketindex=k
                elif self[k]==' ' and (k<openingbracketindex or closingbracketindex==-1):
                    spaceindex=k
                    break
                else:
                    pass

            secondelement=''
            thirdelement=''
            if spaceindex!=-1:
                for l in range(0,spaceindex):
                    secondelement+=self[l]
                easierlist.append(secondelement)
                for m in range(spaceindex+1,len(self)):
                    thirdelement+=self[m]
                easierlist.append(thirdelement)
                return reduceonce(easierlist)
            else:
                return -1
        
        def reduceonce(easierlist): #beta-reduces self once, given the list of three elements (easierlist)

            if len(easierlist[2])==0: #if the lambda term is missing an argument
                return -1

            variable=easierlist[0]
            function=easierlist[1]
            argument=easierlist[2]

            lengthofvariable=len(variable) #if equal to variable, replace with argument
            output=''
            for n in function:
                if n[:lengthofvariable]==variable:
                    output+=argument
                else:
                    output+=n[:lengthofvariable]
            return output

        def bracketsgofirst(self): #find lambda terms in brackets and reduce them to normal form
            for o in range(0,len(self)-1):
                if o==len(self)-1:
                    break
                elif self[o]=='(' and self[o+1]=='λ':
                    closingbracketindex=-1
                    tobereduced=''
                    amountofopeningbrackets=1
                    amountofclosingbrackets=0
                    for p in range(o+1,len(self)):
                        if self[p]==')':
                            amountofclosingbrackets+=1
                            if amountofclosingbrackets==amountofopeningbrackets:
                                closingbracketindex=p
                                break
                        elif self[p]=='(':
                            amountofopeningbrackets+=1
                        else:
                            pass
                    for q in range(o+1,closingbracketindex):
                        tobereduced+=self[q]
                    while 'λ' in tobereduced: #while the term in brackets is a lambdaterm
                        outcome=splitintolist(tobereduced)
                        if outcome==-1:
                            break
                        else:
                            tobereduced=outcome

                    self=self[:o]+tobereduced+self[closingbracketindex+1:]

                else:
                    pass
            return self

        def reduceloop(self):
            while 'λ' in self:
                if splitintolist(self)==-1:
                    break
                else:
                    self=splitintolist(self)
            return self

        self=bracketsgofirst(self)
        self=reduceloop(self)

        while self[0]=='(':
            self=self.strip('()')

        return self

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