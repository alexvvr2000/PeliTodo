FROM mysql:8.0.39-debian

COPY ./esquema/*.sql /docker-entrypoint-initdb.d/
