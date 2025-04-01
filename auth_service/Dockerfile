FROM python:3.12
RUN apt-get update && apt-get install -y netcat-openbsd
RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

ENV ENVIRONMENT=development

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["bash", "entrypoint.sh"]
