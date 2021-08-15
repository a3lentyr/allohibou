FROM python:3.9

RUN mkdir /app
COPY requirements.txt /app

RUN pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app

CMD python main.py