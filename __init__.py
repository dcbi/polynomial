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
		if isinstance(p, int) or isinstance(p, float):
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
			elif d1 > d2:
				return Polynomial(*c, *self._c[d:])
			else:
				return Polynomial(*c)
		else: raise TypeError

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
		if isinstance(p, int) or isinstance(p, float):
			return Polynomial(*tuple([ p*self._c[i] for i in range(len(self._c)) ]))
		elif isinstance(p, Polynomial):
			c = list()
			for i in range(self.degree() + p.degree() + 1):
				c.append(0)
			for i in range(len(self._c)):
				for j in range(len(p._c)):
					c[i+j] =  c[i+j] + self._c[i] * p._c[j]
			return Polynomial(*tuple(c))
		else: raise TypeError

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
		if isinstance(p,int) or isinstance(p,float): return (self._c[0] == p) and (self.degree() == 0)
		elif isinstance(p,Polynomial): return self._c == p._c
		else: return False

	def __ne__(self, p):
		return not self == p

	def __call__(self, x):
		y = self._c[0]
		for i in range(1,len(self._c)):
			y = y + self._c[i] * x ** i
		return 	y

	def derivative(self):
		c = list(self._c[1:])
		for i in range(len(c)):
			c[i] = c[i] * (i+1)
		return Polynomial(*tuple(c))

	def integral(self, const=0):
		c = [const] + list(self._c)
		for i in range(1,len(c)):
			c[i] = c[i] / i
		return Polynomial(*tuple(c))

	def __str__(self, order=False):
		s = str(self._c[0])
		for i in range(1, len(self._c)):
			if not self._c[i] == 0:
				if self._c[i] > 0:
					s = s + ' + '
					if self._c[i] == 1: s = s + self.var
					else: s = s + str(self._c[i]) + self.var
				else:
					s = s + ' - '
					if self._c[i] == -1: s = s + self.var
					else: s = s + str(self._c[i])[1:] + self.var

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
