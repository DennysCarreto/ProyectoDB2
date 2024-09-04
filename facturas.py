import sys
import os
import mysql.connector
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget, \
    QTableWidgetItem, QDateEdit, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.units import inch


class VentasFacturas(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Módulo de Ventas/Facturas")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Conectar a la base de datos y obtener los nombres de los clientes
        self.clientes = self.cargar_clientes()

        # Campos de entrada
        self.id_factura_label = QLabel("ID Factura:")
        self.id_factura_input = QLineEdit()
        self.id_factura_input.setValidator(QIntValidator(0, 1000000))

        self.cliente_label = QLabel("Cliente:")
        self.cliente_combo = QComboBox()
        self.cliente_combo.addItems([f"{cliente[1]} {cliente[2]}" for cliente in self.clientes])
        self.cliente_combo.currentIndexChanged.connect(self.cargar_datos_cliente)

        self.direccion_label = QLabel("Dirección:")
        self.direccion_input = QLineEdit()
        self.direccion_input.setReadOnly(True)

        self.telefono_label = QLabel("Teléfono:")
        self.telefono_input = QLineEdit()
        self.telefono_input.setReadOnly(True)

        self.fecha_label = QLabel("Fecha:")
        self.fecha_input = QDateEdit()
        self.fecha_input.setCalendarPopup(True)
        self.fecha_input.setDate(datetime.now().date())

        self.tipo_pago_label = QLabel("Tipo de Pago:")
        self.tipo_pago_combo = QComboBox()
        self.tipo_pago_combo.addItems(["Efectivo", "Tarjeta"])

        self.total_label = QLabel("Total a Pagar:")
        self.total_input = QLineEdit()
        self.total_input.setValidator(QIntValidator(0, 1000000))

        # Tabla para detalles del consumo
        self.detalle_label = QLabel("Detalle del Consumo:")
        self.detalle_table = QTableWidget()
        self.detalle_table.setColumnCount(2)
        self.detalle_table.setHorizontalHeaderLabels(["Descripción", "Monto"])
        self.detalle_table.setRowCount(5)

        # Botón para generar factura
        self.generar_factura_btn = QPushButton("Generar Factura")
        self.generar_factura_btn.clicked.connect(self.generar_factura)

        # Botón para imprimir factura
        self.imprimir_factura_btn = QPushButton("Imprimir Factura")
        self.imprimir_factura_btn.clicked.connect(self.imprimir_factura)

        # Añadir widgets al layout
        layout.addWidget(self.id_factura_label)
        layout.addWidget(self.id_factura_input)
        layout.addWidget(self.cliente_label)
        layout.addWidget(self.cliente_combo)
        layout.addWidget(self.direccion_label)
        layout.addWidget(self.direccion_input)
        layout.addWidget(self.telefono_label)
        layout.addWidget(self.telefono_input)
        layout.addWidget(self.fecha_label)
        layout.addWidget(self.fecha_input)
        layout.addWidget(self.tipo_pago_label)
        layout.addWidget(self.tipo_pago_combo)
        layout.addWidget(self.total_label)
        layout.addWidget(self.total_input)
        layout.addWidget(self.detalle_label)
        layout.addWidget(self.detalle_table)
        layout.addWidget(self.generar_factura_btn)
        layout.addWidget(self.imprimir_factura_btn)

        self.setLayout(layout)

    def cargar_clientes(self):
        try:
            connection = mysql.connector.connect(
                host='192.168.204.253',
                database='hotel_perza',
                user='Denys',
                password='admin'
            )

            cursor = connection.cursor()
            cursor.execute("SELECT id_cliente, nombre, apellido, direccion, telefono FROM clientes")
            clientes = cursor.fetchall()

            cursor.close()
            connection.close()

            return clientes

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error", f"Error al cargar los clientes: {err}")
            return []

    def cargar_datos_cliente(self, index):
        try:
            if index >= 0 and index < len(self.clientes):
                cliente = self.clientes[index]
                self.direccion_input.setText(str(cliente[3]))  # Convertir a cadena si es necesario
                self.telefono_input.setText(str(cliente[4]))  # Convertir a cadena si es necesario
            else:
                self.direccion_input.clear()
                self.telefono_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los datos del cliente: {e}")
            print(e)

    def generar_factura(self):
        id_factura = self.id_factura_input.text()
        cliente = self.cliente_combo.currentText().replace(" ", "_")
        fecha = self.fecha_input.date().toString(Qt.DateFormat.ISODate)
        tipo_pago = self.tipo_pago_combo.currentText()
        total = self.total_input.text()

        # Consolidar detalles del consumo en una lista
        detalles = []
        for row in range(self.detalle_table.rowCount()):
            descripcion = self.detalle_table.item(row, 0)
            monto = self.detalle_table.item(row, 1)
            if descripcion and monto:
                detalles.append([descripcion.text(), monto.text()])

        # Guardar en la base de datos
        self.guardar_factura_en_db(id_factura, fecha, tipo_pago, total, detalles)

        # Ruta del directorio Facturas
        if not os.path.exists("Facturas"):
            os.makedirs("Facturas")

        # Nombre del archivo PDF
        file_name = f"Factura_{cliente}_{fecha}.pdf"
        file_path = os.path.join("Facturas", file_name)

        # Crear PDF
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Título de la factura
        title = Paragraph("Factura", styles['Title'])
        elements.append(title)
        elements.append(Paragraph("<br/>", styles['Normal']))

        # Información del cliente y la factura
        info_table_data = [
            ["ID Factura:", id_factura],
            ["Cliente:", cliente],
            ["Fecha:", fecha],
            ["Tipo de Pago:", tipo_pago],
            ["Total a Pagar:", total]
        ]
        info_table = Table(info_table_data, hAlign='LEFT')
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(info_table)
        elements.append(Paragraph("<br/><br/>", styles['Normal']))

        # Detalles del consumo
        detalles_table_data = [["Descripción", "Monto"]] + detalles
        detalles_table = Table(detalles_table_data, hAlign='LEFT')
        detalles_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(detalles_table)
        elements.append(Paragraph("<br/><br/>", styles['Normal']))

        # Pie de página
        footer = Paragraph("Gracias por su compra. Por favor, conserve esta factura para futuras referencias.",
                           styles['Normal'])
        elements.append(footer)

        # Construir PDF
        doc.build(elements)

        QMessageBox.information(self, "Factura Generada", f"La factura ha sido generada y guardada en {file_path}")
    def guardar_factura_en_db(self, id_factura, fecha, tipo_pago, total, detalles):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='hotel_perza',
                user='root',
                password=''
            )

            cursor = connection.cursor()
            query = ("INSERT INTO facturas (id_factura, fecha, tipo_pago, total_pagar, detalles) "
                     "VALUES (%s, %s, %s, %s, %s)")
            data = (id_factura, fecha, tipo_pago, total, detalles)
            cursor.execute(query, data)
            connection.commit()

            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error", f"Error al guardar en la base de datos: {err}")

    def imprimir_factura(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)

        if dialog.exec():
            file_path = QFileDialog.getOpenFileName(self, "Seleccionar Factura", "", "PDF Files (*.pdf)")[0]
            if file_path:
                self.imprimir_pdf(file_path, printer)

    def imprimir_pdf(self, file_path, printer):
        # Implementar la lógica de impresión del PDF
        printer.setDocName(file_path)
        printer.setOutputFileName(file_path)
        QMessageBox.information(self, "Impresión", "La impresión de la factura ha sido enviada a la impresora")


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = VentasFacturas()
#     window.show()
#     sys.exit(app.exec())
