# Utilities for dates

from django.contrib import admin
from django.apps import apps
import datetime
from dateutil.relativedelta import relativedelta
import calendar
from datetime import date



def conv_str_to_datetime(d_str: str, format: str) -> datetime:
    """
    Convert from string format to datetime format
    d_str : str
        date in string format
    format : str
        format
    """
    result = ""

    if d_str == "" or d_str == -1 or d_str == "-1" or format == "" or d_str == None:
        return result
    result = datetime.datetime.strptime(d_str, format)
    return result



def conv_yyyymmdd_to_datetime(d_str: str, delimiter: str = "-") -> datetime:
    """
    Convert from string format YYYYMMDD to datetime format
    d_str : str
        date in string format
    delimiter : str
        date parts delimiter, e.g. for date '2022-01-01' delimiter will be '-'
    """
    format = f"%Y{delimiter}%m{delimiter}%d"
    # print(f"format = {format}")
    return conv_str_to_datetime(d_str, format)



def get_very_min_date() -> str:
    return "1000-01-01"

def get_very_max_date() -> str:
    return "3000-01-01"



def get_years_difference(start_date, end_date) -> int:
    """
    Get the difference between two dates in years
    start_date : datetime or date
        start date
    end_date : datetime or date
        end date
    """
    result = 0
    if ((isinstance(start_date, datetime.datetime) and isinstance(end_date, datetime.datetime)) or 
            (isinstance(start_date, datetime.date) and isinstance(end_date, datetime.date)) or 
            (isinstance(start_date, datetime.datetime) and isinstance(end_date, datetime.date)) or 
            (isinstance(start_date, datetime.date) and isinstance(end_date, datetime.datetime))):
        # difference = end_date - start_date
        # result = difference.days / 365.25 # Accounting for leap years
        # result = round(result)
        result = relativedelta(end_date, start_date).years
    return result



def get_month_min_datetime(month: str) -> datetime:
    """
    Get minimal datetime in a month
    month: str
        target month in format YYYY-MM
    """
    year, month = month.split("-")
    return datetime.datetime(int(year), int(month), 1, 0, 0, 0)



def get_month_max_datetime(month: str) -> datetime:
    """
    Get maximal datetime in a month
    month: str
        target month in format YYYY-MM
    """
    year, month = month.split("-")
    days_in_month = calendar.monthrange(int(year), int(month))[1]
    return datetime.datetime(int(year), int(month), int(days_in_month), 23, 59, 59)



def get_month_min_date(month: str) -> date:
    """
    Get minimal date in a month
    month: str
        target month in format YYYY-MM
    """
    year, month = month.split("-")
    return date(int(year), int(month), 1)



def get_month_max_date(month: str) -> date:
    """
    Get maximal date in a month
    month: str
        target month in format YYYY-MM
    """
    year, month = month.split("-")
    days_in_month = calendar.monthrange(int(year), int(month))[1]
    return date(int(year), int(month), int(days_in_month))









