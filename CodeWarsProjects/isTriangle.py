def is_triangle(a, b, c):
    msg = False
    if a + b > c:
        if a + c > b:
            if b + c > a:
                msg = True
    return msg


if __name__ == "__is_triangle__":
    is_triangle()
