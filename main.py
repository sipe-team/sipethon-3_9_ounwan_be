import hashlib
import json
from datetime import datetime
from enum import Enum

from fastapi import FastAPI, HTTPException

from database import Base, SessionLocal, engine
from models import ForecastUser
from openai import get_openai_response
from result_request import ResultRequest

# DB 테이블 생성 (없으면 자동 생성)
Base.metadata.create_all(bind=engine)

def validate_date_format(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y%m%d")
        return True
    except ValueError:
        return False

def validate_time_format(time_str: str) -> bool:
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def generate_hash_id(data: dict) -> str:
    """Generate a 16-character hash from the JSON data"""
    json_str = json.dumps(data, sort_keys=True)
    hash_object = hashlib.sha256(json_str.encode())
    return hash_object.hexdigest()[:8]  # Take first 8 characters of the hash

app = FastAPI()

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/results")
async def generate_results(request: ResultRequest):
    # 날짜 형식 검증
    if not validate_date_format(request.birthday):
        raise HTTPException(
            status_code=400,
            detail="생년월일 형식이 잘못되었습니다. YYYYMMDD 형식으로 입력해주세요."
        )
    
    # 시간 형식 검증
    if not validate_time_format(request.birthtime):
        raise HTTPException(
            status_code=400,
            detail="출생시간 형식이 잘못되었습니다. HH:MM 형식으로 입력해주세요."
        )
    
    request_dict = request.model_dump()
    hash_id = generate_hash_id(request_dict)
    
    db = SessionLocal()
    try:
        existing_record = db.query(ForecastUser).filter(ForecastUser.id == hash_id).first()
        if existing_record:
            print('existing_record')
            return existing_record
        # openai_response = await get_openai_response(request)
        mock_openai_response = {
            "health_score": 90,
            "health_desc": "You will have a great health",
            "love_score": 80,
            "love_desc": "You will have a great love",
            "money_score": 70,
            "money_desc": "You will have a great money",
            "job_score": 60,
            "job_desc": "You will have a great job",
            "health_cover": "Health cover",
            "love_cover": "Love cover",
            "money_cover": "Money cover",
            "job_cover": "Job cover"
        }
        # DB에 저장
        user = ForecastUser(
            id=hash_id,
            health_score=mock_openai_response["health_score"],
            love_score=mock_openai_response["love_score"],
            money_score=mock_openai_response["money_score"],
            job_score=mock_openai_response["job_score"],
            health_desc=mock_openai_response["health_desc"],
            love_desc=mock_openai_response["love_desc"],
            money_desc=mock_openai_response["money_desc"],
            job_desc=mock_openai_response["job_desc"],
            health_cover=mock_openai_response["health_cover"],
            love_cover=mock_openai_response["love_cover"],
            money_cover=mock_openai_response["money_cover"],
            job_cover=mock_openai_response["job_cover"]
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()
