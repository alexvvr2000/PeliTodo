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

create table usuario(
    id_usuario int primary key autoincrement,
    correo_electronico varchar(254) not null,
    nombre_usuario varchar(50) not null,
    salt_clave char(64) not null,
    clave_acceso char(64) not null,
    fecha_creacion datetime not null,
    fecha_baja datetime not null,
    id_pais char(2) not null,
    constraint fk_pais_usuario foreign key(id_pais) references pais(id_pais)
)

create table plataforma_cuenta_externa(
    id_plataforma int primary key autoincrement,
    nombre varchar(50) not null,
    url varchar(2000) not null,
    url_icono varchar(2000) not null
);

create table cuenta_externa_usuario(
    id_usuario int,
    id_plataforma int,
    usuario_externo varchar(100) not null,
    constraint fk_usuario_cuenta foreign key(id_usuario) references usuario(id_usuario),
    constraint fk_plataforma_usuario foreign key(id_plataforma) references plataforma_cuenta_externa(id_plataforma),
    constraint pk_cuenta_usuario foreign key(id_usuario, id_plataforma)
);

create table estudio(
    id_estudio int primary key autoincrement,
    nombre varchar(50) not null,
    pagina_oficial varchar(2000) null,
    id_pais char(2) null,
    fecha_fundacion date null,
    fecha_cierre date null
);

create table genero(
    id_genero int primary key autoincrement,
    descripcion varchar(50) not null,
);

create table rol_artista(
    id_rol int primary key autoincrement,
    descripcion varchar(50) not null,
);

create table artista(
    id_artista int primary key autoincrement,
    nombre varchar(50) not null,
    apellidos varchar(100) not null,
    edad int not null,
    fecha_nacimiento date null,
    fecha_deceso not null,
);

create table plataforma(
    id_plataforma int primary key autoincrement,
    nombre varchar(50) not null,
    url varchar(2000) not null,
);

create table pelicula(
    id_pelicula int primary key autoincrement,
    fecha_estreno date not null,
    id_pais char(2) null,
    duracion int not null,
    constraint fk_pais_pelicula foreign key(id_pais) references pais(id_pais)
)

create table imagen_pelicula(
    id_imagen_pelicula int primary key autoincrement,
    id_pelicula int not null,
    url_imagen varchar(2000) not null,
    descripcion varchar(50) not null,
    constraint fk_pelicula_imagen foreign key(id_pelicula) references pelicula(id_pelicula)
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
    constraint fk_lenguaje_pelicula foreign key(id_lenguaje) references pelicula(id_lenguaje),
    constraint pk_genero_pelicula primary key(id_pelicula, id_lenguaje)
);

create table involucrado_pelicula(
    id_artista int not null,
    id_rol int not null,
    id_pelicula not null,
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
)

create table titulo_pelicula(
    id_pelicula int not null,
    id_pais char(2) not null,
    titulo_alternativo varchar(80) not null,
    constraint fk_pelicula_titulo foreign key(id_pelicula) references pelicula(id_pelicula),
    constraint fk_pais_titulo foreign key(id_pais) references pais(id_pais),
    constraint pk_estudio_pelicula primary key(id_pais, id_pelicula)
);

create table lista_usuario(
    id_lista int primary key autoincrement,
    id_usuario int not null,
    nombre_lista varchar(100) not null,
    constraint fk_usuario_lista foreign key(id_usuario) references usuario(id_usuario)
);

create table pelicula_lista(
    id_lista int not null,
    id_pelicula int not null,
    numero_orden int null,
    constraint fk_lista_pelicula foreign key(id_lista) references lista_usuario(id_lista),
    constraint pk_pelicula_lista primary key(id_lista, id_pelicula)
);
