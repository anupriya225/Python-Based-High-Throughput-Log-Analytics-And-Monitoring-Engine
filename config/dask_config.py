#to separate configuration from business logice
#code is clean and easy for reusable
from dask.distributed import LocalCluster,Client

def start_dask():
    cluster = LocalCluster(
        n_workers=3,
        threads_per_worker=3,
        memory_limit="1GB",
        dashboard_address=":8790"
    )
    return Client(cluster)
#raw data ->[ convet unstructured data into structure data]
#parsing _>translating
