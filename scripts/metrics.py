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


__all__ = ["compute_ratios_comfort"]  # optional, but nice

def compute_ratios_comfort(df, pairs=None, value_col="Percentage", cat_col="Category"):
    """
    Compute ratios like 'Very comfortable/Neutral' from a Category/Percentage table.
    """
    import pandas as pd
    s = df.set_index(cat_col)[value_col].astype(float)
    # default pairs if none provided
    if pairs is None:
        pairs = [
            ("Very comfortable", "Neutral"),
            ("Comfortable", "Neutral"),
            ("Very comfortable", "Uncomfortable"),
            ("Comfortable", "Uncomfortable")
        ]
    # clean labels
    s.index = s.index.str.strip()
    # fail fast if a category is missing
    missing = {x for p in pairs for x in p} - set(s.index)
    if missing:
        raise ValueError(f"Missing categories in data: {sorted(missing)}")

    return pd.Series({f"{a} / {b}": s[a] / s[b] for a, b in pairs}, name="Ratio")



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
