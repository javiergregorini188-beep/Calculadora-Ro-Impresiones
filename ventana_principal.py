import os
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit,
    QComboBox, QCheckBox, QPushButton,
    QVBoxLayout, QFormLayout, QMessageBox,
    QDialog, QGridLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon

from models.calculadora import (
    calcular_trabajo,
    calcular_anillado_dividido
)


# =========================================
# VENTANA MODAL PARA DIVIDIR EN TOMOS
# =========================================
class VentanaDivisionTomos(QDialog):
    def __init__(self, hojas_totales, opciones_division):
        super().__init__()

        self.setWindowTitle("Dividir Anillado en Tomos")
        self.setModal(True)
        self.resize(400, 300)

        self.tomos_seleccionado = None

        layout_principal = QVBoxLayout()

        label_info = QLabel(
            f"El total de {hojas_totales} hojas excede el límite de anillado (500).\n\n"
            "Seleccione en cuántos tomos dividir:"
        )
        label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_info.setWordWrap(True)
        layout_principal.addWidget(label_info)

        grid = QGridLayout()
        self.botones = {}

        fila = 0
        col = 0

        for tomos in range(2, 7):
            texto_boton = f"{tomos} Tomos"

            boton = QPushButton(texto_boton)
            boton.setFixedSize(100, 60)

            if not opciones_division.get(tomos, False):
                boton.setEnabled(False)

            boton.clicked.connect(lambda checked, t=tomos: self.seleccionar_tomos(t))
            grid.addWidget(boton, fila, col)

            self.botones[tomos] = boton

            col += 1
            if col > 2:
                col = 0
                fila += 1

        layout_principal.addLayout(grid)

        layout_botones = QHBoxLayout()

        self.boton_confirmar = QPushButton("Confirmar")
        self.boton_confirmar.setEnabled(False)
        self.boton_confirmar.clicked.connect(self.accept)

        boton_cancelar = QPushButton("Cancelar")
        boton_cancelar.clicked.connect(self.reject)

        layout_botones.addWidget(self.boton_confirmar)
        layout_botones.addWidget(boton_cancelar)

        layout_principal.addLayout(layout_botones)

        self.setLayout(layout_principal)

    def seleccionar_tomos(self, tomos):
        self.tomos_seleccionado = tomos

        for boton in self.botones.values():
            boton.setStyleSheet("")

        self.botones[tomos].setStyleSheet("background-color: lightblue;")
        self.boton_confirmar.setEnabled(True)


# =========================================
# VENTANA PRINCIPAL (SIN BASE DE DATOS)
# =========================================
class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculadora de Impresión")
        
        # Configuración del Logo
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_logo = os.path.join(base_dir, "assets", "1.png")
        self.setWindowIcon(QIcon(ruta_logo))

        layout_principal = QVBoxLayout()
        
        # Mostrar Logo en la ventana
        label_logo = QLabel()
        pixmap = QPixmap(ruta_logo)
        print(f"Ruta del logo: {ruta_logo}") # DEBUG
        print(f"¿Pixmap es nulo? {pixmap.isNull()}") # DEBUG

        if not pixmap.isNull():
            pixmap = pixmap.scaledToHeight(120, Qt.TransformationMode.SmoothTransformation)
            label_logo.setPixmap(pixmap)
            label_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout_principal.addWidget(label_logo)

        formulario = QFormLayout()

        self.input_paginas = QLineEdit()
        formulario.addRow("Cantidad de páginas:", self.input_paginas)

        self.combo_color = QComboBox()
        self.combo_color.addItems(["bn", "color"])
        formulario.addRow("Tipo de color:", self.combo_color)

        self.combo_faz = QComboBox()
        self.combo_faz.addItems(["simple", "doble"])
        formulario.addRow("Tipo de faz:", self.combo_faz)

        self.check_anillado = QCheckBox("Lleva anillado")
        formulario.addRow(self.check_anillado)

        self.boton_calcular = QPushButton("Calcular")
        self.boton_calcular.clicked.connect(self.calcular)

        self.label_resultado = QLabel("Resultado aparecerá aquí")
        self.label_resultado.setWordWrap(True)

        layout_principal.addLayout(formulario)
        layout_principal.addWidget(self.boton_calcular)
        layout_principal.addWidget(self.label_resultado)

        self.setLayout(layout_principal)

    def calcular(self):
        try:
            paginas = int(self.input_paginas.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Ingrese un número válido de páginas.")
            return

        tipo_color = self.combo_color.currentText()
        tipo_faz = self.combo_faz.currentText()
        lleva_anillado = self.check_anillado.isChecked()

        resultado = calcular_trabajo(
            paginas,
            tipo_color,
            tipo_faz,
            lleva_anillado
        )

        # CASO FUERA DE RANGO
        if resultado["fuera_de_rango"]:

            dialogo = VentanaDivisionTomos(
                resultado["hojas"],
                resultado["opciones_division"]
            )

            if dialogo.exec():
                tomos = dialogo.tomos_seleccionado

                division = calcular_anillado_dividido(
                    resultado["hojas"],
                    tomos
                )

                if division:
                    precio_anillado = division["total_anillado"]
                    total_final = resultado["precio_impresion"] + precio_anillado

                    texto = (
                        f"Hojas físicas: {resultado['hojas']}\n"
                        f"Dividido en {tomos} tomos\n"
                        f"Hojas por tomo: {division['hojas_por_tomo']}\n"
                        f"Precio impresión: ${resultado['precio_impresion']}\n"
                        f"Precio anillado: ${precio_anillado}\n"
                        f"Total: ${total_final}"
                    )

                    self.label_resultado.setText(texto)

            return

        # CASO NORMAL
        texto = (
            f"Hojas físicas: {resultado['hojas']}\n"
            f"Precio impresión: ${resultado['precio_impresion']}\n"
            f"Precio anillado: ${resultado['precio_anillado']}\n"
            f"Total: ${resultado['total']}"
        )

        self.label_resultado.setText(texto)