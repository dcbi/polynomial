class Polynomial():
    _var = 'x'

    @classmethod
    def set_variables(cls, y):
        cls._var = y

    def __init__(self, *c):
        self._c = c
        if self._c[-1] == 0: self._truncate()
        self.var = self._var

    def _truncate(self):
        c = list(self._c)
        while c[-1] == 0:
            if len(c) == 1: break
            c.pop()
        self._c = tuple(c)

    def variable(self, y):
        self.var = y

    def degree(self):
        return len(self._c) - 1

    def __add__(self, p):
        if isinstance(p, (int,float,Rational)):
            return Polynomial(p+self._c[0], *self._c[1:])
        elif isinstance(p, Polynomial):
            d1 = len(self._c)
            d2 = len(p._c)
            d = min(d1,d2)
            c = list()
            for i in range(d):
                c.append(self._c[i]+p._c[i])
            c = tuple(c)
            if d1 < d2:
                return Polynomial(*c, *p._c[d:])
            elif d2 < d1:
                return Polynomial(*c, *self._c[d:])
            else:
                return Polynomial(*c)
        else: return p.__add__(self)

    def __radd__(self,p):
        return self.__add__(p)

    def __neg__(self):
        c = list(self._c)
        for i in range(len(c)):
            c[i] = -c[i]
        return Polynomial(*tuple(c))

    def __sub__(self,p):
        return -p + self

    def __rsub__(self,p):
        return (-self).__add__(p)

    def __mul__(self, p):
        if isinstance(p, (int,float,Rational)):
            return Polynomial(*tuple([ p*self._c[i] for i in range(len(self._c)) ]))
        elif isinstance(p, Polynomial):
            c = list()
            for i in range(self.degree() + p.degree() + 1):
                c.append(0)
            for i in range(len(self._c)):
                for j in range(len(p._c)):
                    c[i+j] =  c[i+j] + self._c[i] * p._c[j]
            return Polynomial(*tuple(c))
        else: p.__mul__(self)

    def __rmul__(self,p):
        return self.__mul__(p)

    def __pow__(self, n):
        if n == 0: return Polynomial(1)
        elif n == 1: return self
        else:
            if n < 0 or isinstance(n, float): return lambda x: self(x) ** n
            else:
                result = self
                for i in range(1,n): result = result * self
                return result

    def __eq__(self, p):
        if isinstance(p,(int,float,Rational)): return (self._c[0] == p) and (self.degree() == 0)
        elif isinstance(p,Polynomial): return self._c == p._c
        else: return False

    def __ne__(self, p):
        return not self == p

    def __call__(self, x):
        y = self._c[0]
        for i in range(1,len(self._c)):
            y = y + self._c[i] * x ** i
        return  y

    def derivative(self):
        c = list(self._c[1:])
        for i in range(len(c)):
            c[i] = c[i] * (i+1)
        return Polynomial(*tuple(c))

    def integral(self, const=0):
        c = [const] + list(self._c)
        for i in range(2,len(c)):
            c[i] = c[i] / i
        return Polynomial(*tuple(c))

    def __str__(self, order=False):
        s = str(self._c[0])
        for i in range(1, len(self._c)):
            C = self._c[i]
            if not C == 0:
                if not C <= 0:
                    s = s + ' + '
                    if C == 1: s = s + self.var
                    else: s = s + str(C) + self.var
                else:
                    s = s + ' - '
                    if C == -1: s = s + self.var
                    s = s + str(-C) + self.var

                if not i == 1: s = s + '^' + str(i)

        if self._c[0] == 0 and self.degree() > 0:
            j = s.index(' ')
            return s[j+3:]

        else: return s

    def __repr__(self):
        return 'Polynomial' + str(self._c)

    def __iter__(self):
        return polyiter(self)

    def __getitem__(self, key):
        return self._c[key]

class polyiter():
    def __init__(self, poly):
        self.poly = poly
        self.index = 0
    def __next__(self):
        if self.index < len(self.poly._c):
            result = self.poly._c[self.index]
            self.index += 1
            return result
        else: raise StopIteration

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
