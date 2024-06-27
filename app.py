#--------------------------------------------------------------------
from flask import Flask, request, jsonify

from flask_cors import CORS

import mysql.connector

from werkzeug.utils import secure_filename

import os
import time
#--------------------------------------------------------------------

app = Flask(__name__)
CORS(app)  # Esto habilita CORS para todas las rutas. Esto permite que el frontend de la aplicación haga solicitudes a la API desde un origen diferente (dominio, protocolo o puerto).

#import mysql.connector
class Gestion:

    #metodo constructor de la clase, inicializa una instancia de Gestion y crea conexion a la base 
    def __init__(self, host, user, password, database):

        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()
        # Intento seleccionar la base
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creo
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reservas ( 
                                nro_reserva INT AUTO_INCREMENT PRIMARY KEY, 
                                nro_habitacion INT(4) NOT NULL,
                                nro_cliente INT(8) NOT NULL, 
                                cant_ninios INT(2),
                                cant_adultos INT (2) NOT NULL, 
                                fecha_ingreso date NOT NULL,
                                fecha_egreso date NOT NULL,
                                reserva_qr VARCHAR(255))''')
        self.conn.commit()
        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    def listar_reservas(self):
        self.cursor.execute("SELECT * FROM reservas") 
        reservas = self.cursor.fetchall() 
        return reservas
    
    def consultar_reserva(self, nro_reserva):
        #consulto a partir del código de reserva
        self.cursor.execute(f"SELECT * FROM reservas WHERE nro_reserva = {nro_reserva}")
        return self.cursor.fetchone()
    
    #muestro las reserva
    def mostrar_reserva(self,nro_reserva):
        reserva = self.consultar_reserva(nro_reserva)
        if reserva:
            print("-" * 40)
            print(f"Reserva..........: {reserva['nro_reserva']}")
            print(f"Habitación.......: {reserva['nro_habitacion']}")
            print(f"Cliente..........: {reserva['nro_cliente']}")
            print(f"Niños............: {reserva['cant_ninios']}")
            print(f"Adultos..........: {reserva['cant_adultos']}")
            print(f"Ingreso..........: {reserva['fecha_ingreso']}")
            print(f"Egreso...........: {reserva['fecha_egreso']}")
            print(f"QR...............: {reserva['reserva_qr']}")
            print("-" * 40)
        else:
            print("Reserva no encontrada.")
    
    def agregar_reserva(self,nro_habitacion,nro_cliente,cant_ninios,cant_adultos,fecha_ingreso,fecha_egreso,reserva_qr):
        sql = "INSERT INTO reservas (nro_habitacion,nro_cliente,cant_ninios,cant_adultos,fecha_ingreso,fecha_egreso,reserva_qr) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        valores = (nro_habitacion,nro_cliente,cant_ninios,cant_adultos,fecha_ingreso,fecha_egreso,reserva_qr)
        
        self.cursor.execute(sql, valores) 
        self.conn.commit() 
        return self.cursor.lastrowid
      
    
    def modificar_reserva (self,nro_reserva,nuevo_nro_habitacion,nuevo_nro_cliente,nueva_cant_ninios,nueva_cant_adultos,nueva_fecha_ingreso,nueva_fecha_egreso,nuevo_reserva_qr):
        sql = "UPDATE reservas SET nro_habitacion = %s, nro_cliente = %s, cant_ninios = %s, cant_adultos = %s, fecha_ingreso = %s, fecha_egreso = %s, reserva_qr = %s WHERE nro_reserva = %s"
        valores= (nuevo_nro_habitacion,nuevo_nro_cliente,nueva_cant_ninios,nueva_cant_adultos,nueva_fecha_ingreso,nueva_fecha_egreso,nuevo_reserva_qr,nro_reserva)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0
       
    
    def eliminar_reserva(self, nro_reserva): 
        # Elimina una reserva de la tabla a partir de su nro de reserva
        self.cursor.execute(f"DELETE FROM reservas WHERE nro_reserva = {nro_reserva}") 
        self.conn.commit() 
        return self.cursor.rowcount > 0
    
#----------------------------------------------------------
# Programa principal
#----------------------------------------------------------
# gestion = Gestion(host='localhost', user='root', password='root_Admin', database='aparthotel')
gestion = Gestion(host='ggindelli.mysql.pythonanywhere-services.com', user='ggindelli', password='root_Admin', database='ggindelli$aparthotel')





# Carpeta para guardar los código QR
ruta_destino = '/home/ggindelli/mysite/img/'
#ruta_destino = './img/'
#Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere 
#ruta_destino = '/home/USUARIO/mysite/static/imagenes'

@app.route("/reservas", methods=["GET"]) #con GET recupero los datos de la reserva
def listar_reservas():
    reservas= gestion.listar_reservas()
    return jsonify(reservas)


@app.route("/reservas/<int:nro_reserva>", methods=["GET"])  #obtengo los datos con GET en base al nro_reserva
def mostrar_reserva(nro_reserva):
    reserva = gestion.consultar_reserva(nro_reserva)
    if reserva:
        return jsonify(reserva)
    else:
        return "Reserva no encontrada", 404
    

@app.route("/reservas", methods=["POST"])#con método POST puedo adicionar una nueva reserva
def agregar_reserva():
    #Recojo los datos del form agregarReserva.html
    nro_habitacion = request.form['nro_habitacion']
    nro_cliente = request.form['nro_cliente']
    cant_ninios = request.form['cant_ninios']
    cant_adultos = request.form['cant_adultos']
    fecha_ingreso = request.form['fecha_ingreso']
    fecha_egreso = request.form['fecha_egreso']
    reserva_qr = request.files['reserva_qr']
    nombre_imagen = ""

    # Genero el nombre de la imagen
    nombre_imagen = secure_filename(reserva_qr.filename) 
    nombre_base, extension = os.path.splitext(nombre_imagen) 
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" 

    nuevo_codigo = gestion.agregar_reserva(nro_habitacion, nro_cliente, cant_ninios, cant_adultos, fecha_ingreso, fecha_egreso, nombre_imagen)
    if nuevo_codigo:    
        reserva_qr.save(os.path.join(ruta_destino, nombre_imagen))
        return jsonify({"mensaje": "Reserva agregada correctamente.", "Reserva": nuevo_codigo, "QR": nombre_imagen}), 201
    else:
        return jsonify({"mensaje": "Error al agregar la reserva."}), 500


@app.route("/reservas/<int:nro_reserva>", methods=["PUT"])#con el método put puedo modificar los datos de una información ya existente
def modificar_reserva(nro_reserva):
              

    #Se recuperan los nuevos datos del formulario
    nuevo_nro_habitacion= request.form.get("nro_habitacion")
    nuevo_nro_cliente = request.form.get("nro_cliente")
    nueva_cant_ninios = request.form.get("cant_ninios")
    nueva_cant_adultos = request.form.get("cant_adultos")
    nueva_fecha_ingreso = request.form.get("fecha_ingreso")
    nueva_fecha_egreso = request.form.get("fecha_egreso")
    
    # Verifica si se proporcionó una nueva imagen
    if 'reserva_qr' in request.files:
        reserva_qr = request.files['reserva_qr']
        # Procesamiento de la imagen
        nombre_imagen = secure_filename(reserva_qr.filename) 
        nombre_base, extension = os.path.splitext(nombre_imagen) 
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" 

        # Guardar la imagen en el servidor
        reserva_qr.save(os.path.join(ruta_destino, nombre_imagen))
        
        # Busco la reserva guardada
        reserva = gestion.consultar_reserva(nro_reserva)
        if reserva: # Si existe la reserva...
            imagen_vieja = reserva["reserva_qr"]
            # Armo la ruta a la imagen
            ruta_imagen = os.path.join(ruta_destino, imagen_vieja)

            # Y si existe la borro.
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
    else:     
        reserva = gestion.consultar_reserva(nro_reserva)
        if reserva:
            nombre_imagen = reserva["reserva_qr"]

   # Se llama al método modificar_producto pasando el nro de reserva y los nuevos datos.
    if gestion.modificar_reserva(nro_reserva, nuevo_nro_habitacion, nuevo_nro_cliente, nueva_cant_ninios, nueva_cant_adultos, nueva_fecha_ingreso, nueva_fecha_egreso, nombre_imagen):
        return jsonify({"mensaje": "Reserva modificada."}), 200
    else:
        return jsonify({"mensaje": "Reserva no encontrada"}), 403

@app.route("/reservas/<int:nro_reserva>", methods=["DELETE"])
def eliminar_reserva(nro_reserva):
    # Primero, obtiene la información de la reserva para encontrar la imagen
    reserva = gestion.consultar_reserva(nro_reserva)
    if reserva:
        # Eliminar la imagen asociada si existe
        ruta_imagen = os.path.join(ruta_destino, reserva['reserva_qr'])
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

        # Luego, elimina la reserva
        if gestion.eliminar_reserva(nro_reserva):
            return jsonify({"mensaje": "Reserva eliminada"}), 200
        else:
            return jsonify({"mensaje": "Error al eliminar la reserva"}), 500
    else:
        return jsonify({"mensaje": "Reserva no encontrada"}), 404



if __name__ == "__main__":
    app.run(debug=True)

    


    