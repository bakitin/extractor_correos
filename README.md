# extractor_correos

Herramienta de línea de comandos que respalda buzones de correo por IMAP a disco local.
Pensada para migraciones o cierres de hosting: no modifica nada en el servidor
(abre las carpetas en solo lectura y no marca mensajes como leídos).

## Características

- Un directorio por correo con el `.eml` original, el texto del cuerpo y los adjuntos.
- La fecha del directorio coincide con la fecha de llegada del correo al servidor.
- Reanudable: los mensajes ya respaldados se saltan.
- Un error en un mensaje se registra en el log y no detiene el resto.
- Solo librería estándar de Python.

## Requisitos

- Python 3.10 o superior.

## Configuración

1. Copia `.env.example` como `.env` y ajusta los valores.
2. Copia `cuentas.example.csv` como `cuentas.csv` y escribe las cuentas a respaldar.

`.env` y `cuentas.csv` están en `.gitignore`: contienen credenciales en texto plano.
Bórralos cuando termines el backup.

## Uso

```
python -m extractor_correos
```

## Estructura de salida

```
DESTINO/
└── usuario@dominio.com/
    └── INBOX/
        └── 2026-10-01_1015_uid45_Cotizacion-octubre/
            ├── mensaje.eml
            ├── cuerpo.txt
            └── adjuntos/
```

## Pruebas

```
python -m unittest discover tests
```

## Licencia

Pendiente.


## De tu mensaje inicial quedan pendientes estos puntos de diseño:

Reanudable: si un correo ya está en disco, se salta. Con 27 cuentas es el más valioso, porque si algo se corta a mitad de camino no vuelves a descargar todo.
Fecha de la carpeta: que la fecha de modificación coincida con la llegada del correo, como pediste al principio.
Log en archivo: que los errores queden escritos en un archivo y no solo en pantalla.
Opciones del .env: CARPETAS y EXTRAER_ADJUNTOS existen, pero el código todavía no las usa.
Dejarlo listo para GitHub: prueba.py pasa a main.py, actualizar README y .env.example, y sacar IMAP_USUARIO e IMAP_CLAVE del .env.