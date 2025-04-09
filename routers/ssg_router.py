from fastapi import APIRouter
from fastapi import UploadFile, File
import pandas as pd
import io
from fastapi.responses import StreamingResponse

from services.ssg_generator import SecretSantaGenerator
from utils.file_handler import read_file

router = APIRouter(prefix="/ssg", tags=["SSG"])


@router.post("/generate")
async def generate_ssg(employee_details: UploadFile = File(...),
                       previous_year_ssa: UploadFile | None = File(None)):
    try:
        # read employee details file
        df = await read_file(employee_details)

        # Load previous year assignments if available
        previous_assignments = set()
        if previous_year_ssa:
            # read previous year file
            prev_df = await read_file(previous_year_ssa)

            if {"Employee_EmailID", "Secret_Child_EmailID"}.issubset(prev_df.columns):
                previous_assignments = set(
                    zip(prev_df["Employee_EmailID"], prev_df["Secret_Child_EmailID"]))

        # generate secret santa assignments
        generator = SecretSantaGenerator(df, previous_assignments)
        secret_df = generator.generate_secret_santa()

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
    except Exception as e:
        return {"error": str(e)}
