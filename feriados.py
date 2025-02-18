# feriados.py
import datetime
import numpy as np

def easter_sunday(year):
    # Cálculo da data da Páscoa (Método de Computus)
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19*a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2*e + 2*i - h - k) % 7
    m = (a + 11*h + 22*l) // 451
    month = (h + l - 7*m + 114) // 31
    day = ((h + l - 7*m + 114) % 31) + 1
    return datetime.date(year, month, day)

def get_national_holidays(year):
    # Feriados nacionais fixos
    holidays = [
        datetime.date(year, 1, 1),    # Confraternização Universal
        datetime.date(year, 4, 21),   # Tiradentes
        datetime.date(year, 5, 1),    # Dia do Trabalhador
        datetime.date(year, 9, 7),    # Independência do Brasil
        datetime.date(year, 10, 12),  # Nossa Senhora Aparecida
        datetime.date(year, 11, 2),   # Finados
        datetime.date(year, 11, 15),  # Proclamação da República
        datetime.date(year, 12, 25)   # Natal
    ]

    # Cálculo da Sexta-Feira Santa
    easter = easter_sunday(year)
    good_friday = easter - datetime.timedelta(days=2)
    holidays.append(good_friday)

    return holidays

def get_busdaycalendar_with_holidays(start_date, end_date):
    # Gera um busdaycalendar com os feriados nacionais entre os anos das datas fornecidas
    holidays = []
    for yr in range(start_date.year, end_date.year + 1):
        for h in get_national_holidays(yr):
            holidays.append(np.datetime64(h))
    bus_cal = np.busdaycalendar(holidays=holidays)
    return bus_cal
