FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /goallens

COPY Pipfile Pipfile.lock /goallens/
RUN pip install pipenv && pipenv install --system

COPY . /goallens/