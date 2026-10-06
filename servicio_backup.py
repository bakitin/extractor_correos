"""ServicioBackup: orquesta cuentas, carpetas y mensajes; aísla errores por mensaje."""
class ServicioBackup:
    def __init__(self, cliente, almacen, analizador):
        self.cliente = cliente
        self.almacen = almacen
        self.analizador = analizador

    def respaldar_todas(self, cuentas):            # recorre las cuentas, con try por cuenta
        for cuenta in cuentas:
            try:
                self.respaldar_cuenta(cuenta["correo"],cuenta["clave"])

            except Exception as error:
                print("Error: ", error)

    def respaldar_cuenta(self, usuario, clave):    # conectar, carpetas, correos, desconectar

        print("Entrando a: ", usuario, " ...")
        
        self.cliente.conectar(usuario,clave)

        print("Sesion iniciada en: ", usuario)

        carpetas = self.cliente.listar_carpetas()

        print("Se inicia proceso de verificacion de correos, espere...")
        for carpeta in carpetas:
            uids = self.cliente.listar_uids(carpeta)
            
            for uid in uids:
                try:
                    # self.almacen.existe(usuario,carpeta,uid)
                
                    fecha, contenido = self.cliente.traer_correo(uid)
                    asunto = self.analizador.leer_asunto(contenido)
                    cuerpo = self.analizador.leer_cuerpo(contenido)
                    adjuntos = self.analizador.leer_adjuntos(contenido)
                    fecha_texto, nombre_archivo, carpeta_guardada = self.almacen.guardar_eml(usuario, carpeta, uid, contenido, fecha, asunto, cuerpo, adjuntos)

                    # print("Correo:",usuario,"|","Fecha:",fecha_texto, "|","Correo guardado:",uid,"|", "Guardado en:", carpeta_guardada,"|")
                except Exception as error:
                    print("Ocurrio un error al momento de hacer un backup en el Correo:",usuario, "Correo:",uid, "|", "Guardado en:",carpeta, "|" ,error)
            
            
        print("Proceso finalizado, cerrando sesion de: ", usuario)
        print("---------------------------------------------------")
        self.cliente.desconectar()
