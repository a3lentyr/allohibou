FROM python

RUN pip install noise flask cairosvg

RUN mkdir /app
COPY . /app
WORKDIR /app

CMD python generate.py