FROM snakepacker/python:all as builder

RUN python3.8 -m venv /usr/share/python3/venv \
 && /usr/share/python3/venv/bin/pip install -U pip

COPY . /mnt/
RUN /usr/share/python3/venv/bin/pip install -r /mnt/requirements.txt

MAINTAINER pawa

RUN source /usr/share/python3/venv/bin/activate
RUN flask run