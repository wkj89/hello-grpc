#!/bin/bash



if [ "$service" = "web" ]
then
  gunicorn -k gevent -b :4000 web:app
else

  python grpc_service.py
fi

