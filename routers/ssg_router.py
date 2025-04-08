from typing import Union
from fastapi import APIRouter
from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/ssg", tags=["SSG"])


@router.post("/generate")
async def generate_ssg(employee_details: UploadFile = File(...),
                       previous_year_ssa: UploadFile | None = File(None)):

    employee_details_contents = await employee_details.read()
    df = pd.read_excel(io.BytesIO(employee_details_contents)) if employee_details.filename.endswith(
        ".xlsx") else pd.read_csv(io.BytesIO(employee_details_contents))
    # print("employee_details", df)

    # copy the dataframe
    secret_df = df.copy()

    while True:
        # shuffle the dataframe
        shuffled_df = df.sample(frac=1).reset_index(drop=True)
        # print(shuffled_df.equals(secret_df))
        print(any(df["Employee_EmailID"] == shuffled_df["Employee_EmailID"]))
        if not any(df["Employee_EmailID"] == shuffled_df["Employee_EmailID"]):
            break

    # update the secret child with shuffled data
    secret_df["Secret_Child_Name"] = shuffled_df["Employee_Name"]
    secret_df["Secret_Child_EmailID"] = shuffled_df["Employee_EmailID"]

    # create xlsx file
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        secret_df.to_excel(writer, index=False, sheet_name="SSG")
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={"Content-Disposition": f"attachment; filename=SSG.xlsx"}
    )
