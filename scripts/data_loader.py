import pandas as pd

def load_clean_data(filepath):
    """
    Loads and cleans the Muslim sentiment survey data.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    df = pd.read_csv(filepath)
    df = df.drop(index=0).reset_index(drop=True)

    # Drop personally identifiable or irrelevant columns
    drop_cols = [
        'Respondent ID', 'Collector ID', 'Start Date', 'End Date',
        'IP Address', 'Email Address', 'First Name', 'Last Name',
        'Custom Data 1', 'collector_type_source', 'Device'
    ]
    df = df.drop(columns=drop_cols, errors='ignore')

    # Rename ambiguous columns
    df.rename(columns={
        'Unnamed: 11': "Religion_other",
        'Unnamed: 16': "News_other"
    }, inplace=True)

    return df