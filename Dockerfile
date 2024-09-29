FROM mysql:8.0.39-debian

COPY ./esquema/01_esquema.sql /docker-entrypoint-initdb.d/
