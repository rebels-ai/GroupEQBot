FROM python:3.8-slim

COPY . /project
WORKDIR /project

RUN apt-get update \
    && apt-get install -y -u gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "./run_bot.py"]
