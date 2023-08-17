FROM python:3.9

WORKDIR /app

COPY ./app /code/app

RUN pip install redis[hiredis]

CMD ["python", "watch_socket_server.py"]