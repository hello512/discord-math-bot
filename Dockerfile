FROM python:3.8

WORKDIR /discord_math_bot

COPY Pipfile Pipfile.lock ./

RUN python -m pip install pipenv

RUN pipenv install

COPY . .

VOLUME /permanent_storage

CMD ["pipenv", "run", "python", "bot.py"]
