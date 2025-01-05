from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from decouple import config

AWS_BUCKET_NAME = config("AWS_BUCKET_NAME")
AWS_REGION = config("AWS_REGION")
AWS_ACCESS_KEY = config("AWS_ACCESS_KEY")
AWS_SECRET_KEY = config("AWS_SECRET_KEY")

s3_client = boto3.client(
    "s3",
    region_name = AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

app = FastAPI()
# logfire.instrument_fastapi(app)

@app.post("/save")
async def save_string_to_s3(key: str, value: str):
    try:
        s3_client.put_object(
            Bucket=AWS_BUCKET_NAME,
            Key=key,
            Body=value,
            ContentType="text/plain"
        )
        return {"message": f"string saved to S3 with key '{key}'"}
    except (NoCredentialsError, PartialCredentialsError):
        raise HTTPException(status_code=500, detail="AWS credentials are not configured properly.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/retrieve")
async def retrieve_string_from_s3(key: str):
    try:
        response = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=key)
        data = response["Body"].read().decode("utf-8")
        return {"key": key, "value": data}
    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail=f"No string found with key '{key}'")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))