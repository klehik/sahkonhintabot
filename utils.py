
from datetime import datetime
import calendar




def format_price(value):
    
    price = format(value, ".2f")
    price = str(price).replace('.',',')
    return price


def get_ranges(nums):
    nums = sorted(set(nums))
    gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s+1 < e]
    edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
    return list(zip(edges, edges))




def get_month_name(month):
    switch = {
            
            1: "tammikuu",
            2: "helmikuu",
            3: "maaliskuu",
            4: "huhtikuu",
            5: "toukokuu",
            6: "kesäkuu",
            7: "heinäkuu",
            8: "elokuu",
            9: "syyskuu",
            10: "lokakuu",
            11: "marraskuu",
            12: "joulukuu"
        }
    return switch.get(month, "")


def get_days_in_month(date: datetime):
    monthrange = calendar.monthrange(date.year, date.month)
    return monthrange[1]


def format_difference(value):
    if value > 0:
        return "+" + str(format_price(value))
    else: 
        return str(format_price(value))

def format_percentage(value):
    value = round(value, 1)
    prefix = ""

    if value > 0:
        prefix = "+"

    value = format(value, ".1f")
    
    value = str(value).replace('.',',') 
    
    return prefix + value




