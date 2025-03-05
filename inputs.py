from datetime import datetime, timedelta
import keyboard

def input_str(prompt="Введите строку: "):
    """Запрашивает ввод строки у пользователя с проверкой."""
    user_input = None
    while True:
        try:
            return input(prompt)
        except EOFError:
            print("\nОшибка завершения ввода.")
            continue
        except KeyboardInterrupt:
            print("\nОшибка прерывания ввода.")
            continue

def wait_for_keypress():
    """
    Ожидает нажатия клавиши и возвращает символ.
    Работает с буквами, цифрами и специальными клавишами.
    """
    #print("Нажмите любую клавишу...")
    while True:
        event = keyboard.read_event()  # Считываем событие клавиатуры
        if event.event_type == 'up':  # Обрабатываем только нажатие
            key = event.name
            if len(key) == 1 and key.isprintable():
                return event.name  # Возвращаем название нажатой клавиши

def input_int(prompt="Введите целое число: "):
    """Запрашивает ввод целого числа у пользователя с проверкой на корректность."""
    while True:
        user_input = input_str(prompt)
        try:
            return int(user_input)
        except ValueError:
            print("Ошибка: введите корректное целое число.")


def input_float(prompt="Введите вещественное число: "):
    """Запрашивает ввод вещественного числа у пользователя с проверкой на корректность."""
    while True:
        user_input = input_str(prompt)
        try:
            return float(user_input)
        except ValueError:
            print("Ошибка: введите корректное вещественное число.")


def input_string(prompt="Введите строку: ", allow_empty=False):
    """Запрашивает ввод строки у пользователя с проверкой на пустоту."""
    while True:
        user_input = input_str(prompt)
        if user_input or allow_empty:
            return user_input
        else:
            print("Ошибка: строка не может быть пустой.")


def input_choice(options, prompt="Сделайте выбор: "):
    """
    Запрашивает у пользователя ввод, проверяя, что он принадлежит одному из предложенных вариантов.
    Аргумент `options` — список допустимых значений.
    """
    options_str = ', '.join(options)
    while True:
        user_input = input_str(f"{prompt} ({options_str}): ")
        if user_input in options:
            return user_input
        else:
            print(f"Ошибка: выберите один из предложенных вариантов: {options_str}.")


def input_yes_no(prompt="Введите 'да' или 'нет': "):
    """Запрашивает ввод 'да' или 'нет' от пользователя."""
    while True:
        user_input = input_str(prompt).strip().lower()
        if user_input in ['да', 'д', 'yes', 'y']:
            return True
        elif user_input in ['нет', 'н', 'no', 'n']:
            return False
        else:
            print("Ошибка: введите 'да' или 'нет'.")


def input_date(prompt="Введите дату в формате ДД.ММ.ГГГГ: "):
    """
    Запрашивает у пользователя ввод даты в формате ДД.ММ.ГГГГ с проверкой на корректность.
    Возвращает объект datetime.
    """
    while True:
        user_input = input_str(prompt)
        try:
            # Парсинг даты с заданным форматом
            return datetime.strptime(user_input, "%d.%m.%Y")
        except ValueError:
            print("Ошибка: введите дату в формате ДД.ММ.ГГГГ.")


def date_difference(date1, date2):
    """
    Вычисляет разницу между двумя датами и возвращает её в формате (лет, месяцев, дней).
    """
    if date1 > date2:
        date1, date2 = date2, date1

    # Разница в днях между датами
    delta = date2 - date1

    # Начинаем с разницы по годам
    years = date2.year - date1.year
    months = date2.month - date1.month
    days = date2.day - date1.day

    # Корректировка месяцев и дней, если разница отрицательная
    if days < 0:
        months -= 1
        # Определяем количество дней в предыдущем месяце
        prev_month = (date2.month - 1) if date2.month > 1 else 12
        prev_year = date2.year if date2.month > 1 else date2.year - 1
        days += (datetime(prev_year, prev_month + 1, 1) - timedelta(days=1)).day

    if months < 0:
        years -= 1
        months += 12

    return years, months, days

def input_integer_in_range(prompt: str, min_value: int, max_value: int) -> int:
    """
    Запрашивает у пользователя ввод целого числа из указанного диапазона.

    Args:
        prompt (str): Текст для отображения пользователю при вводе.
        min_value (int): Минимальное допустимое значение.
        max_value (int): Максимальное допустимое значение.

    Returns:
        int: Целое число, введённое пользователем, которое находится в указанном диапазоне.

    Raises:
        ValueError: Если диапазон некорректен (min_value > max_value).
    """
    if min_value > max_value:
        raise ValueError("Минимальное значение не может быть больше максимального.")

    while True:
        user_input = input_str(f"{prompt} (от {min_value} до {max_value}): ")
        try:
            number = int(user_input)
            if min_value <= number <= max_value:
                return number
            else:
                print(f"Ошибка: введите число в диапазоне от {min_value} до {max_value}.")
        except ValueError:
            print("Ошибка: введите корректное целое число.")