import matplotlib.pyplot as plt

def add_bar_labels(x,y, fontsize):
    for i in range(len(x)):
        plt.text(i, y[i] + 0.2, y[i], fontdict={"fontsize": fontsize, "weight": "bold"}, ha = "center")
    
def legend_position(y, max, bars_from_start):
    legend_is_on_bars = False
    treshold = max * 0.70
    print('legend_treshold', treshold)
    for val in y[0:bars_from_start]:
        if val > treshold:
            legend_is_on_bars = True

    if legend_is_on_bars:
        return 8, 12
    else:
        return 170,90


