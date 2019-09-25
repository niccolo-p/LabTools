
#  LabTools - significant_digit
#  Copyright 2019 Luca Arnaboldi

import math

"""
Convert x in a string written with p significant digit and the  exponent of the 
exponential notation.
If compact is True it retuens only a string. Example:
0.00345, 2, False --> ("3.4", -3)
0.00345, 2, True  --> "3.4e-3"

Code heavily ispired from https://github.com/randlet/to-precision
"""
def significant_digits(x, p, compact = False):
    x = float(x)

    if x == 0.:
        return "0." + "0"*(p-1)

    out = []

    if x < 0:
        out.append("-")
        x = -x

    e = int(math.log10(x))
    tens = math.pow(10, e - p + 1)
    n = math.floor(x/tens)

    if n < math.pow(10, p - 1):
        e = e - 1
        tens = math.pow(10, e - p+1)
        n = math.floor(x / tens)

    if abs((n + 1.) * tens - x) <= abs(n * tens -x):
        n = n + 1

    if n >= math.pow(10,p):
        n = n / 10.
        e = e + 1

    m = "%.*g" % (p, n)
    
    exp_notation = False

    if e < -2 or e >= p:
        out.append(m[0])
        if p > 1:
            out.append(".")
            out.extend(m[1:p])

        if compact:
            out.append('e')
            if e > 0:
                out.append("+")
            out.append(str(e))
        else:
            exp_notation = True
    elif e == (p - 1):
        out.append(m)
    elif e >= 0:
        out.append(m[:e+1])
        if e+1 < len(m):
            out.append(".")
            out.extend(m[e+1:])
    else:
        out.append("0.")
        out.extend(["0"]*-(e+1))
        out.append(m)
        
    if exp_notation:
        exponent = e
    else:
        exponent = 0

    if compact:
        return "".join(out)
    else:
        return "".join(out), exponent


"""
Return the exponent of themost significant digit of a number x
"""
def most_significant_digit(x):
    return int(math.floor(math.log10(abs(x))))



"""
Move the decimal separator of delta digits.
"""
def move_decimal(number, delta):
    float(number) # Check that number is representing a float
    
    if delta == 0:
        return number
        
    p = number.find('.')
    
    if delta > 0:
        ans = number[:p]
        if p + 1 + delta < len(number):
            ans += number[p + 1:p + 1 + delta]
            ans += "."
            ans += number[p + 1 + delta:len(number)]
        else:
            ans += number[p + 1:len(number)]
            ans += "0" * (p + 1 + delta - len(number))
        return ans
    else:
        if p + delta <= 0:
            ans = "0."
            ans += "0" * (-(p + delta))
            ans += number[:p] + number[p + 1:len(number)]
        else:
            ans = number[:p + delta]
            ans += "."
            ans += number[p + delta : p]
            ans += number[p + 1 : len(number)]
        return ans 


