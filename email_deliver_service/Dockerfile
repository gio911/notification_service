FROM python:3.9

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8003", "--reload"]

