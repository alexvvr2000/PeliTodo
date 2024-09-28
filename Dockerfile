FROM mysql:8.0.39-debian

COPY ./esquema/ /docker-entrypoint-initdb.d/
