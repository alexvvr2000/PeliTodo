create table lista_usuario(
    id_lista int not null auto_increment,
    id_usuario int not null,
    nombre_lista varchar(100) not null,
    constraint fk_usuario_lista foreign key(id_usuario) references usuario(id_usuario),
    constraint pk_lista_usuario primary key(id_lista)
);

create table pelicula_lista(
    id_lista int not null,
    id_pelicula int not null,
    numero_orden int null,
    constraint fk_lista_pelicula foreign key(id_lista) references lista_usuario(id_lista),
    constraint pk_pelicula_lista primary key(id_lista, id_pelicula)
);

create table critica(
    id_usuario int not null,
    id_pelicula int not null,
    corazon bool null,
    estrellas decimal(2,1) not null,
    descripcion tinytext null,
    fecha_publicacion datetime not null,
    constraint fk_usuario_critica foreign key(id_usuario) references usuario(id_usuario),
    constraint fk_pelicula_critica foreign key(id_pelicula) references pelicula(id_pelicula),
    constraint pk_critica primary key(id_pelicula, id_usuario)
);
