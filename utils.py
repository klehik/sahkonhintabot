import os
from datetime import datetime, timedelta

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


def compile_message(data_item):
    insights = data_item.calculte_insights()
    below_average_periods = data_item.calculate_below_average_hours()

    range_str = ''

    if len(below_average_periods) > 1:
        range_str = "Ajanjaksot"
    else:
        range_str = "Ajanjakso"

    message = f"Sähkön spot-hinnat {data_item.date} snt/kWh (alv 0%)\n"
    message+= f"Alin: {insights['min']}\n"
    message+= f"Ylin: {insights['max']}\n"
    message+= f"Keskiarvo: {insights['mean']}\n\n"
    message+= f"{range_str}, jossa hinta alle vuorokauden keskiarvon\n"
    for r in below_average_periods:
        mean = str(r[2]).replace('.',',')
        message+= f"{str(r[0])}.00 - {str(r[1])}.00, keskihinta {mean}\n"
    message+= "\n#energia #sähkö #hinta"

    return message