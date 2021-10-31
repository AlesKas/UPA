FROM python:latest

ADD /src/* /usr/src/
WORKDIR /usr/src/

RUN python3.10 -m pip install pipenv

RUN pipenv install --skip-lock --deploy --system