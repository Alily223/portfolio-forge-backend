from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from decouple import config
import json

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

class SignUpRequest(BaseModel):
    email: str
    first_name: str
    last_name: str
    user_name: str
    password: str
    birth_date: str


@app.post("/sign-up")
async def sign_up(request: SignUpRequest):
    try:
        s3_client.put_object(
            Body=json.dumps(request.model_dump()),
            Bucket=AWS_BUCKET_NAME,
            Key=f"users/{request.user_name}.json",
            ACL="public-read",
            ContentType="application/json"
        )
        return {"message": "File uploaded successfully"}
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise HTTPException(status_code=500, detail=str(e))