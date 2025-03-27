FROM python:3.9

WORKDIR /consumer

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/consumer


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY consumer/ /consumer/

CMD ["python", "start_worker.py"]
