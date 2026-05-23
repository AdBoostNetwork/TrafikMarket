FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/backend

COPY requirements/app.txt ./
RUN pip install --no-cache-dir -r app.txt

COPY backend/app/ ./backend/app/

CMD ["python", "-m", "app.main"]
