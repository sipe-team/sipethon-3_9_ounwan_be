# How to start

```bash
pip install -r requirements.txt
docker compose up db
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
