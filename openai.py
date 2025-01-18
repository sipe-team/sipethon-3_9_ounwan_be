import json
import os

from dotenv import load_dotenv

import openai

# OpenAI API 키 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def get_openai_response(request):
    try:
        prompt = (
            f"If I tell you the date of birth, tell me the appropriate health luck score for 2025 (0-100), affection luck score (0-100), job luck score (0-100), "
            f"monetary luck score (0-100), total score (0-100), health luck summary, affection luck summary in JSON form. "
            f"Please provide health luck summary in Korean. "
            f"Don't give me anything but JSON to answer. I just want you to give me JSON.\n\n"
            f"Date and time of birth: {request.birth_info}"
        )

        completion = await openai.ChatCompletion.acreate(
            model="gpt-4",  # 또는 "gpt-3.5-turbo"
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
            
            # 필요한 필드가 모두 있는지 확인하고 기본값 설정
            return {
                "health_score": response_json.get("health_luck_score", 0),
                "health_desc": response_json.get("health_luck_summary", "건강 운세를 불러올 수 없습니다."),
                "love_score": response_json.get("affection_luck_score", 0),
                "love_desc": response_json.get("affection_luck_summary", "애정 운세를 불러올 수 없습니다."),
                "money_score": response_json.get("monetary_luck_score", 0),
                "money_desc": "자세한 금전운은 프리미엄 서비스에서 확인하실 수 있습니다.",
                "job_score": response_json.get("job_luck_score", 0),
                "job_desc": "자세한 직장운은 프리미엄 서비스에서 확인하실 수 있습니다.",
                "health_cover": "Health cover",
                "love_cover": "Love cover",
                "money_cover": "Money cover",
                "job_cover": "Job cover"
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