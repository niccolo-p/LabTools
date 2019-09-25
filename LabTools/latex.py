
#  LabTools - latex.py
#  Copyright 2019 Luca Arnaboldi

from .utils import significant_digits, move_decimal, most_significant_digit

DEFAULT_SIGNIFICANT_DIGITS = 4
DEFAULT_UNC_DIGITS = 2


class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def setvalue(self, value):
        self.value = value

    def setname(self, name):
        self.name = name

    def latexcode(self):
        return '\\newcommand{{\\{0}}}{{{1}}}'.format(
            self.name,
            str(self.value),
        )


class Decimal(Variable):
    """
        It needs Latex Package siunitx to work properly.
    """
    def __init__(self, name, value, digits=DEFAULT_SIGNIFICANT_DIGITS):
        super().__init__(name, float(value))
        self.digits = digits

    def setdigits(self, digits):
        self.digits = digits

    def latexcode(self, ):
        return '\\newcommand{{\\{0}}}{{{1}}}'.format(
            self.name,
            significant_digits(self.value, self.digits, True),
        )


class UDecimal(Variable):
    """
    It needs Latex Package siunitx to work properly.
    """

    def __init__(self, name, value, unc, unc_digit=DEFAULT_UNC_DIGITS):
        super().__init__(name, float(value))
        self.unc = float(unc)
        self.unc_digit = int(unc_digit)

    def setunc(self, unc):
        self.unc = float(unc)

    def setuncdigit(self, unc_digit):
        self.unc_digit = int(unc_digit)

    def latexcode(self):
        unc_digit = most_significant_digit(self.unc)

        value_digit = most_significant_digit(self.value)

        to_print_unc, unc_digit_rep = significant_digits(self.unc, self.unc_digit)
        to_print_value, value_digit_rep = significant_digits(
            self.value,
            max(value_digit - unc_digit + self.unc_digit, 0)
        )

        to_print_value = move_decimal(to_print_value,
                                      value_digit_rep - unc_digit_rep)
        # Raise a warning if adding digits to uncertanty
        if len(str(self.unc)) < len(to_print_unc):
            raise Warning("""uncertanty of Udecimal '{0}' has more digit than
                             orginal value: {1}""".format(self.name, self.unc))

        return '\\newcommand{{\\{0}}}{{{1} \\pm {2} e{3}}}'.format(
            self.name,
            to_print_value,
            to_print_unc,
            unc_digit,
        )


class Document:
    def __init__(self):
        self.variables = []

    def setvariable(self, variable):
        # Check correct type
        if issubclass(variable.__class__, Variable):
            # Try to replace an existence one
            for i in range(0, len(self.variables)):
                if self.variables[i].name == variable.name:
                    self.variables[i] = variable
                    return
            # Adding if not present
            self.variables.append(variable)
        else:
            raise TypeError('object {0} ({1}) is not a valid variable.'.format(
                variable,
                type(variable),
            ))

    def removevariable(self, name):
        for i in range(0, len(self.variables)):
            if self.variables[i].name == name:
                del self.variables[i]

    def clearvariables(self):
        self.variables.clear()

    def save(self, filename):
        # Header message
        tex = '% File generated with LabTools.latex\n'
        tex += '% Copyright (c) Luca Arnaboldi 2019\n\n'
        tex += '% Include this file in your LaTex project to use these definitions\n\n'

        # Variables 
        tex += '% Variables\n'
        for v in self.variables:
            tex += v.latexcode() + '\n'
        
        with open(filename, 'w') as tfile:
            tfile.write(tex)
