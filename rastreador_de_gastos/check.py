#check if input is a datetime
def check_datetime(word : str, format : str) -> bool:
    from datetime import datetime
    try:
        data = datetime.strptime(word, format)
        return True
    except:
        return False

#check if input is a float
def check_float(input_user) -> bool:
    try:
        input_user = float(input_user)
        return input_user >= 0
    except:
        return False

#check if input is a int
def check_int(input_user) -> bool:
    try:
        input_user = int(input_user)
        return True
    except:
        return False
    
#check if a number to be in interval
def check_at_interval(num, ini, end):
    if check_int(num) == True:
        return (ini <= int(num) and int(num) <= end)
    return False