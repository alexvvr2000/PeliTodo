FROM mysql:8.0.39-debian

COPY ./esquema/1 esquema.sql /docker-entrypoint-initdb.d/
