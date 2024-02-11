FROM python:3.11-alpine


WORKDIR /app

COPY Pipfile.lock /app/
COPY Pipfile /app/

RUN pip install pipenv
RUN pipenv install --ignore-pipfile --skip-lock

COPY . /app/

CMD pipenv run python main.py
