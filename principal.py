import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox, \
    QGridLayout, QLabel, QMenuBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QAction, QFont
from clientes import VentanaClientes
from reservas import VentanaReservas
from habitaciones import VentanaHabitaciones
from insumos import VentanaInsumo
from RegistroUsuario import VentanaRegistro
from facturas import VentasFacturas
import subprocess

import shutil

import datetime

class VentanaPrincipal(QMainWindow):
    def __init__(self, id_usuario, nombre, apellido, cargo):
        super().__init__()
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.cargo = cargo

        self.setWindowTitle(f"Sistema de Gestión de Hotel - {self.nombre} {self.apellido}")
        self.setGeometry(100, 100, 800, 600)  # Aumenta el tamaño de la ventana

        # Establecer imagen de fondo
        background_label = QLabel(self)
        pixmap = QPixmap("Images/login.jpg")
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        self.setCentralWidget(background_label)

        # Creamos un widget central para la ventana principal
        widget_central = QWidget(self)
        layout_grid = QGridLayout(widget_central)

        # Definir estilo de los botones
        estilo_boton = """
        QPushButton {
            background-color: #2d89ef;
            color: white;
            border-radius: 10px;
            font-size: 16px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #1e70bf;
        }
        """

        # Crear botones para los diferentes módulos
        self.boton_reservas = QPushButton("Módulo de Reservas")
        layout_grid.addWidget(self.boton_reservas, 0, 0, 1, 1)
        self.boton_reservas.setStyleSheet(estilo_boton)
        self.boton_reservas.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_reservas.clicked.connect(self.abrir_modulo_reservas)

        self.boton_habitaciones = QPushButton("Módulo de Habitaciones")
        layout_grid.addWidget(self.boton_habitaciones, 0, 1, 1, 1)
        self.boton_habitaciones.setStyleSheet(estilo_boton)
        self.boton_habitaciones.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_habitaciones.clicked.connect(self.abrir_modulo_habitaciones)

        self.boton_ventas = QPushButton("Módulo de Ventas/Facturas")
        layout_grid.addWidget(self.boton_ventas, 1, 0, 1, 1)
        self.boton_ventas.setStyleSheet(estilo_boton)
        self.boton_ventas.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_ventas.clicked.connect(self.abrir_modulo_ventas)

        self.boton_insumos = QPushButton("Módulo de Insumos")
        layout_grid.addWidget(self.boton_insumos, 1, 1, 1, 1)
        self.boton_insumos.setStyleSheet(estilo_boton)
        self.boton_insumos.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_insumos.clicked.connect(self.abrir_modulo_insumos)

        self.boton_clientes = QPushButton("Módulo de Clientes")
        layout_grid.addWidget(self.boton_clientes, 2, 0, 1, 1)
        self.boton_clientes.setStyleSheet(estilo_boton)
        self.boton_clientes.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_clientes.clicked.connect(self.abrir_modulo_clientes)

        self.boton_cerrar_sesion = QPushButton("Cerrar Sesión")
        layout_grid.addWidget(self.boton_cerrar_sesion, 2, 1, 1, 1)
        self.boton_cerrar_sesion.setStyleSheet(estilo_boton)
        self.boton_cerrar_sesion.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_cerrar_sesion.clicked.connect(self.cerrar_sesion)

        # Botón de Registrar (solo para Gerentes)
        if self.cargo.lower() == 'gerente':
            self.boton_registrar = QPushButton("Registrar")
            layout_grid.addWidget(self.boton_registrar, 3, 0, 1, 1)
            self.boton_registrar.setStyleSheet(estilo_boton)
            self.boton_registrar.setCursor(Qt.CursorShape.PointingHandCursor)
            self.boton_registrar.clicked.connect(self.abrir_registrar)
            
            self.boton_backup = QPushButton("Backup")
            layout_grid.addWidget(self.boton_backup, 3, 1, 1, 1)
            self.boton_backup.setStyleSheet(estilo_boton)
            self.boton_backup.setCursor(Qt.CursorShape.PointingHandCursor)
            self.boton_backup.clicked.connect(self.realizar_backup)

        # Establecer el layout para el widget central
        widget_central.setLayout(layout_grid)
        self.setCentralWidget(widget_central)

    # Métodos para abrir cada módulo
    def abrir_modulo_reservas(self):
        self.ventana_reservas = VentanaReservas()
        self.ventana_reservas.show()

    def abrir_modulo_habitaciones(self):
        self.ventana_habitaciones = VentanaHabitaciones()
        self.ventana_habitaciones.show()

    def abrir_modulo_ventas(self):
        self.ventana_facturas = VentasFacturas()
        self.ventana_facturas.show()

    def abrir_modulo_insumos(self):
        self.ventana_insumo = VentanaInsumo()
        self.ventana_insumo.show()

    def abrir_modulo_clientes(self):
        self.ventana_clientes = VentanaClientes()
        self.ventana_clientes.show()

    def abrir_registrar(self):
        self.ventana_registrar = VentanaRegistro()
        self.ventana_registrar.show()

    def cerrar_sesion(self):
        self.close()

    def mostrar_ventana_principal(self):
        self.show()


    def realizar_backup(self):
        try:
            # Obtener la fecha y hora actual para el nombre del archivo de backup
            fecha_hora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{fecha_hora}_backup.sql"
            
            # Definir las rutas de backup
            backup_path_local = f"C:\\Users\\DavidG2\\Documents\\backupLocal\\{backup_filename}"
            backup_path_red = f"\\\\DESKTOP-TA8QMIP\\Users\\Public\\Backups\\{backup_filename}"
            
            # Contraseña para MySQL
            password = 'admin'
            
            # Comando mysqldump para crear el backup en la ruta local
            comando_local = f"mysqldump -u root -p{password} hotel_perza > \"{backup_path_local}\""
            
            # Ejecutar el comando para la ubicación local
            result_local = subprocess.run(comando_local, shell=True, check=True)
            
            # Comprobar si el comando se ejecutó correctamente para la ubicación local
            if result_local.returncode == 0:
                print(f"Backup creado en la ubicación local: {backup_path_local}")
                
                # Copiar el archivo de la ubicación local a la red
                shutil.copy(backup_path_local, backup_path_red)
                print(f"Backup copiado a la ubicación de red: {backup_path_red}")
                
                QMessageBox.information(self, "Backup", "Backup creado exitosamente en ambas ubicaciones.")
            else:
                print(f"Error al crear el backup en la ubicación local: Código de retorno {result_local.returncode}")
                QMessageBox.critical(self, "Error", "Error al crear el backup en la ubicación local.")
        
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el comando mysqldump: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al crear el backup: {str(e)}")
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")