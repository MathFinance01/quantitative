import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import QuantLib as ql

def plot_dataframe_wrapper(lst):
    return pd.DataFrame(lst, columns=['x', 'y'])

def plot_xy(xy_data, ax, title, x_axis, y_axis):
    xy_data = plot_dataframe_wrapper(xy_data)
    ax.plot(xy_data['x'], xy_data['y'])
    ax.set_title(title)
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)

def generate_continuous_inputs(x):
    start_value = x / 2
    end_value = 1.5 * x
    delta_x = x / 100
    x = start_value

    while x < end_value:
        x += delta_x
        yield x

def generate_dates(start_date, end_date):
    x = end_date
    cal = ql.TARGET()
    one_day = ql.Period(-1, ql.Days)
    while x > start_date:
        yield x
        x = cal.advance(x, one_day, ql.Following, False)
