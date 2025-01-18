import json
import os

import openai
from dotenv import load_dotenv
from fastapi import HTTPException

from result_request import ResultRequest

# OpenAI API 키 로드
load_dotenv(".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

async def get_openai_response(request: ResultRequest):
    try:
        prompt = (
            f"Please provide a detailed fortune reading based on the date of birth, including the following: "
            f"money_score (0-100), money_desc, money_one_line_comment, "
            f"love_score (0-100), love_desc, love_one_line_comment, "
            f"health_score (0-100), health_desc, health_one_line_comment, "
            f"job_score (0-100), job_desc, job_one_line_comment. "
            f"The scores (money_score, love_score, health_score, job_score) should be between 0 and 100. "
            f"For money, love, and health, provide a full summary for each (money_desc, love_desc, health_desc) "
            f"that gives a complete reading, in a formal tone like '~~입니다'. For job_desc, provide a detailed summary in a similarly formal tone. "
            f"Also, for each category (money, love, health, and job), provide a warm and friendly one-line comment (money_one_line_comment, "
            f"love_one_line_comment, health_one_line_comment, job_one_line_comment) in a conversational tone, ending like '해요' or '에요'. "
            f"Please ensure that the fortune reading provides advice and insights, not just scores. "
            f"Return the result as a JSON object with no additional text or explanations.\n\n"
            f"Date and time of birth (YYYYMMDD HH:MM): {request.birthday} {request.birthtime}\n"
        )





        print(prompt)



        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",  # 또는 "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a fortune teller providing luck predictions in JSON format."},
                {"role": "user", "content": prompt}
            ],

            
            temperature=0.7,
            max_tokens=1000
        )

        # API 응답에서 JSON 부분 추출
        try:
            response_text = completion.choices[0].message.content
            response_json = json.loads(response_text)
            print(response_text)
            # 필요한 필드가 모두 있는지 확인하고 기본값 설정
            return {
                "health_score": response_json.get("health_score", 0),
                "health_desc": response_json.get("health_desc", "건강 운세를 불러올 수 없습니다."),
                "love_score": response_json.get("love_score", 0),
                "love_desc": response_json.get("love_desc", "애정 운세를 불러올 수 없습니다."),
                "money_score": response_json.get("money_score", 0),
                "money_desc": response_json.get("money_desc", 0),
                "job_score": response_json.get("job_score", 0),
                "job_desc": response_json.get("job_desc", 0),
                "health_one_line_comment":response_json.get("health_one_line_comment", 0),
                "love_one_line_comment":response_json.get("love_one_line_comment", 0),
                "money_one_line_comment": response_json.get("money_one_line_comment", 0),
                "job_one_line_comment": response_json.get("job_one_line_comment", 0),
            }
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API 응답을 파싱할 수 없습니다."
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OpenAI API 호출 중 오류가 발생했습니다: {str(e)}"
        )