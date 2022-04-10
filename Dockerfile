FROM snakepacker/python:all as builder

RUN python3.8 -m venv /usr/share/python3/venv \
 && /usr/share/python3/venv/bin/pip install -U pip

COPY ./requirements.txt /mnt/requirements.txt
RUN /usr/share/python3/venv/bin/pip install -r /mnt/requirements.txt
COPY db_init /mnt/DataLake/db_init
COPY create_db.py /mnt/DataLake/
RUN /usr/share/python3/venv/bin/python /mnt/DataLake/create_db.py
RUN apt-get update && apt-get install wget
RUN wget -O /mnt/DataLake/mask_rcnn_coco.h5 "https://github.com/matterport/Mask_RCNN/releases/download/v2.0/mask_rcnn_coco.h5"
COPY . /mnt/DataLake
MAINTAINER pawa
COPY deploy/entrypoint /entrypoint
RUN chmod +x /entrypoint
ENTRYPOINT ["/entrypoint"]