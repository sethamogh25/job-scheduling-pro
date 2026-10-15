
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ap.py .
COPY index.html .

EXPOSE 5000

CMD ["python", "ap.py"]
