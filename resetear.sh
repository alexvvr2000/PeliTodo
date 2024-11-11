#!/usr/bin/env bash

# Esto vuelve a recrear la base de datos desde 0 en caso de querer cambiar el esquema

sudo rm -rf ./mysql_data/* \
    && rm -rf ./esquema/inserts/* \
    && docker compose build \
    && docker compose up
