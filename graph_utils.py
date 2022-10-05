import matplotlib.pyplot as plt
import logging

def add_bar_labels(x,y, fontsize):
    for i in range(len(x)):
        plt.text(i, y[i] + 0.2, y[i], fontdict={"fontsize": fontsize, "weight": "bold"}, ha = "center")
    
def legend_position(y, max, bars_from_start_or_end):
    legend_is_on_first_bars = False
    legend_is_on_last_bars = False
    treshold = max * 0.70
    logging.debug("Legend treshold: {}".format(treshold))
    for val in y[0:bars_from_start_or_end]:
        if val > treshold:
            legend_is_on_first_bars = True

    for val in y[-bars_from_start_or_end:]:
        if val > treshold:
            legend_is_on_last_bars = True

    if legend_is_on_first_bars and legend_is_on_last_bars:
        return 8, 12
    elif legend_is_on_first_bars:
        return 880, 90
    else: 
        return 170, 90 



    
    


    