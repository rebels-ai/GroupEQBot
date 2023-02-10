FROM python:3.8-slim

COPY . /project
WORKDIR /project

RUN apt-get update \
    && apt-get install -y -u gcc \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt requirements.txt

RUN --mount=type=cache,target=/root/.cache \
( pip install --upgrade pip \
  && pip install --upgrade -r requirements.txt \
)

CMD ["python", "./run_bot.py"]
