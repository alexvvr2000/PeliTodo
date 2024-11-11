FROM python:3.12

RUN sh -c 'if [ "$(ls /output/ | grep -E "sql" | wc -l)" -ne 0 ]; then \
    echo "Ya se tienen generados archivos de prueba, pasando a inicialización de la base de datos"; \
    exit 0; \
    fi'


COPY ./datos/peliculas.json /datos/peliculas.json

COPY ./script/requirements.txt /datos/requirements.txt
RUN pip install -r /datos/requirements.txt

COPY ./script/creacion_insert.py /datos/creacion_insert.py
RUN python /datos/creacion_insert.py
