import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def boxplot(L, out_file_name, x_ticks, x_label, y_label, title):
    """
    Draw a boxplot diagram and save it as a figure.
    Parameters:
    L: A list of numbers in either integer or float type
    out_file_name: The file name for the output figure
    x_ticklabel: The name of x-axis members
    x_label: The name of x-axis for the output figure
    y_label: The name of y-axis for the output figure
    title: Title of the boxplot
    """
    if os.path.exists(out_file_name):
        raise FileExistsError('File already exists.')

    fig = plt.figure(figsize=(10, 3), dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    ax.boxplot(L)
    ax.set_xticklabels(x_ticks, rotation=90)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)

    plt.savefig(out_file_name, bbox_inches='tight')
