"""
Автор:
Цель: Проверка принадлежности списка переменных к типу Integer
Вход: Переменные
Выход: Флаг с соответствующим значением
"""


def is_int(value):
    try:
        for i in value:
            int(i)
        return True
    except ValueError:
        return False
