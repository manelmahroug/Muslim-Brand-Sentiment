import pandas as pd
import matplotlib.pyplot as plt

def compute_sentiment_metrics(row):
    """
    Calculates mean change, volatility (std), and net change for a time series row.

    Args:
        row (pd.Series): A pandas Series representing sentiment over time.

    Returns:
        pd.Series: Contains Mean_Change, Volatility, and Net_Change.
    """
    deltas = row.diff().dropna()
    return pd.Series({
        "Mean_Change": deltas.mean(),
        "Volatility": deltas.std(),
        "Net_Change": row.iloc[-1] - row.iloc[0]
    })

def interpret_metrics(row):
    """
    Returns a textual interpretation of sentiment trends based on metrics.

    Args:
        row (pd.Series): Contains Mean_Change, Volatility, and Net_Change.

    Returns:
        str: Interpretation string.
    """
    mean = row["Mean_Change"]
    vol = row["Volatility"]
    net = row["Net_Change"]

    if mean > 1:
        direction = "Increasing"
    elif mean < -1:
        direction = "Decreasing"
    else:
        direction = "Stable"

    if vol < 2:
        volatility_note = "Very stable"
    elif vol < 5:
        volatility_note = "Moderately stable"
    else:
        volatility_note = "High volatility"

    return f"{direction} trend with {volatility_note} changes over time."

def plot_sentiment_trend(dates, sentiment_values, ylabel, filename):
    """
    Plots a sentiment trend line across multiple time points.

    Args:
        dates (list): List of time period labels.
        sentiment_values (list): List of sentiment percentages.
        ylabel (str): Label for the Y-axis.
        filename (str): Filename to save the plot to.
    """
    plt.figure(figsize=(7, 3))
    plt.plot(dates, sentiment_values, marker='o', color='red')
    plt.ylabel(ylabel)
    plt.ylim(0, 100)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"images/{filename}.png", dpi=300, bbox_inches='tight')
    plt.show()
