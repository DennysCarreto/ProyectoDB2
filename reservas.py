from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLabel, QPushButton, QWidget, QLineEdit, QCalendarWidget,QGridLayout,QTableWidget,QTableWidgetItem
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QPixmap
import datetime
import os
from PyQt6.QtCore import Qt
import mysql.connector


class VentanaReservas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Módulo de Reservas")
        self.setGeometry(600, 300, 600, 400)  # X, Y, Ancho, Alto
        # Establecer imagen de fondo
        background_label = QLabel(self)
        pixmap = QPixmap("Images/login.jpg")
        background_label.setPixmap(pixmap)
        background_label.resize(pixmap.width(), pixmap.height())

        # Creamos un widget central para la ventana principal
        widget_central = QWidget()
        #self.setCentralWidget(widget_central)

        # Creamos un layout grid para organizar los botones
        layout_grid = QGridLayout(widget_central)
        self.conexion = mysql.connector.connect(
            host="192.168.204.253",
            user="Denys",
            password="admin",
            database="hotel_perza"
        )
        

        
        # Creamos los botones 
        self.boton_agregar_reserva = QPushButton("Agregar")
        layout_grid.addWidget(self.boton_agregar_reserva, 1, 5,1,1)
        self.boton_agregar_reserva.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.boton_agregar_reserva.setCursor(Qt.CursorShape.PointingHandCursor)
        # Conecta la señal de cuando el mouse entra y sale del botón a los métodos correspondientes
        self.boton_agregar_reserva.enterEvent = self.on_enter_buttonA
        self.boton_agregar_reserva.leaveEvent = self.on_leave_buttonA

        self.boton_mostrar_reserva = QPushButton("Mostar")
        layout_grid.addWidget(self.boton_mostrar_reserva, 2, 5,1,1)
        self.boton_mostrar_reserva.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.boton_mostrar_reserva.setCursor(Qt.CursorShape.PointingHandCursor)
        # Conecta la señal de cuando el mouse entra y sale del botón a los métodos correspondientes
        self.boton_mostrar_reserva.enterEvent = self.on_enter_buttonM
        self.boton_mostrar_reserva.leaveEvent = self.on_leave_buttonM

        self.etiquetaHa=QLabel("No Habitacion: ")
        layout_grid.addWidget(self.etiquetaHa, 0, 3,1,1)
        self.setHabitacion = QLineEdit(self)
        layout_grid.addWidget(self.setHabitacion, 0, 4,1,1)
        
        self.etiquetaC=QLabel("ID del cliente: ")
        layout_grid.addWidget(self.etiquetaC, 1, 3,1,1)
        self.setCliente = QLineEdit(self)
        layout_grid.addWidget(self.setCliente,1, 4,1,1)
        
        self.etiquetaP=QLabel("No de personas: ")
        layout_grid.addWidget(self.etiquetaP, 2, 3,1,1)
        self.setNoPersonas = QLineEdit(self)
        layout_grid.addWidget(self.setNoPersonas,2, 4,1,1)

        self.etiquetaN=QLabel("No de niños: ")
        layout_grid.addWidget(self.etiquetaN, 3, 3,1,1)
        self.setNoNiños = QLineEdit(self)
        layout_grid.addWidget(self.setNoNiños, 3, 4,1,1)

        self.etiquetaFE=QLabel("Fecha de entrada: ")
        layout_grid.addWidget(self.etiquetaFE, 0, 0,1,1)
        self.fecha_entrada = QCalendarWidget()
        layout_grid.addWidget(self.fecha_entrada, 1, 0,3,1)
        
        self.etiquetaFS=QLabel("Fecha de Salida: ")
        layout_grid.addWidget(self.etiquetaFS, 0, 1,1,1)
        self.fecha_salida = QCalendarWidget()
        layout_grid.addWidget(self.fecha_salida, 1, 2,3,1)
        

        self.tableWidget = QTableWidget()
        layout_grid.addWidget(self.tableWidget, 4, 0,3,5)

        
        

        self.boton_regresar = QPushButton("regresar")
        layout_grid.addWidget(self.boton_regresar, 5, 5,1,1)
        self.boton_regresar.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.boton_regresar.setCursor(Qt.CursorShape.PointingHandCursor)
        # Conecta la señal de cuando el mouse entra y sale del botón a los métodos correspondientes
        self.boton_regresar.enterEvent = self.on_enter_buttonR
        self.boton_regresar.leaveEvent = self.on_leave_buttonR

        # Establecer el layout para la ventana principal
        widget_central.setLayout(layout_grid)
        self.setCentralWidget(widget_central)

        self.boton_agregar_reserva.clicked.connect(self.agregar_reserva)
        self.boton_mostrar_reserva.clicked.connect(self.mostrar_reservas)
        self.boton_regresar.clicked.connect(self.cerrar_ventana)
        
    def registrar_bitacora(self,mensaje):
        # Obtener la ruta de la carpeta "Documentos" del usuario
        carpeta_documentos = os.path.expanduser("~/Documents")
        archivo_bitacora = os.path.join(carpeta_documentos, "bitacora_transacciones.txt")
        
        # Escribir en el archivo de bitácora
        with open(archivo_bitacora, "a") as archivo:
            fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"{fecha_hora} - {mensaje}\n")
    
    def agregar_reserva(self):
        self.FechaSeleccionada = self.fecha_entrada.selectedDate()
        self.FechaSali = self.fecha_salida.selectedDate()
        getFechaEntrada = self.FechaSeleccionada.toString("yyyy-MM-dd")
        getFechaSalida = self.FechaSali.toString("yyyy-MM-dd")
        NoHabitacion = self.setHabitacion.text()
        habitacion = int(NoHabitacion)
        idCliente = self.setCliente.text()
        cliente = int(idCliente)
        personas = self.setNoPersonas.text()
        ninios = self.setNoNiños.text()
        

        self.agregar_reservaD(getFechaEntrada,getFechaSalida,habitacion,cliente,personas,ninios)

        self.setHabitacion.clear()
        self.setCliente.clear()
        self.setNoPersonas.clear()
        self.setNoNiños.clear()
    def agregar_reservaD(self, fechaEntrada, fechaSalida,NoHabitacion, idCliente, NoPersonas, NoNiños):
        if not self.verificar_existencia_cliente(idCliente):
            mensaje = "Error: El cliente con ID {} no existe.".format(idCliente)
            self.registrar_bitacora(mensaje)
            QMessageBox.critical(self, "Error", mensaje)
            return
    
        if not self.verificar_existencia_habitacion(NoHabitacion):
            mensaje = "Error: La habitación con ID {} no existe.".format(NoHabitacion)
            self.registrar_bitacora(mensaje)
            QMessageBox.critical(self, "Error", mensaje)
            return
        if not self.verificar_disponibilidad_habitacion(NoHabitacion, fechaEntrada, fechaSalida):
            mensaje = "Error: La habitación no está disponible para las fechas seleccionadas."
            self.registrar_bitacora(mensaje)
            QMessageBox.critical(self, "Error", mensaje)
            return
        cursor = None
        try:
              # Asegurarse de que no haya transacciones activas
            if self.conexion.in_transaction:
                self.conexion.rollback()

            # Desactivar el modo autocommit
            self.conexion.autocommit = False
        
            cursor = self.conexion.cursor()

            

            # Consulta para insertar la nueva reserva
            consulta = """
            INSERT INTO reserva (fechaEntrada, FechaSalida, NoPersonas, NoNinios, Cliente_id, Habitacion_id) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            datos = (fechaEntrada,fechaSalida, NoPersonas, NoNiños, NoHabitacion, idCliente)
            cursor.execute(consulta, datos)

            # Consulta para actualizar la disponibilidad de la habitación
            consulta_actualizar_habitacion = """
            UPDATE habitacion SET Diponibilidad = 0 WHERE id = %s
            """
            cursor.execute(consulta_actualizar_habitacion, (NoHabitacion,))

            # Confirmar la transacción
            self.conexion.commit()
            mensaje = "Reserva agregada correctamente."
            self.registrar_bitacora(mensaje)
            QMessageBox.information(self, "Correcto", "Reserva agregada correctamente")

        except mysql.connector.Error as error:
            # Si ocurre un error, deshacer los cambios
            self.conexion.rollback()
            mensaje = f"Error al agregar la reserva: {error}"
            self.registrar_bitacora(mensaje)
            print(f"Error al agregar la reserva: {error}")
            QMessageBox.critical(self, "Error", "No se pudo agregar la reserva.")

        finally:
            if self.conexion.is_connected():
                cursor.close()
                print("Cursor cerrado.")
                self.conexion.autocommit = True

    def verificar_existencia_cliente(self,idCliente):
        try:
            cursor = self.conexion.cursor()
            consulta = "SELECT COUNT(*) FROM cliente WHERE id = %s"
            cursor.execute(consulta, (idCliente,))
            count = cursor.fetchone()[0]
            cursor.close()
            return count > 0
        except mysql.connector.Error as error:
            print(f"Error al verificar cliente: {error}")
            return False

    def verificar_existencia_habitacion(self,NoHabitacion):
        try:
            cursor = self.conexion.cursor()
            consulta = "SELECT COUNT(*) FROM habitacion WHERE id = %s"
            cursor.execute(consulta, (NoHabitacion,))
            count = cursor.fetchone()[0]
            cursor.close()
            return count > 0
        except mysql.connector.Error as error:
            print(f"Error al verificar habitación: {error}")
            return False   
    def verificar_disponibilidad_habitacion(self, NoHabitacion, fechaEntrada, fechaSalida):
        try:
            cursor = self.conexion.cursor()
            
            # Consulta para verificar si hay reservas que se superpongan
            consulta = """
            SELECT COUNT(*) FROM reserva
            WHERE Habitacion_id = %s
            AND (
                (fechaEntrada <= %s AND FechaSalida > %s)
                OR (fechaEntrada < %s AND FechaSalida >= %s)
                OR (fechaEntrada >= %s AND fechaEntrada < %s)
            )
            """
            
            cursor.execute(consulta, (NoHabitacion, fechaEntrada, fechaEntrada, fechaSalida, fechaSalida, fechaEntrada, fechaSalida))
            
            count = cursor.fetchone()[0]
            
            # Si count es 0, significa que no hay reservas superpuestas
            return count == 0

        except mysql.connector.Error as error:
            print(f"Error al verificar la disponibilidad de la habitación: {error}")
            return False
    
        finally:
            if cursor:
                cursor.close()
                print("Cursor cerrado en verificar_disponibilidad_habitacion.")         
    

    
    def mostrar_reservas(self):
        try:
            cursor = self.conexion.cursor()

             #Verificar la conexión antes de ejecutar la consulta
            if not self.conexion.is_connected():
                print("¡Error! La conexión no está activa.")
                return
            
            column_names = ['id','Fehca de entrada','No.Personas','No.Niños','Cliente','Habitacion']
            cursor.execute("SELECT id,fechaEntrada,NoPersonas,NoNinios,cliente_id,habitacion_id FROM reserva")
            reservas = cursor.fetchall()
            

                # Limpiar la tabla antes de mostrar nuevos datos    
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(len(reservas[0]))

             # Establecer los nombres de las columnas
            self.tableWidget.setHorizontalHeaderLabels(column_names)
            

             # Insertar filas y llenar celdas con datos
            for fila_num, fila_datos in enumerate(reservas):
                self.tableWidget.insertRow(fila_num)
                for columna_num, dato in enumerate(fila_datos):
                    celda = QTableWidgetItem(str(dato))
                    self.tableWidget.setItem(fila_num, columna_num, celda)

        except mysql.connector.Error as error:
            print(f"Error al mostrar clientes: {error}")

        finally:
        # Cerrar cursor y conexión al finalizar
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
                print("Cursor cerrado.")


    def cerrar_ventana(self):
        self.close() 
        

    def on_enter_buttonA(self, event):
        # Cambia el color de fondo del botón cuando el mouse entra
        self.boton_agregar_reserva.setStyleSheet("background-color: #94e7ff; color: #000000;")
    def on_leave_buttonA(self, event):
        # Restaura el color de fondo original del botón cuando el mouse sale
        self.boton_agregar_reserva.setStyleSheet("background-color: #ffffff; color: #000000;")

    def on_enter_buttonM(self, event):
        # Cambia el color de fondo del botón cuando el mouse entra
        self.boton_mostrar_reserva.setStyleSheet("background-color: #94e7ff; color: #000000;")
    def on_leave_buttonM(self, event):
        # Restaura el color de fondo original del botón cuando el mouse sale
        self.boton_mostrar_reserva.setStyleSheet("background-color: #ffffff; color: #000000;")

    def on_enter_buttonR(self, event):
        # Cambia el color de fondo del botón cuando el mouse entra
        self.boton_regresar.setStyleSheet("background-color: #94e7ff; color: #000000;")
    def on_leave_buttonR(self, event):
        # Restaura el color de fondo original del botón cuando el mouse sale
        self.boton_regresar.setStyleSheet("background-color: #ffffff; color: #000000;")
