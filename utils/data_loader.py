import os
import pandas as pd
import pyarrow.parquet as pq

def load_parquet_file(filepath: str) -> pd.DataFrame:
    """
    Loads a single LILA BLACK Parquet file into a Pandas DataFrame.
    
    Args:
        filepath (str): Path to the Parquet file (e.g. .nakama-0 file)
        
    Returns:
        pd.DataFrame: A formatted pandas dataframe of the event data
    """
    # Read the parquet table, PyArrow handles it regardless of the file extension
    table = pq.read_table(filepath)
    df = table.to_pandas()
    
    # Decode the event column from bytes to string
    if 'event' in df.columns:
        df['event'] = df['event'].apply(
            lambda x: x.decode('utf-8') if isinstance(x, bytes) else x
        )
        
    # Fix timestamp parsing (Nakama stores seconds, but Parquet schema claims ms)
    if 'ts' in df.columns:
        df['ts'] = pd.to_datetime(df['ts'].astype('int64'), unit='s')
        
    # Ensure match_id is a string if it exists
    if 'match_id' in df.columns:
        df['match_id'] = df['match_id'].astype(str)
        
    # Create the user_type column (Numeric = Bot, UUID = Human)
    if 'user_id' in df.columns:
        # A simple way to check if it's numeric is to use str.isnumeric()
        df['user_type'] = df['user_id'].apply(
            lambda x: 'Bot' if str(x).isnumeric() else 'Human'
        )
        
    return df
