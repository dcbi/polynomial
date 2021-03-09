# poly-ratio
Python classes for representing polynomial functions and rational numbers.

## Example Usage
### Polynomials
Create a Polynomial object by passing its coefficients:
```python
from polynomial import Polynomial

quadratic = Polynomial(1,0,-1)
print(quadratic)
#  1 - x^2
```

You can change the variable used in its string representation:
```python
quadratic.variable('z')
print(quadratic)
#  1 - z^2
```

Polynomial objects can be added, subtracted, and multiplied by each other or by numbers. They can also be raised to integer powers. For example:
```python
cubic = Polynomial(1,0,0,1)

print(2 * cubic + quadratic)
#  3 - 2x^2 + x^3

print(quadratic ** 2)
#  1 - 2x^2 + x^4
```

Notice that any operation between Polynomials returns a new one with the default variable name, 'x'. Change the default variable name by calling the class method:
```python
Polynomial.set_variables('z')
print(Polynomial(1,-1))
#  1 - z
```

You can find the degree of any Polynomial:
```python
p = cubic ** 3
p.degree()
#  9
```

Polynomials are essentially tuples. You can index, slice, or iterate over them:
```python
p[6]
#  3

p[3:7]
#  (3, 0, 0, 3)

for c_i in p:
  if not c_i == 0: print(c_i)
 #  1
 #  3
 #  3
 #  1
```

Polynomials are also functions:
```python
cubic(2)
#  9
```

You can take the derivative and anti-derivative of Polynomials:
```python
print(cubic.derivative())
#  3z^2

linear = Polynomial(0,1)
print( linear.integral() )
#  0.5z^2
```

You can specify the constant of integration by passing it as an argument. By default it is zero. Since Polynomials are also functions, the `.integral()` method lets you easily calculate the definite integral:
```python
linear.integral()(1) - linear.integral()(0)
#  0.5
```
### Rationals
Create a Rational by passing its numerator and denominator:
```python
from rational import Rational
half = Rational(1,2)
```

Rationals automatically simplify to their reduced form upon creation. Negative signs are also placed in the numerator.
```python
Rational(9,-27)
#  (-1 / 3)
```

You can do most algebraic operations between Rationals, or between Rationals and integers (the result of which will be a Rational type). The exception is raising a Rational to a non-integer power, which will return a float. Algebraic operations between Rationals and floats will always return a float.

Rationals can also be used alongside Polynomials. They can be added, subtracted, and multiplied together. The result is always a Polynomial. You can only divide Polynomials by Rationals (not the other way around) and Polynomials cannot be raised to a power of Rational.
