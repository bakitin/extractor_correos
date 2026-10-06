"""Almacen: nombres de carpeta seguros para Windows y escritura a disco."""
import time
from pathlib import Path
class Almacen:
    def __init__(self, destino):                                   # guarda la carpeta raíz (Path)
        self.destino = destino

    def guardar_eml(self, cuenta, carpeta, uid, contenido, fecha, asunto, cuerpo, adjuntos):        # devuelve la ruta del archivo guardado

        asunto_seguro = self._nombre_seguro(asunto)[:50]

        fecha_texto=time.strftime("%Y-%m-%d_%H%M", fecha)

        #-------------------------------------

        nombre_carpeta_buzon = carpeta.strip('"')

        ruta_carpeta_buzon = self.destino/cuenta/nombre_carpeta_buzon

        ruta_carpeta_buzon.mkdir(parents=True, exist_ok=True)

        #-------------------------------------

        nombre_carpeta_correo = f"{fecha_texto}_uid{uid}_{asunto_seguro}"

        ruta_carpeta_correo = self.destino/cuenta/nombre_carpeta_buzon/nombre_carpeta_correo

        ruta_carpeta_correo.mkdir(parents=True, exist_ok=True)

        #-------------------------------------

        nombre_archivo = f"{uid}.eml"

        (ruta_carpeta_correo/nombre_archivo).write_bytes(contenido)

        #-------------------------------------
        
        nombre_cuerpo = "cuerpo.txt"

        (ruta_carpeta_correo/nombre_cuerpo).write_text(cuerpo, encoding="utf-8")


        #-------------------------------------

        numero = 0

        for nombre_adjunto, datos in adjuntos:

            numero += 1

            nombre = self._nombre_seguro(nombre_adjunto)

            nombre_carpeta_adjuntos = "Adjuntos"
                        
            ruta_carpeta_adjuntos = self.destino/cuenta/nombre_carpeta_buzon/nombre_carpeta_correo/nombre_carpeta_adjuntos
    
            ruta_carpeta_adjuntos.mkdir(parents=True, exist_ok=True)

            (ruta_carpeta_adjuntos/f"{numero}_{nombre}").write_bytes(datos)

        #-------------------------------------

        return fecha_texto , nombre_archivo, nombre_carpeta_buzon

    def _nombre_seguro(self, asunto):
        if not asunto:
            return "sin-asunto"
        else:
            for caracter in ':?/\\*<>|" ':
                asunto = asunto.replace(caracter, "-")
            return asunto

    # def existe(self, cuenta, carpeta, uid):
    #     ruta = Path(f"D:/Backup/Correos/{cuenta}/{carpeta}")
    #     archivos = list(ruta.glob(f"*_{uid}_*/{uid}.eml"))


    #     for archivo in archivos :
    #         print("Archivo: ",archivo)
    #         if archivo:
    #             return print(True)
    #         else:
    #             return print(False)
