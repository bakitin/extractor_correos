# extractor_correos

Herramienta de línea de comandos que respalda buzones de correo por IMAP a disco local.
Pensada para migraciones o cierres de hosting: no modifica nada en el servidor
(abre las carpetas en solo lectura y no marca mensajes como leídos).

## Características

- Varias cuentas en una sola corrida, leídas desde un CSV.
- Una carpeta por correo con el `.eml` original, el texto del cuerpo y los adjuntos.
- La fecha de modificación de cada carpeta coincide con la llegada del correo al servidor.
- Reanudable: los correos que ya están en disco se saltan sin volver a descargarse.
- Un error en un correo o en una cuenta se registra en el log y no detiene el resto.
- Solo librería estándar de Python.

## Requisitos

- Python 3.10 o superior.

## Configuración

1. Copia `.env.example` como `.env` y ajusta los valores.
2. Copia `cuentas.example.csv` como `cuentas.csv` y escribe las cuentas a respaldar, una por línea.

Si una contraseña contiene comas, escríbela entre comillas dobles:

```
correo,clave
usuario@dominio.com,"clave,con,comas"
```

Si además contiene una comilla doble `"`, se escribe dos veces: `ab"cd` queda como `"ab""cd"`.

`.env` y `cuentas.csv` están en `.gitignore`: contienen credenciales en texto plano.
Bórralos cuando termines el backup.

### Opciones del `.env`

| Clave | Descripción |
|---|---|
| `IMAP_HOST` | Servidor IMAP. Debe coincidir con la región de tus registros MX (por ejemplo, `.ovh.ca` u `.ovh.net`). |
| `IMAP_PUERTO` | Puerto IMAP con SSL, normalmente `993`. |
| `DESTINO` | Carpeta local donde se guarda el backup. |
| `CUENTAS_CSV` | Ruta del CSV de cuentas. |
| `EXTRAER_ADJUNTOS` | `si` para guardar también los adjuntos sueltos; `no` para guardar solo el `.eml` y el cuerpo. |

## Uso

Desde la carpeta del proyecto:

```
python main.py
```

Si el proceso se corta, vuelve a ejecutarlo: los correos ya guardados se saltan.

## Estructura de salida

```
DESTINO/
├── backup.log
└── usuario@dominio.com/
    └── INBOX/
        └── 2026-10-01_1015_uid45_Cotizacion-octubre/
            ├── 45.eml
            ├── cuerpo.txt
            └── Adjuntos/
                ├── 1_factura.pdf
                └── 2_image001.png
```

- **Nombre de la carpeta:** fecha y hora de llegada, UID del correo en el servidor y asunto. Los caracteres que Windows no admite se reemplazan por `-` y el asunto se recorta a 50 caracteres.
- **`<uid>.eml`:** el correo original sin modificar. Se abre con Outlook, Thunderbird o cualquier cliente de correo.
- **`cuerpo.txt`:** el texto del correo (versión en texto plano o, si no existe, la HTML).
- **`Adjuntos/`:** solo existe si el correo trae adjuntos y `EXTRAER_ADJUNTOS=si`. Cada archivo lleva un número delante para que no se pisen los nombres repetidos.
- **`backup.log`:** todo lo que se muestra en pantalla, con fecha y hora. Busca `ERROR` al terminar.

Las carpetas del buzón que no tienen correos no se crean en disco.

## Estructura del código

| Archivo | Responsabilidad |
|---|---|
| `main.py` | Punto de entrada: lee la configuración, prepara el log y arma los objetos. |
| `configuracion.py` | Lee `.env` y `cuentas.csv`. |
| `cliente_imap.py` | Único módulo que habla con el servidor IMAP. |
| `analizador.py` | Extrae asunto, cuerpo y adjuntos de los bytes del `.eml`. |
| `almacen.py` | Único módulo que escribe en disco: nombres seguros, carpetas y fechas. |
| `servicio_backup.py` | Orquesta cuentas, carpetas y correos, y aísla los errores. |

## Licencia

Pendiente.
