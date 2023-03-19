import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_loss(measurements, title):
    """Plot the paket loss of measurements."""
    x = [m.timestamp for m in measurements]
    x = mdates.date2num(x)
    y = [m.paket_loss for m in measurements]
    
    # Create figure
    fig, ax = plt.subplots(nrows=1, ncols=1) 
    fig.suptitle(title)
    ax.plot_date(x, y)

    # Format the x-axis
    date_format = mdates.DateFormatter('%m-%d-%Y')
    ax.xaxis.set_major_formatter(date_format)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    return fig