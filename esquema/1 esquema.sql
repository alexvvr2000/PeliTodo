use pelitodo;

create table lenguaje(
    id_lenguaje char(2) primary key,
    nombre varchar(30) not null
);

create table pais(
    id_pais char(2) primary key,
    codigo_alfa_3 char(3),
    descripcion varchar(30)
);
