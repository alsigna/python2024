def calc_match(a: int, b: int, op: str) -> int:
    match op:
        case "+":
            return a + b
        case "-":
            return a - b
        case "/":
            return a // b
        case "*":
            return a * b
        case _:
            raise ValueError("Неизвестная операция")


def calc_if(a: int, b: int, op: str) -> int:
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "/":
        return a // b
    elif op == "*":
        return a * b
    else:
        raise ValueError("Неизвестная операция")


def calc_dict(a: int, b: int, op: str) -> int:
    funcs = {
        "+": lambda a, b: a + b,  # operator.add()
        "-": lambda a, b: a - b,  # operator.sub()
        "/": lambda a, b: a // b,  # operator.floordiv()
        "*": lambda a, b: a * b,  # operator.mul()
    }
    f = funcs.get(op)
    if f is None:
        raise ValueError("Неизвестная операция")
    else:
        return f(a, b)


if __name__ == "__main__":
    f = calc_dict
    print(f(3, 2, "+"))
    print(f(3, 2, "-"))
    print(f(3, 2, "*"))
    print(f(3, 2, "/"))
    print(f(3, 2, "**"))
