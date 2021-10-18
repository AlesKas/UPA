FROM python:latest

ADD /src/* /usr/src/
WORKDIR /usr/src/

RUN pip install pipenv
RUN pipenv install --ignore-pipfile --deploy --system