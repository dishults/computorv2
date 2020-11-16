def linear(a, b):
    """
    x = -b / a
    """

    res = "The R solution is:\n"
    if b == 0 and a == 0:
        return res + "  Every real number is a solution"
    elif a == 0:
        return res + "  The eqution has no solution"
    elif b == 0:
        return res + "  0"
    else:
        return res + f"  {-b / a}"
    
def quadratic(two_a, b, discriminant, simple=True):
    """
        -b +- sqrt(b^2 - 4ac)
    x = —————————————————————
                2a
    """
    if two_a == 0:
        return "The eqution has no solution"
    elif simple:
        sqrt = discriminant ** 0.5
        x1 = (-b - sqrt) / two_a
        x2 = (-b + sqrt) / two_a
        res = "The two R solutions are:\n"
        res += f"  {round(x1, 6)}\n"
        res += f"  {round(x2, 6)}"
    else:
        discriminant *= -1
        sqrt = discriminant ** 0.5
        real = -b / two_a
        imaginary = sqrt / two_a
        res = "The two C solutions are:\n"
        res += f"  {round(real, 6)} - {round(imaginary, 6)}i\n"
        res += f"  {round(real, 6)} + {round(imaginary, 6)}i"
    return res