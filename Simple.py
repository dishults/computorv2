om Numbers import Numbers

class Simple:

    def __init__(self, variable, equation, sub_equation=False):
        self.equation = []
        self.var = variable
        self.sub_equation = sub_equation
        starts_with_minus = False
        if equation[0] == "-":
            equation = equation[1:]
            starts_with_minus = True
        for c in equation:
            if c in ("+", "-", "/", "%", "*"):
                var, equation = equation.split(c, 1)
                self.proceed(var)
                self.equation.append(c)
            elif c == "(":
                equation = equation.strip("(")
                var, equation = equation.rsplit(")", 1)
                self.equation.append(Simple(variable, var, sub_equation=True))
                if not equation:
                    break
        if equation:
            self.proceed(equation)
        if starts_with_minus and type(self.equation[0]) in (int, float):
            self.equation[0] *= -1
    
    def __str__(self):
        f = ""
        if self.sub_equation:
            f += f"({self.equation[0]}"
            for e in self.equation[1:]:
                f += f" {e}"
            f += ")"
        else:
            for e in self.equation:
                f += f" {e}"
        return f
    
    def proceed(self, var):
        try:
            var = Numbers.convert_to_num(var)
        except:
            if self.var != var:
                raise ValueError
        self.equation.append(var)