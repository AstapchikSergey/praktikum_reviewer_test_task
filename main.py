import datetime as dt


class Record:
    # В таком случае, лучше date инициализировать по умолчанию None, а не пустой строкой,
    # А для избежания сложной конструкции можно сразу инициализировать date = dt.datetime.now().date()
    # а в конструкторе достаточно написать self.date = date
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Не стоит называть переменную так же как класс, тем более что в строке 36 все ок.
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # (today - record.date).days желательно вынести в отдельную переменную,
            # чтобы не вичислять два раза и уменьшить компреммию выражения
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Комментарии к функции оформляются в виде Docstring, а не так
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            # В соответствии с требованиями, бэкслеши не применяются для переноса
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # Можно просто писать return str без лишних круглых скобок.
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.
    # Бессмысленная передача параметров. USD_RATE и EURO_RATE итак объявлены переменными класса
    # и доступны в self.
    # Тем более, по ТЗ эти параметры не передаются в функцию.
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # Почему с строке 71 currency, а в остальных currency_type?
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Тут наверное тоже хотелось бы разделить а не присвоить?
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            # Из требований к коду: В f-строках применяется только подстановка переменных
            # и нет логических или арифметических операций, вызовов функций и подобной динамики
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # Здесь можно использовать else, а не elif, так как это полный набор событий
        elif cash_remained < 0:
            # Снова бэкслеш
            # Нарушается консистентность кода, в предыдущем случае для округления
            # была использована функция round(), теперь форматирование.
            # Для одинаковых проблем желетельно использовать одинаковые методы.
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Зачем? Почему тогда методы get_today_stats и add_record не перегружены?
    # И в классе CaloriesCalculator тоже.
    def get_week_stats(self):
        super().get_week_stats()
