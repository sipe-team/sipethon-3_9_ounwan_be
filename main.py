from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import ForecastUser

# DB 테이블 생성 (없으면 자동 생성)
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# 예제 엔드포인트: 사용자 목록 조회
# @app.get("/users/")
# def read_users(db: Session = Depends(get_db)):
#     users = db.query(User).all()
#     return users

@app.get("/results/{user_id}")
def get_results(user_id: str, db: Session = Depends(get_db)):
    db_forecast = db.query(ForecastUser).filter(ForecastUser.id == user_id).first()
    return db_forecast
    