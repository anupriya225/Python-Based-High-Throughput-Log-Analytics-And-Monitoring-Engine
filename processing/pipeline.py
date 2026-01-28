import dask.dataframe as dd 
from ingestion.loader import load_logs
from ingestion.parser import parse_log_line


def build_pipeline(file_path):
    bag = load_logs(file_path)
    
    parsed = (
        bag.map(parse_log_line). filter(lambda x: x is not None)
    )
    
    meta = {
        "timestamp":"object",
        "level" : "object",
        "service": "object",
        "message": "object"
    }
    
    df = parsed.to_dataframe(meta=meta)  #covert dask bag to dask dataframe
    df["timestamp"] = dd.to_datetime(df["timestamp"])
    return df


# This pipeline ingests raw logs using dask bag, parse them into 
# structured records or data by filtering invalid entires, converts and pass them into 
# a dask datframe with explict metadata and prepare them scalable analytics.