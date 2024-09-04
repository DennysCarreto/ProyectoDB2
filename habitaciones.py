from PyQt6.QtWidgets import QMainWindow, QComboBox, QTableWidgetItem, QLabel, QPushButton, QLineEdit, QWidget,QMessageBox, QTableWidget,QGridLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import mysql.connector

conexion = mysql.connector.connect(
    host="192.168.204.253",
    user="Denys",
    password="admin",
    database="hotel_perza"
)


class VentanaHabitaciones(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Módulo de Habitaciones")
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



        # Creamos los botones 
        self.boton_agregar_insumo = QPushButton("Agregar")
        layout_grid.addWidget(self.boton_agregar_insumo, 0, 3,1,1)
        self.boton_agregar_insumo.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.boton_agregar_insumo.setCursor(Qt.CursorShape.PointingHandCursor)
        # Conecta la señal de cuando el mouse entra y sale del botón a los métodos correspondientes
        self.boton_agregar_insumo.enterEvent = self.on_enter_buttonA
        self.boton_agregar_insumo.leaveEvent = self.on_leave_buttonA

        self.boton_mostrar_insumo = QPushButton("Mostar")
        layout_grid.addWidget(self.boton_mostrar_insumo, 1, 3,1,1)
        self.boton_mostrar_insumo.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.boton_mostrar_insumo.setCursor(Qt.CursorShape.PointingHandCursor)
        # Conecta la señal de cuando el mouse entra y sale del botón a los métodos correspondientes
        self.boton_mostrar_insumo.enterEvent = self.on_enter_buttonM
        self.boton_mostrar_insumo.leaveEvent = self.on_leave_buttonM

        self.boton_actualizar_Habitacion = QPushButton("Actualizar")
        layout_grid.addWidget(self.boton_actualizar_Habitacion, 2, 3,1,1)
        self.boton_actualizar_Habitacion.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.boton_actualizar_Habitacion.setCursor(Qt.CursorShape.PointingHandCursor)
        # Conecta la señal de cuando el mouse entra y sale del botón a los métodos correspondientes
        self.boton_actualizar_Habitacion.enterEvent = self.on_enter_buttonAc
        self.boton_actualizar_Habitacion.leaveEvent = self.on_leave_buttonAc

        self.boton_buscar_Habitacion = QPushButton("Buscar")
        layout_grid.addWidget(self.boton_buscar_Habitacion, 2, 4,1,1)
        self.boton_buscar_Habitacion.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.boton_buscar_Habitacion.setCursor(Qt.CursorShape.PointingHandCursor)
        # Conecta la señal de cuando el mouse entra y sale del botón a los métodos correspondientes
        self.boton_buscar_Habitacion.enterEvent = self.on_enter_buttonAc
        self.boton_buscar_Habitacion.leaveEvent = self.on_leave_buttonAc

        self.etiqueta=QLabel("Capacidad de Habitacion: ")
        layout_grid.addWidget(self.etiqueta, 0, 0,1,1)
        self.setcapacidad_de_habitacion = QLineEdit(self)
        layout_grid.addWidget(self.setcapacidad_de_habitacion, 0, 1,1,1)

        self.searchHabitacion=QLabel("numero de Habitacion: ")
        layout_grid.addWidget(self.searchHabitacion, 0, 4,1,1)
        self.searchNoHabitacion = QLineEdit(self)
        layout_grid.addWidget(self.searchNoHabitacion, 1, 4,1,1)

        self.etiqueta2=QLabel("Tipo de Habitacion: ")
        layout_grid.addWidget(self.etiqueta2, 1, 0,1,1)
        self.tipoHabitacion = QComboBox(self)
        self.tipoHabitacion.addItems(["Individual", "Doble", "Suite"])
        layout_grid.addWidget(self.tipoHabitacion, 1, 1,1,1)

        self.etiqueta4=QLabel("Disonibilidad: ")
        layout_grid.addWidget(self.etiqueta4, 2, 0,1,1)
        self.disponibilidad = QLineEdit(self)
        layout_grid.addWidget(self.disponibilidad, 2, 1,1,1)

        self.tableWidget = QTableWidget()
        layout_grid.addWidget(self.tableWidget, 3, 0,2,3)
        

        self.boton_regresar = QPushButton("regresar")
        layout_grid.addWidget(self.boton_regresar, 5, 4,1,1)
        self.boton_regresar.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.boton_regresar.setCursor(Qt.CursorShape.PointingHandCursor)
        # Conecta la señal de cuando el mouse entra y sale del botón a los métodos correspondientes
        self.boton_regresar.enterEvent = self.on_enter_buttonR
        self.boton_regresar.leaveEvent = self.on_leave_buttonR

        # Establecer el layout para la ventana principal
        widget_central.setLayout(layout_grid)
        self.setCentralWidget(widget_central)

        # Conectamos la señal clicked del botón de regresar al método de cerrar la ventana
        self.boton_agregar_insumo.clicked.connect(self.agregarHabitacion)
        self.boton_mostrar_insumo.clicked.connect(self.mostrar_Habitacion)
        self.boton_buscar_Habitacion.clicked.connect(self.buscar_Habitacion)
   
        self.boton_regresar.clicked.connect(self.cerrar_ventana)
        
    def agregarHabitacion(self):
        
        capacidad = self.setcapacidad_de_habitacion.text()
        dispo = self.disponibilidad.text()
        cap = int(capacidad)
        self.agregar_HabitacionD(cap,dispo)

        self.setcapacidad_de_habitacion.clear()
        self.disponibilidad.clear()
    def agregar_HabitacionD(self,capacidad,disponibilidad):
        try:
            cursor = conexion.cursor()

            consulta = """
            INSERT INTO habitacion (capacidad,diponibilidad) 
            VALUES (%s, %s)
            """
            datos = (capacidad,disponibilidad)
            cursor.execute(consulta, datos)

            conexion.commit()
            QMessageBox.information(self, "correct", "Habitacion agregado correctamente")

        except mysql.connector.Error as error:
            print(f"Error al agregar la habitacion: {error}")

        finally:
            if conexion.is_connected():
                cursor.close()
                print("Cursor cerrado.")
    
    def mostrar_Habitacion(self):
        try:
            cursor = conexion.cursor()

             #Verificar la conexión antes de ejecutar la consulta
            if not conexion.is_connected():
                print("¡Error! La conexión no está activa.")
                return
            
            column_names = ['id','capacidad','disponibilidad']
            cursor.execute("SELECT id,capacidad,diponibilidad FROM habitacion")
            insumos = cursor.fetchall()
            

                # Limpiar la tabla antes de mostrar nuevos datos    
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(len(insumos[0]))

             # Establecer los nombres de las columnas
            self.tableWidget.setHorizontalHeaderLabels(column_names)
            

             # Insertar filas y llenar celdas con datos
            for fila_num, fila_datos in enumerate(insumos):
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
    def buscar_Habitacion(self):
        id = self.searchNoHabitacion.text()
        try:
            cursor = conexion.cursor()
             # Verificar la conexión antes de ejecutar la consulta
            if not conexion.is_connected():
                print("¡Error! La conexión no está activa.")
                return
            cursor.execute("SELECT capacidad FROM habitaciones WHERE id_habitacion = %s", (id,))
            result = cursor.fetchone()
            if result:
                capacidad = result[0]  # Acceder al primer elemento de la tupla
                self.setcapacidad_de_habitacion.setText(str(capacidad))  # Convertir a str si es necesario
            else:
                print(f"No se encontró ninguna habitación con el ID {id}.")
        except mysql.connector.Error as error:
            print(f"Error al mostrar habitación: {error}")
        finally:
        # Cerrar cursor y conexión al finalizar
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
                print("Cursor cerrado.")

    def cerrar_ventana(self):
        self.close()
    def on_enter_buttonA(self, event):
        # Cambia el color de fondo del botón cuando el mouse entra
        self.boton_agregar_insumo.setStyleSheet("background-color: #94e7ff; color: #000000;")
    def on_leave_buttonA(self, event):
        # Restaura el color de fondo original del botón cuando el mouse sale
        self.boton_agregar_insumo.setStyleSheet("background-color: #ffffff; color: #000000;")

    def on_enter_buttonM(self, event):
        # Cambia el color de fondo del botón cuando el mouse entra
        self.boton_mostrar_insumo.setStyleSheet("background-color: #94e7ff; color: #000000;")
    def on_leave_buttonM(self, event):
        # Restaura el color de fondo original del botón cuando el mouse sale
        self.boton_mostrar_insumo.setStyleSheet("background-color: #ffffff; color: #000000;")

    def on_enter_buttonR(self, event):
        # Cambia el color de fondo del botón cuando el mouse entra
        self.boton_regresar.setStyleSheet("background-color: #94e7ff; color: #000000;")
    def on_leave_buttonR(self, event):
        # Restaura el color de fondo original del botón cuando el mouse sale
        self.boton_regresar.setStyleSheet("background-color: #ffffff; color: #000000;")
    def on_enter_buttonAc(self, event):
        # Cambia el color de fondo del botón cuando el mouse entra
        self.boton_actualizar_Habitacion.setStyleSheet("background-color: #94e7ff; color: #000000;")
    def on_leave_buttonAc(self, event):
        # Restaura el color de fondo original del botón cuando el mouse sale
        self.boton_actualizar_Habitacion.setStyleSheet("background-color: #ffffff; color: #000000;")
    
    def on_enter_buttonBus(self, event):
        # Cambia el color de fondo del botón cuando el mouse entra
        self.boton_buscar_Habitacion.setStyleSheet("background-color: #94e7ff; color: #000000;")
    def on_leave_buttonBus(self, event):
        # Restaura el color de fondo original del botón cuando el mouse sale
        self.boton_buscar_Habitacion.setStyleSheet("background-color: #ffffff; color: #000000;")

