FROM python:3.11

ENV EMAIL_PASS jzvb umhm lisj jmkn
ENV EMAIL_USER lostipod12@gmail.com
ENV SECRET_KEY ef931caa57f5dcc01a77ba311507ade0
ENV SQLALCHEMY_DATABASE_URI sqlite:///site.db


WORKDIR /flaskblog-app

COPY requirements.txt .
COPY run.py .

RUN pip install -r requirements.txt

COPY ./flaskblog ./flaskblog
COPY ./instance ./instance

CMD ["python", "run.py"]
