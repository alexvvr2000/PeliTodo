FROM mysql:8.0.39-debian

COPY ./esquema/tablas/*.sql /docker-entrypoint-initdb.d/
