create table plataforma(
    id_plataforma int not null auto_increment,
    nombre varchar(50) not null,
    constraint pk_plataforma primary key(id_plataforma)
);

create table pelicula(
    id_pelicula int not null auto_increment,
    fecha_estreno date not null,
    id_pais char(2) null,
    duracion int not null,
    constraint fk_pais_pelicula foreign key(id_pais) references pais(id_pais),
    constraint pk_pelicula primary key(id_pelicula)
);

create table imagen_pelicula(
    id_imagen_pelicula int not null auto_increment,
    id_pelicula int not null,
    url_imagen varchar(2000) not null,
    descripcion varchar(50) not null,
    constraint fk_pelicula_imagen foreign key(id_pelicula) references pelicula(id_pelicula),
    constraint pk_imagen_pelicula primary key(id_imagen_pelicula)
);

create table genero_pelicula(
    id_pelicula int not null,
    id_genero int not null,
    constraint fk_pelicula_genero foreign key(id_pelicula) references pelicula(id_pelicula),
    constraint fk_genero_pelicula foreign key(id_genero) references genero(id_genero),
    constraint pk_genero_pelicula primary key(id_pelicula, id_genero)
);

create table plataforma_pelicula(
    id_pelicula int not null,
    id_plataforma int not null,
    constraint fk_pelicula_plataforma foreign key(id_pelicula) references pelicula(id_pelicula),
    constraint fk_plataforma_pelicula foreign key(id_plataforma) references plataforma(id_plataforma),
    constraint pk_genero_pelicula primary key(id_pelicula, id_plataforma)
);

create table lenguaje_pelicula(
    id_pelicula int not null,
    id_lenguaje char(2) not null,
    constraint fk_pelicula_lenguaje foreign key(id_pelicula) references pelicula(id_pelicula),
    constraint fk_lenguaje_pelicula foreign key(id_lenguaje) references lenguaje(id_lenguaje),
    constraint pk_genero_pelicula primary key(id_pelicula, id_lenguaje)
);

create table involucrado_pelicula(
    id_artista int not null,
    id_rol int not null,
    id_pelicula int not null,
    constraint fk_artista_involucrado foreign key(id_artista) references artista(id_artista),
    constraint fk_rol_involucrado foreign key(id_rol) references rol_artista(id_rol),
    constraint fk_pelicula_involucrado foreign key(id_pelicula) references pelicula(id_pelicula),
    constraint pk_involucrados_pelicula primary key(id_artista, id_rol, id_pelicula)
);

create table estudio_pelicula(
    id_estudio int not null,
    id_pelicula int not null,
    constraint fk_estudio_pelicula foreign key(id_estudio) references estudio(id_estudio),
    constraint fk_pelicula_estudio foreign key(id_pelicula) references pelicula(id_pelicula),
    constraint pk_estudio_pelicula primary key(id_estudio, id_pelicula)
);

create table titulo_pelicula(
    id_pelicula int not null,
    id_pais char(2) not null,
    titulo_alternativo varchar(80) not null,
    constraint fk_pelicula_titulo foreign key(id_pelicula) references pelicula(id_pelicula),
    constraint fk_pais_titulo foreign key(id_pais) references pais(id_pais),
    constraint pk_estudio_pelicula primary key(id_pais, id_pelicula)
);
