import turtle


def koch_segment(length, order):
    """
    Малює одну ламану Коха довжини length з рекурсивним порядком order.
    Базовий випадок: order == 0 -> пряма лінія.
    """
    if order == 0:
        turtle.forward(length)
    else:
        length /= 3.0
        koch_segment(length, order - 1)
        turtle.left(60)
        koch_segment(length, order - 1)
        turtle.right(120)
        koch_segment(length, order - 1)
        turtle.left(60)
        koch_segment(length, order - 1)


def koch_snowflake(length, order):
    """Малює повну сніжинку Коха (3 сторони трикутника)."""
    for _ in range(3):
        koch_segment(length, order)
        turtle.right(120)


def main():
    # Запит рівня рекурсії у користувача
    while True:
        try:
            order = int(input("Введіть рівень рекурсії (наприклад, 0–6): "))
            if order < 0:
                print("Рівень не може бути від’ємним.")
                continue
            break
        except ValueError:
            print("Будь ласка, введіть ціле число.")

    turtle.speed(0)
    turtle.penup()
    turtle.goto(-200, 100)  # Зміщуємо фігуру в центр вікна
    turtle.pendown()

    koch_snowflake(400, order)

    turtle.hideturtle()
    turtle.done()


if __name__ == "__main__":
    main()