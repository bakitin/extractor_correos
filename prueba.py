from configuracion import Configuracion
from cliente_imap import ClienteImap
from almacen import Almacen
from servicio_backup import ServicioBackup
from analizador import AnalizadorCorreo

# ----CONFIG----
configuracion = Configuracion(".env")
cuentas = configuracion.leer_cuentas()

# ----IMAP----
cliente = ClienteImap(configuracion.host, puerto = configuracion.puerto)

# ----ALMACEN----
almacen = Almacen(configuracion.destino)

# ----ANALIZADOR----
analizador = AnalizadorCorreo()


# ----PROGRAMA----
servicio = ServicioBackup(cliente, almacen, analizador)
servicio.respaldar_todas(cuentas)