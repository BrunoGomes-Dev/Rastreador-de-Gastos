#print a list
def print_list(list, func):
    for i in list:
        func(i)

#binary_search
def binary_search(ini : int, end : int, value : int, lista: list) -> int:
    while ini <= end and len(lista) > 0:
        mid = (ini+end)//2
        compare_value = lista[mid]["ID"]

        if compare_value == value:
            return mid
        elif compare_value > value:
            end = mid - 1
        else:
            ini = mid + 1
    return -1

def filter_list(lista, category = "", monty_year = ""):
    return [item for item in lista if category in item["Categoria"] and monty_year in item["Data"]]