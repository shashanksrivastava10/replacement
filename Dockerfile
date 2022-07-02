FROM python:3

WORKDIR /usr/src/app

COPY replacement.py ./
ENV FLASK_APP=replacement
RUN pip install flask-restful

ENTRYPOINT flask run --host=0.0.0.0
