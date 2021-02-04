FROM python:3.9-slim-buster
LABEL maintainer="taeju.kim@nhntoast.com"

RUN mkdir /python_socket_server
WORKDIR /python_socket_server

ADD . /python_socket_server/
# CMD [ "python", "server_main.py", "10000", "10001" ]