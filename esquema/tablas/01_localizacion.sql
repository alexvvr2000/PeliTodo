create table lenguaje(
    id_lenguaje char(2) not null,
    nombre varchar(30) not null,
    constraint pk_lenguaje primary key(id_lenguaje)
);

create table pais(
    id_pais char(2) not null,
    codigo_alfa_3 char(3) not null,
    descripcion varchar(30) not null,
    constraint pk_pais primary key(id_pais)
);
