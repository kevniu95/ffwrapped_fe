FROM python:3.12

WORKDIR /app
COPY . /app

RUN pip install "poetry==2.0.0"
RUN poetry install --no-interaction --no-ansi

CMD ["poetry", "run", "python", "-m", "app.run"]