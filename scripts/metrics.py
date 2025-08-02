def compute_sentiment_ratios(df, col):
    """
    Computes the positive-to-negative and positive-to-neutral sentiment ratios.

    Args:
        df (pd.DataFrame): DataFrame containing the sentiment column.
        col (str): Name of the sentiment column.

    Returns:
        tuple: (positive_to_negative_ratio, positive_to_neutral_ratio)
    """
    counts = df[col].value_counts()
    ratio_pos_neg = counts.get("Good", 0) / counts.get("Bad", 1)
    ratio_pos_neutral = counts.get("Good", 0) / counts.get("Neutral", 1)
    return ratio_pos_neg, ratio_pos_neutral

def get_sentiment_proportions(df, col):
    """
    Calculates the percentage of each sentiment category in a given column.

    Args:
        df (pd.DataFrame): DataFrame containing the sentiment column.
        col (str): Name of the sentiment column.

    Returns:
        pd.DataFrame: DataFrame with columns ['Category', 'Percentage']
    """
    prop = df[col].value_counts(normalize=True).reset_index()
    prop.columns = ['Category', 'Percentage']
    prop['Percentage'] *= 100
    return prop
