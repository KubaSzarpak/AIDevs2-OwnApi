FROM python:3.10.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/app/

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .