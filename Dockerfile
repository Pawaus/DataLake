FROM snakepacker/python:all as builder

RUN python3.8 -m venv /usr/share/python3/venv \
 && /usr/share/python3/venv/bin/pip install -U pip

COPY ./requirements.txt /mnt/requirements.txt
RUN /usr/share/python3/venv/bin/pip install -r /mnt/requirements.txt
COPY . /mnt/DataLake
RUN /usr/share/python3/venv/bin/python /mnt/DataLake/create_db.py
MAINTAINER pawa
COPY deploy/entrypoint /entrypoint
RUN chmod +x /entrypoint
ENTRYPOINT ["/entrypoint"]