FROM python:3.9

RUN mkdir /app
COPY requirements.txt /app

RUN pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app

RUN python setup.py build_ext --inplace

CMD python main.py