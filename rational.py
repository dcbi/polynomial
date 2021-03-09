class Rational():

    def __init__(self,numerator,denominator,reduce=True):
        if reduce: self.up, self.down = self.__reduce__(numerator, denominator)
        else: self.up, self.down = numerator, denominator

    def __reduce__(self, a, b):
        d = gcd(a,b)
        up = int(a//d)
        down = int(b//d)
        if b < 0: return -up, -down
        else: return up, down

    def __float__(self):
        return self.up / self.down

    def __int__(self):
        return int(self.__float__())

    def __add__(self, p):
        if isinstance(p, float):
            return self.__float__() + p
        elif isinstance(p, int):
            return  Rational( p * self.down + self.up, self.down )
        elif isinstance(p,  Rational):
            return  Rational( self.up * p.down + p.up * self.down, self.down * p.down )
        elif isinstance(p,Polynomial):
            return p.__add__(self)
        else: raise TypeError

    def __radd__(self,p):
        return self.__add__(p)

    def __neg__(self):
        return Rational(-self.up, self.down, False)

    def __sub__(self,p):
        return -p + self

    def __rsub__(self,p):
        return (-self).__add__(p)

    def __mul__(self, p):
        if isinstance(p, float):
            return self.__float__() * p
        elif isinstance(p, int):
            return Rational( p*self.up, self.down )
        elif isinstance(p,  Rational):
            return Rational( self.up * p.up, self.down * p.down )
        elif isinstance(p, Polynomial):
            return p.__mul__(self)
        else: raise TypeError

    def __rmul__(self,p):
        return self.__mul__(p)

    def __truediv__(self,p):
        if isinstance(p,int): return Rational(self.up , self.down * p)
        elif isinstance(p, float): return self.__float__() / p
        elif isinstance(p, Rational): return Rational(self.up * p.down, self.down * p.up)
        else: raise TypeError

    def __rtruediv__(self,p):
        if isinstance(p,int): return Rational( p * self.down, self.up )
        elif isinstance(p,float): return p / self.__float__()
        elif isinstance(p, Polynomial): p.__mul__(1 / self)
        else: raise TypeError

    def __pow__(self, n):
        if isinstance(n,int):
            if n == 0: return Rational(1,1,False)
            elif n == 1: return self
            elif n < 0: return Rational(self.down , self.up).__pow__(-n)
            else: return Rational( self.up ** n , self.down ** n )
        elif isinstance(n,float):
            return  self.__float__() ** n
        elif isinstance(n,Rational):
            return  self.__float__() ** n.__float__()
        else: raise TypeError

    def __eq__(self, p):
        if isinstance(p,(int,float)): return p == self.__float__()
        elif isinstance(p, Rational): return (self.up == p.up) and (self.down == p.down)
        else: return p.__eq__(self)

    def __ne__(self, p):
        return not self == p

    def __lt__(self,p):
        if isinstance(p,(int,float)): return self.__float__() < p
        elif isinstance(p, Rational): return self.__float__() < p.__float__()
        else: return TypeError

    def __le__(self,p):
        if isinstance(p,(int,float)): return self.__float__() <= p
        elif isinstance(p, Rational): return self.__float__() <= p.__float__()
        else: return TypeError

    def __ge__(self,p):
        if isinstance(p,(int,float)): return self.__float__() >= p
        elif isinstance(p, Rational): return self.__float__() >= p.__float__()
        else: return TypeError

    def __str__(self, order=False):
        if self.down == 1: return str(self.up)
        s = '('
        if self.down < 0:
            if self.up < 0: s = s + str(self.up)[1:]
            else: s = s + '-' + str(self.up)
            s = s + ' / ' + str(self.down)[1:]
        else: s = s + str(self.up) + ' / ' + str(self.down)
        return s + ')'

    def __repr__(self):
        return str(self)

    def __getitem__(self, key):
        return (self.up, self.down)[key]

    @staticmethod
    def convert(x):
        if isinstance(x, int): return Rational(x,1,False)
        elif isinstance(x, float):
            y = x
            r = x - int(x)
            d =  10
            while not r == 0:
                y = y * d
                r = y - int(y)
                d = d * 10
            return Rational(int(y),d)
        elif isinstance(x, str):
            y = x.strip('(').strip(')')
            m = y.split('/')
            n,d = int(m[0].strip()) , int(m[1].strip())
            return Rational(n,d,False)
        else: raise TypeError
