from fastapi import FastAPI, HTTPException, File, UploadFile, Depends
from pydantic import BaseModel, EmailStr
from datetime import datetime
import jwt
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from decouple import config
import json
from typing import List, Optional

AWS_BUCKET_NAME = config("AWS_BUCKET_NAME")
AWS_REGION = config("AWS_REGION")
AWS_ACCESS_KEY = config("AWS_ACCESS_KEY")
AWS_SECRET_KEY = config("AWS_SECRET_KEY")

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

app = FastAPI()

# User Model
class SignUpRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    user_name: str
    password: str
    birth_date: str

class UserResponse(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    user_name: str
    email: str
    bio: Optional[str]
    profile_picture: Optional[str]
    subscription: Optional[str]
    followers: List[str] = []
    following: List[str] = []
    skills: List[str] = []
    links: List[str] = []
    like_pages: List[str] = []
    visit_count: int = 0

# Subscription Model
class Subscription(BaseModel):
    subscription_id: int
    subscription_type: str
    price: float
    start_date: datetime
    end_date: datetime

# Contact Request Model
class ContactRequest(BaseModel):
    contact_email: EmailStr
    contact_message: str

# Portfolio Model
class Portfolio(BaseModel):
    use_template: bool
    select_web_template: str
    use_portfolio_template_widget: bool
    publish: bool
    widgets: List[str] = []
    layout: str  # React-Grid-Layout JSON structure

@app.post("/sign-up", response_model=UserResponse)
async def sign_up(request: SignUpRequest):
    try:
        user_data = request.model_dump()
        s3_client.put_object(
            Body=json.dumps(user_data),
            Bucket=AWS_BUCKET_NAME,
            Key=f"users/{request.user_name}.json",
            ACL="private",
            ContentType="application/json"
        )
        return {"message": "User registered successfully"}
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/subscribe")
async def subscribe_user(subscription: Subscription):
    return {"message": "Subscription activated", "subscription": subscription}

@app.post("/contact-request")
async def contact_request(contact: ContactRequest):
    return {"message": "Contact request sent", "contact": contact}

@app.post("/portfolio")
async def create_portfolio(portfolio: Portfolio):
    try:
        s3_client.put_object(
            Body=json.dumps(portfolio.model_dump()),
            Bucket=AWS_BUCKET_NAME,
            Key=f"portfolios/{portfolio.select_web_template}.json",
            ACL="private",
            ContentType="application/json"
        )
        return {"message": "Portfolio created", "portfolio": portfolio}
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    try:
        s3_client.upload_fileobj(file.file, AWS_BUCKET_NAME, f"uploads/{file.filename}")
        return {"message": "File uploaded successfully", "file_name": file.filename}
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_name}", response_model=UserResponse)
async def get_user(user_name: str):
    try:
        response = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=f"users/{user_name}.json")
        user_data = json.loads(response["Body"].read().decode("utf-8"))
        return user_data
    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_name}")
async def delete_user(user_name: str):
    try:
        s3_client.delete_object(Bucket=AWS_BUCKET_NAME, Key=f"users/{user_name}.json")
        return {"message": "User deleted successfully"}
    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="User not found")