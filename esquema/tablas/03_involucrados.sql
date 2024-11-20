create table estudio(
    id_estudio int not null auto_increment,
    nombre varchar(50) not null,
    id_pais char(2) null,
    constraint pk_estudio primary key(id_estudio)
);

create table genero(
    id_genero int not null auto_increment,
    descripcion varchar(50) not null,
    constraint pk_genero primary key(id_genero)
);

create table rol_artista(
    id_rol int not null auto_increment,
    descripcion varchar(50) not null,
    constraint pk_rol_artista primary key(id_rol)
);

create table artista(
    id_artista int not null auto_increment,
    nombre varchar(50) not null,
    apellidos varchar(100) null,
    edad int not null,
    fecha_nacimiento date null,
    fecha_deceso date null,
    constraint pk_artista primary key(id_artista)
);
