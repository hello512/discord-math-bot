FROM python:3

WORKDIR /discord_math_bot

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv

COPY . .

CMD ["pipenv", "run", "python", "start.py"]