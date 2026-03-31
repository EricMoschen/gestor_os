import holidays

BR_HOLIDAYS = holidays.Brazil()

def eh_feriado_ou_domingo(data):
    return data in BR_HOLIDAYS or data.weekday() == 6

def eh_sabado(data):
    return data.weekday() == 5
