import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QCheckBox
from principal import VentanaPrincipal
from Conexion import *
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
import mysql.connector


class VentanaLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setGeometry(600, 300, 280, 150)
        self.initUI()
        self.conexion = self.conectar_a_base_de_datos()

    def conectar_a_base_de_datos(self):
        try:
            conexion = mysql.connector.connect(
                host="192.168.204.253",
                user="Denys",
                password="admin",
                database="hotel_perza"
            )
            return conexion
        except mysql.connector.Error as error:
            QMessageBox.warning(self, 'Error de conexión', f'No se pudo conectar a la base de datos: {error}')
            return None

    def encriptarContraseña(self, contrasena):
        clave = 3  # Desplazamiento para el cifrado (puedes elegir cualquier número)

        contrasena_encriptada = ""
        for caracter in contrasena:
            if caracter.isalpha():
                nuevo_caracter = chr(((ord(caracter) - ord('a' if caracter.islower() else 'A') + clave) % 26) + ord('a' if caracter.islower() else 'A'))
                contrasena_encriptada += nuevo_caracter
            else:
                contrasena_encriptada += caracter

        return contrasena_encriptada

    def validar_credenciales(self):
        usuario = self.entrada_usuario.text()
        contraseña = self.entrada_password.text()
        contraseniaE = self.encriptarContraseña(contraseña)

        if self.conexion:
            cursor = self.conexion.cursor()
            try:
                cursor.execute("SELECT id, nombre, apellido, cargo FROM usuarios WHERE usuario = %s AND contrasenia = %s", (usuario, contraseniaE))
                resultado = cursor.fetchone()
                if resultado:
                    id_usuario, nombre, apellido, cargo = resultado
                    self.abrir_ventana_principal(id_usuario, nombre, apellido, cargo)
                else:
                    QMessageBox.warning(self, 'Login Fallido', 'Usuario o contraseña incorrectos.')
            except mysql.connector.Error as error:
                QMessageBox.warning(self, 'Error en consulta', f'Error al realizar la consulta: {error}')
            finally:
                cursor.close()
        else:
            QMessageBox.warning(self, 'Error de conexión', 'No hay conexión con la base de datos.')

    def mostrar_contrasenia(self, clicked):
        if clicked:
            self.entrada_password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.entrada_password.setEchoMode(QLineEdit.EchoMode.Password)

    def on_enter_button(self, event):
        self.boton_login.setStyleSheet("background-color: #94e7ff; color: #000000;")

    def on_leave_button(self, event):
        self.boton_login.setStyleSheet("background-color: #ffffff; color: #000000;")

    def abrir_ventana_principal(self, id_usuario, nombre, apellido, cargo):
        self.ventana_principal = VentanaPrincipal(id_usuario, nombre, apellido, cargo)
        self.ventana_principal.show()
        self.close()

    def initUI(self):
        layout = QVBoxLayout()
        # Establecer imagen de fondo
        background_label = QLabel(self)
        pixmap = QPixmap("Images/login.png")
        background_label.setPixmap(pixmap)
        background_label.resize(pixmap.width(), pixmap.height())

        self.etiquetaTitulo = QLabel(' Hotel Perza')
        self.etiquetaTitulo.setStyleSheet("color: #94e7ff;")
        self.etiquetaTitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Establece el tamaño de la fuente a 20 puntos
        font = QFont()
        font.setFamily("Bebas Neue")
        font.setPointSize(30)
        self.etiquetaTitulo.setFont(font)
        self.etiquetaTitulo.setBuddy(self.etiquetaTitulo)

        self.etiqueta_usuario = QLabel()
        self.entrada_usuario = QLineEdit()
        self.entrada_usuario.setPlaceholderText("Usuario")
        self.etiqueta_usuario.setBuddy(self.entrada_usuario)
        # Cargar la imagen IconUser
        pixmap = QPixmap("Images/Icon_user.png")
        scaled_pixmap = pixmap.scaled(30, 30)
        if not pixmap.isNull():
            self.IconUser = QLabel()
            self.IconUser.setPixmap(scaled_pixmap)
            self.IconUser.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.etiqueta_password = QLabel()
        self.entrada_password = QLineEdit()
        self.entrada_password.setPlaceholderText("Contraseña")
        self.entrada_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.etiqueta_password.setBuddy(self.entrada_password)
        # Cargar la imagen Iconpassword
        pixmap = QPixmap("Images/Icon_password.png")
        scaled_pixmap = pixmap.scaled(30, 30)
        if not pixmap.isNull():
            self.IconPassword = QLabel()
            self.IconPassword.setPixmap(scaled_pixmap)
            self.IconPassword.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Mostrar contraseña
        self.check_view_password = QCheckBox()
        self.check_view_password.setText("Ver Contraseña")
        self.check_view_password.toggled.connect(self.mostrar_contrasenia)

        self.boton_login = QPushButton('Iniciar Sesión')
        self.boton_login.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.boton_login.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_login.enterEvent = self.on_enter_button
        self.boton_login.leaveEvent = self.on_leave_button

        self.boton_login.clicked.connect(self.validar_credenciales)

        layout.addWidget(self.etiquetaTitulo)
        layout.addWidget(self.etiqueta_usuario)
        layout.addWidget(self.IconUser)
        layout.addWidget(self.entrada_usuario)
        layout.addWidget(self.etiqueta_password)
        layout.addWidget(self.IconPassword)
        layout.addWidget(self.entrada_password)
        layout.addWidget(self.check_view_password)
        layout.addWidget(self.boton_login)

        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    ventana = VentanaLogin()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
