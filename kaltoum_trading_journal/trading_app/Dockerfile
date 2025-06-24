FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure logs folder exists
RUN mkdir -p /app/logs

CMD ["python3", "app.py"]

