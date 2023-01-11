FROM python:3.11

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/

RUN python3 -m pip install -r requirements.txt

COPY . /usr/src/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
