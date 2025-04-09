from fastapi import UploadFile
import pandas as pd
import io


async def read_file(uploaded_file: UploadFile) -> pd.DataFrame:
    content = await uploaded_file.read()
    if uploaded_file.filename.endswith(".xlsx"):
        return pd.read_excel(io.BytesIO(content))
    elif uploaded_file.filename.endswith(".csv"):
        return pd.read_csv(io.BytesIO(content))
    else:
        raise ValueError("Unsupported file format. Use .xlsx or .csv.")
