from utils import format_difference, format_percentage, format_price, get_month_name, format_difference
from datetime import datetime

def compile_day_ahead_message(data_item):
    insights = data_item.insights
    below_average_periods = data_item.calculate_below_average_periods()
    #num_of_periods = len(below_average_periods)
    hashtags = "#sähkö #energia"
    
    mean = format_price(insights['mean'])
    min = format_price(insights['min'])
    max = format_price(insights['max'])

    range_str = ''
    if len(below_average_periods) > 1:
        range_str = "Ajanjaksot, joissa"
    else:
        range_str = "Ajanjakso, jossa"

    message = f"Spot-hinnat {data_item.date}, snt/kWh (alv 0%)\n"
    message += f"Alin: {min}\n"
    message += f"Ylin: {max}\n"
    message += f"Keskihinta: {mean}\n\n"
    

    #message +=f"7vrk keskihinta: {format_price(data_item.avg_7_day.insights['mean'])}\n"
    #message +=f"28vrk keskihinta: {format_price(data_item.avg_28_day.insights['mean'])}\n\n"

    

    below_average_message = f"{range_str} hinta pysyttelee alle vuorokauden keskiarvon\n"
    for r in below_average_periods:
        mean = str(r[2]).replace('.',',')
        below_average_message+= f"{str(r[0])}.00 - {str(r[1])}.00, keskihinta {mean}\n"


    if (len(message) + len(below_average_message)) < 280:
        message += below_average_message

    if (len(message) + len(hashtags)) < 280:
        message += f"\n{hashtags}"
    

    return message

def compile_today_reply_message():
    
    message = "Tuntihinnat tänään"
    return message

def compile_28_day_reply_message(data_item):
    insights = data_item.insights
    mean = format_price(insights['mean'])
    min = format_price(insights['min'])
    max = format_price(insights['max'])

    message = f"28 vuorokauden keskihinta: {mean} snt/kWh"
    return message

    pass
def compile_7_day_reply_message(data_item):
    insights = data_item.insights
    mean = format_price(insights['mean'])
    message = f"7 vuorokauden keskihinta: {mean} snt/kWh"
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