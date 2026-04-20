'''
- we are given a start date
- we are given number of working days required
- we need to skip weekends and holidays

- in order to skip weekends, we need to know the weekday of our startDate
'''

def _days_before_year(year):
    '''
    Returns the days before the current year to be added as offset.
    '''
    y = year - 1
    return 365 * y + y // 4 - y // 100 + y // 400

def _days_before_month(year, month):
    '''
    Returns the days before the current month.
    '''
    total = 0
    for m in range(1, month):
        total += _days_in_month(year, m)
    return total

def _absolute_day(year, month, day):
    return _days_before_year(year) + _days_before_month(year, month) + day

def _weekday(year, month, day):
    '''
    Returns the weekday from a reference date
    '''
    ref_abs = _absolute_day(1970, 1, 1)
    target_abs = _absolute_day(year, month, day)
    offset = target_abs - ref_abs
    ref_weekday = 3
    return (ref_weekday + offset) % 7

def _encode_date(date):
    '''
    Converts string yyyy-mm-dd format date to (yyyy, mm, dd) integer date tuple.
    '''
    parts = date.strip().split('-')
    year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
    return (year, month, day)

def _decode_date(date):
    '''
    Converts (yyyy, mm, dd) integer date tuple to yyyy-mm-dd format string.
    '''
    year, month, day = date
    return f"{year}-{month}-{day}"

def _is_working_date(date, holiday_set):
    weekday = _weekday(date[0], date[1], date[2])

    if weekday == 5 or weekday == 6 or date in holiday_set:
        return False
    
    return True

def _is_leap_year(year):
    '''
    Returns if a year is a leap year.
    '''
    return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)

def _days_in_month(year, month):
    '''
    Returns days in a month.
    '''
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if _is_leap_year(year) and month == 2:
        return 29
    return days[month - 1]

def _next_date(date):
    '''
    Returns the next date. 
    '''
    year, month, day = date

    days_left_in_month = _days_in_month(year, month) - day
    
    if days_left_in_month > 0:
        return (year, month, day + 1)
    else:
        if month == 12:
            return (year + 1, 1, 1)
        else:
            return (year, month + 1, 1)

def finish_days(startDate, holidays, workingDays):
    '''
    Returns the end date of a project.
    '''

    holiday_set = set()
    for holiday in holidays:
        encoded_holiday_date = _encode_date(holiday)
        holiday_set.add(encoded_holiday_date)

    remaining_working_days = workingDays
    current_date = _encode_date(startDate)

    while remaining_working_days > 0:

        if _is_working_date(current_date, holiday_set):
            remaining_working_days -= 1
        
        current_date = _next_date(current_date)
    
    return _decode_date(current_date)

startDate = '2024-6-23'
holidays = ['2024-6-30', '2026-7-15']
workingDays = 55

print(finish_days(startDate, holidays, workingDays))
        
