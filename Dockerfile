FROM python

RUN pip install noise flask

RUN mkdir /app
COPY . /app
WORKDIR /app

CMD python generate.py