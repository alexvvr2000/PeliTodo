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
)

create table artista(
    id_artista int primary key autoincrement,
    nombre varchar(50) not null,
    apellidos varchar(100) not null,
    edad int not null,
    fecha_nacimiento date null,
    fecha_deceso not null,
)
