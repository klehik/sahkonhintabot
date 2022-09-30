from email import message_from_string
import os
from datetime import datetime, timedelta
import calendar


def format_price(value):
    price = round(value, 2)
    price = format(price, ".2f")
    price = str(price).replace('.',',')
    return price


def get_ranges(nums):
    nums = sorted(set(nums))
    gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s+1 < e]
    edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
    return list(zip(edges, edges))


def compile_day_ahead_message(data_item):
    insights = data_item.insights
    below_average_periods = data_item.calculate_below_average_periods()
    num_of_periods = len(below_average_periods)

    
    mean = format_price(insights['mean'])


    min = format_price(insights['min'])

   
    max = format_price(insights['max'])

    range_str = ''
    if len(below_average_periods) > 1:
        range_str = "Ajanjaksot, joissa"
    else:
        range_str = "Ajanjakso, jossa"

    message = f"Sähkön spot-hinnat {data_item.date}, snt/kWh (alv 0%)\n"
    message+= f"Keskihinta: {mean}\n"
    message+= f"Alin: {min}\n"
    message+= f"Ylin: {max}\n\n"

    

    if num_of_periods <= 3 and num_of_periods > 0:

        message+= f"{range_str} hinta pysyttelee alle vuorokauden keskiarvon\n"
        for r in below_average_periods:
            mean = str(r[2]).replace('.',',')
            message+= f"{str(r[0])}.00 - {str(r[1])}.00, keskihinta {mean}\n"

    message+= "\n#energia #sähkö"

    return message

def compile_monthly_message(data_item_current, data_item_previous):

    insights_curr = data_item_current.insights
    insights_prev = data_item_previous.insights

    diff = insights_curr['mean'] - insights_prev['mean']
    diff_percent = diff / insights_prev['mean'] * 100
    
    min = format_price(insights_curr['min'])
    max = format_price(insights_curr['max'])
    mean = format_price(insights_curr['mean'])

    curr_month = get_month_name(data_item_current.start.month)
    prev_month = get_month_name(data_item_previous.start.month)

    message =  f"Pörssisähkön hinta {curr_month}ssa, snt/kWh (alv 0%)\n"
    message += f"Alin: {min}\n"
    message += f"Ylin: {max}\n"
    message += f"Keskihinta: {mean}\n"
    message += f"Muutos {prev_month}hun: {format_difference(diff)} ({format_percentage(diff_percent)}%)\n"

    message+= "\n#energia #sähkö #hinta"
    print(len(message))
    return message

def compile_weekly_message(data_item_current, data_item_previous):

    insights_curr = data_item_current.insights
    insights_prev = data_item_previous.insights

    diff = insights_curr['mean'] - insights_prev['mean']
    diff_percent = diff / insights_prev['mean'] * 100
    
    min = format_price(insights_curr['min'])
    max = format_price(insights_curr['max'])
    mean = format_price(insights_curr['mean'])

    curr_month = get_month_name(data_item_current.start.month)
    prev_month = get_month_name(data_item_previous.start.month)

    message =  f"Pörssisähkön tuntihinnat tällä viikolla, snt/kWh (alv 0%)\n"
    message += f"Alin: {min}\n"
    message += f"Ylin: {max}\n"
    message += f"Keskihinta: {mean}\n"
    message += f"Muutos edelliseen viikkoon: {format_difference(diff)} ({format_percentage(diff_percent)}%)\n"

    message+= "\n#energia #sähkö #hinta"
    print(len(message))
    return message




def compile_reply():
    now = datetime.now()

    img_path = f"./images/{str(now.day)}.{str(now.month)}.{str(now.year)}.png"

    message = f"Pörssisähkön spot-hinnat tänään"

    return message, img_path


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