import datetime
def date():

    original_date = datetime.datetime.now().date()
    new_date = ''
    original_date = str(original_date)
    original_date = original_date.split("-")
    new_date += original_date[1]
    new_date += '/'
    new_date += original_date[2]
    new_date += '/'
    new_date += original_date[0]

    if new_date[0] == '0':
        new_date = new_date[1:]

    return new_date
