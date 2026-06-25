import pandas as pd
from pathlib import Path
import boto3
from dotenv import load_dotenv
load_dotenv()
import os
bucket_name=os.getenv("Bucket_Name")
excel_file = Path("../datasets/raw/Supply chain logisitcs problem.xlsx")
output_dir = Path("../datasets/csv")
output_dir.mkdir(parents=True, exist_ok=True)
s3=boto3.client('s3')
xls = pd.ExcelFile(excel_file)

for sheet in xls.sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet)

    csv_path = output_dir / f"{sheet}.csv"

    df.to_csv(csv_path, index=False)

    s3.upload_file(
        csv_path,
        bucket_name,
        f"raw/{sheet}.csv"
    )

    print(f"Uploaded succefully {sheet}.csv")

