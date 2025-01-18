FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .

# pip 업그레이드 및 의존성 설치
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 코드 복사
COPY . .

# FastAPI 애플리케이션 실행 (uvicorn 사용)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
