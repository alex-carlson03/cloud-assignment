import time
import io
import json
import os
from azure.storage.blob import BlobServiceClient
import pandas as pd

_connect_str = ("DefaultEndpointsProtocol=http;"
                "AccountName=devstoreaccount1;"
                "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
                "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;")

# Client is created once at module load and reused on every invocation.
# In a real serverless environment the module stays loaded between warm calls,
# so this avoids re-establishing the SDK connection on each trigger.
_blob_client = BlobServiceClient.from_connection_string(_connect_str)

def process_nutritional_data_from_azurite():
    t_start = time.perf_counter()

    blob = _blob_client.get_blob_client("datasets", "All_Diets.csv")
    stream = blob.download_blob().readall()
    df = pd.read_csv(io.BytesIO(stream))

    avg_macros = df.groupby("Diet_type")[["Protein(g)", "Carbs(g)", "Fat(g)"]].mean()
    result = avg_macros.round(2).reset_index().to_dict(orient="records")

    os.makedirs("simulated_nosql", exist_ok=True)
    with open("simulated_nosql/results.json", "w") as f:
        json.dump(result, f, indent=4)

    elapsed = time.perf_counter() - t_start
    return f"Data processed and stored in simulated_nosql/results.json (took {elapsed:.3f}s)"

# Two back-to-back calls to show the second is faster because the
# BlobServiceClient is already initialized and its HTTP session is warm.
print("Invocation 1:", process_nutritional_data_from_azurite())
print("Invocation 2:", process_nutritional_data_from_azurite())
