FROM python:3.7.2


RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN pip install flask grpcio gunicorn gevent grpcio-tools prometheus_client

RUN chmod 766 /code/deploy.sh
CMD ["/code/deploy.sh"]