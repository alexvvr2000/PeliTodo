FROM python:3.12

COPY ./datos/peliculas.json /datos/peliculas.json

COPY ./script/requirements.txt /datos/requirements.txt
RUN pip install -r /datos/requirements.txt

COPY ./script/creacion_insert.py /datos/creacion_insert.py
