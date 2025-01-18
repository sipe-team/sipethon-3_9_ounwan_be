from enum import Enum

from pydantic import BaseModel, Field


class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"

class ResultRequest(BaseModel):
    name: str = Field(..., description="이름")
    gender: Gender = Field(..., description="성별 (Male/Female)")
    birthday: str = Field(..., description="생년월일 (YYYYMMDD 형식)", 
                         min_length=8, max_length=8)
    isLunar: bool = Field(..., description="음력 여부")
    birthtime: str = Field(..., description="출생 시간 (HH:MM 형식)")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "홍길동",
                "gender": "Male",
                "birthday": "19900101",
                "isLunar": True,
                "birthtime": "09:30"
            }
        }
