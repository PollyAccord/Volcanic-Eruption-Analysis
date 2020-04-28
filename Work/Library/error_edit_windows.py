from tkinter import messagebox as mb


"""
Автор:
Цель: обрабатывает исключения 
Вход: объект исключения 
Выход: Строковое сообщение 
"""


def error(string):
    mb.showerror("Ошибка", string)


"""
Автор: 
Цель: Выводит окно с вопросом и ответами yes/no 
Вход: сообщение 
Выход: принятое решение (да/нет) 
"""


def yes_no(string):
    answer = mb.askyesno(title="Вопрос", message=string)
    flag = True
    if answer:
        mb.showinfo("Cообщение", "Выполнено")
        return flag
    elif not answer:
        mb.showinfo("Сообщение", "Отменено")
        return not flag


"""
Автор:  
Цель: Открывает окно с текстом-предупреждением 
Вход: сообщение 
Выход: Нет 
"""


def warning(string, flag):
    if not flag:
        mb.showwarning("Предупреждение", string)
    else:
        mb.showinfo("Cообщение", "OK")
