# Pelitodo

En esta base de datos se trata de copiar, con cierto grado de error, un esquema de una aplicación estilo [letterboxd](https://letterboxd.com/).

Para el esquema se usa MySQL y dentro de las tecnologías para la creación de las instrucciones que llenan la base de datos se usan las siguientes tecnologías:

* [httpx](https://www.python-httpx.org/)
* [trio](https://trio.readthedocs.io/en/stable/)
* [aiofiles](https://github.com/Tinche/aiofiles)
* [TMDB](https://developer.themoviedb.org/docs/getting-started)
* [faker](https://faker.readthedocs.io/en/stable/)
* [lxml](https://lxml.de/)

# Datos de prueba
Antes de levantar el servidor, debes llenar el archivo usuarios.json con un arreglo de id's de peliculas de TMDB para llenar la base de datos con datos para poder extraer reviews y los datos de peliculas.

Ejemplo de archivo usuarios.json válido:

```json
{
  "peliculas": [
    "533535-deadpool-wolverine",
    "917496",
    "1087822"
  ]
} 
```

Si no se detecta un archivo válido antes de la ejecución de extracción de datos, se mostrará una excepción y no se podrá continuar con la creación del contenedor en Docker.

Todas los datos creados serán creados en archivos SQL en la carpeta /esquema/inserts/.

# Parametros validos

Dentro de un archivo .env, que debe estar dentro de la misma carpeta que compose.yaml, se pueden agregar las siguientes variables:

* __REVIEWS__: Cantidad maxima de reviews que serán agregadas a la base de datos; es un número entre 1 y 1000.
* __PELICULAS__: Cantidad maxima de peliculas que serán agregadas a la base de datos; es un número entre 1 y 1000.

Al usar las peliculas como punto de partida para sacar las reviews y estas últimas como base para los usuarios, se tienen que tener las siguientes advertencias en cuenta:

* Los numeros dados por reviews y peliculas son mutualmente exclusivos asi que se para el proceso cuando uno llege a su limite dado por el archivo .env
* Pueden aparecer reviews en blanco, lo que no afecta a la cantidad de reviews agregadas que se tengan en el momento.
* Si solo se tiene una película como vista sin ningún tipo de review, como un corazón o una descripción, se agrega a la tabla de críticas de igual manera

# Levantar el servidor

Para usar la base de datos, es tan simple como usar el comando

```
docker compose up
```

En el directorio donde se clona este repositorio y esperar a que todos los datos sean generados.

# Tablas de idiomas y lenguajes

Las tablas de donde se parsean los datos de los [idiomas](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) y [paises](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes) son provistas por [Wikipedia](https://www.wikipedia.org/), y yo mismo copié las tablas html a los archivos txt incluidos en la carpeta /esquema/datos.
