from .check import check_datetime, check_float, check_at_interval

#confirme datetime of user
def confirme_datetime(date : str, format, format_for_user : str, func) -> str:
    while check_datetime(date, format) == False:
        date = func(f"Formato inválido! Use o formato {format_for_user}")
    return date

#confirme value for price
def confirmer_value(value : str, func) -> float:
    while check_float(value) == False:
        value = func("Valor inválido! Digite um número positivo")

    return round(float(value), 2)

#confirme number in interval
def confirme_number_in_interval(choice_category, ini : int, end : int, func_input)->int:
    while check_at_interval(choice_category, ini, end) == False:
        choice_category = func_input(f"Valor inválido! Digite um número entre {ini} a {end}")

    return int(choice_category)