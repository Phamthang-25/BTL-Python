FROM python:3.10-slim

WORKDIR /app

# Cài đặt thư viện hệ thống cần cho psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 8000

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
