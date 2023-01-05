from utils import format_difference, format_percentage, format_price, get_month_name, format_difference
from datetime import datetime
import database
import os

def compile_day_ahead_message(report):
    insights = report.insights
    below_average_periods = report.calculate_below_average_periods()
    #num_of_periods = len(below_average_periods)
    hashtags = "#sähkönhinta"
    
    mean = format_price(insights['mean'])
    min = format_price(insights['min'])
    max = format_price(insights['max'])

    range_str = ''
    if len(below_average_periods) > 1:
        range_str = "Ajanjaksot, joissa"
    else:
        range_str = "Ajanjakso, jossa"

    tax = os.getenv("TAX")

    message = f"Spot-hinnat {report.date}, snt/kWh (alv {tax}%)\n"
    message += f"Alin: {min}\n"
    message += f"Ylin: {max}\n"
    message += f"Keskihinta: {mean}\n\n"
    

    #message +=f"7vrk keskihinta: {format_price(report.avg_7_day.insights['mean'])}\n"
    #message +=f"28vrk keskihinta: {format_price(report.avg_28_day.insights['mean'])}\n\n"

    

    below_average_message = f"{range_str} hinta pysyttelee alle vuorokauden keskiarvon\n"
    if len(below_average_periods) <=3:
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

def compile_28_day_message(report):
    insights = report.insights
    mean = format_price(insights['mean'])
    min = format_price(insights['min'])
    max = format_price(insights['max'])

    message = f"28 vuorokauden keskihinta: {mean} snt/kWh"
    return message

    
def compile_7_day_message(report):
    insights = report.insights
    mean = format_price(insights['mean'])
    message = f"7 vuorokauden keskihinta: {mean} snt/kWh"
    return message

def compile_monthly_message(report_current, report_previous):

    insights_curr = report_current.insights
    insights_prev = report_previous.insights

    diff = insights_curr['mean'] - insights_prev['mean']
    diff_percent = diff / insights_prev['mean'] * 100
    
    min = format_price(insights_curr['min'])
    max = format_price(insights_curr['max'])
    mean = format_price(insights_curr['mean'])

    curr_month = get_month_name(report_current.start.month)
    prev_month = get_month_name(report_previous.start.month)

    tax = os.getenv("TAX")

    message =  f"Pörssisähkön hinta {curr_month}ssa, snt/kWh (alv {tax}%)\n"
    message += f"Alin: {min}\n"
    message += f"Ylin: {max}\n"
    message += f"Keskihinta: {mean}\n"
    message += f"Keskihinnan muutos {prev_month}hun: {format_difference(diff)} ({format_percentage(diff_percent)}%)\n"

    message+= "\n#energia #sähkönhinta"
    print(len(message))
    return message

def compile_weekly_message(report_current, report_previous):

    insights_curr = report_current.insights
    insights_prev = report_previous.insights

    diff = insights_curr['mean'] - insights_prev['mean']
    diff_percent = diff / insights_prev['mean'] * 100
    
    min = format_price(insights_curr['min'])
    max = format_price(insights_curr['max'])
    mean = format_price(insights_curr['mean'])

    tax = os.getenv("TAX")

    message =  f"Pörssisähkön tuntihinnat tällä viikolla, snt/kWh (alv {tax}%)\n"
    message += f"Alin: {min}\n"
    message += f"Ylin: {max}\n"
    message += f"Keskihinta: {mean}\n"
    message += f"Muutos edelliseen viikkoon: {format_difference(diff)} ({format_percentage(diff_percent)}%)\n"

    message+= "\n#energia #sähkö #hinta"
    print(len(message))
    return message




def compile_reply():
    now = datetime.now()
    latest = database.get_latest()

    tax = os.getenv("TAX")
    img_path = latest['latest_7_path']

    message = f"Pörssisähkön 7 tuntihinnat, keskihinta {latest['latest_7_avg']} snt/kWh (alv {tax}%)"

    return message, img_path