
import sys

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFormLayout,
    QMessageBox,
    QScrollArea,
)

from src.entrada_facturas import verificar_lote_desde_texto
from src.conceptos import sumar_conceptos
from src.importes import interpretar_importe

def formato_euros(importe):
    """Muestra un importe con formato español."""
    texto = f"{importe:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def iniciar_aplicacion():
    app = QApplication(sys.argv)

    # Área desplazable para facturas con muchos conceptos
    ventana = QWidget()

    area_desplazamiento = QScrollArea()
    area_desplazamiento.setWidgetResizable(True)
    area_desplazamiento.setFrameShape(QScrollArea.Shape.NoFrame)

    contenido = QWidget()

    distribucion = QVBoxLayout()
    distribucion.setAlignment(Qt.AlignmentFlag.AlignTop)
    distribucion.setSpacing(12)
    distribucion.setContentsMargins(20, 20, 20, 20)

    ventana.setWindowTitle(
        "Asistente de Facturación y Verificación Contable"
    )
    ventana.resize(650, 400)

    titulo = QLabel(
        "Asistente de Facturación y Verificación Contable"
    )
    titulo.setStyleSheet("""
        QLabel {
            font-size: 20px;
            font-weight: bold;
            color: #1e3a5f;
            padding-bottom: 8px;
        }
    """)
    distribucion.addWidget(titulo)


    descripcion = QLabel(
        "Verificación de facturas, IVA, retenciones y lotes."
    )
    distribucion.addWidget(descripcion)

    formulario = QFormLayout()

    campo_base = QLineEdit()
    campo_base.setPlaceholderText("Ejemplo: 1.000,00")
    formulario.addRow("Base imponible (€):", campo_base)

    campo_iva = QLineEdit()
    campo_iva.setPlaceholderText("Ejemplo: 210,00")
    formulario.addRow("IVA (€):", campo_iva)


    campo_porcentaje_iva = QLineEdit()
    campo_porcentaje_iva.setPlaceholderText("Ejemplo: 21")
    formulario.addRow("IVA (%):", campo_porcentaje_iva)


    campo_retencion = QLineEdit()
    campo_retencion.setPlaceholderText("Ejemplo: 150,00")
    formulario.addRow("Retención (€):", campo_retencion)

    campo_porcentaje_retencion = QLineEdit()
    campo_porcentaje_retencion.setPlaceholderText("Ejemplo: 15")
    formulario.addRow(
        "Retención (%):",
        campo_porcentaje_retencion
    )

    campo_total = QLineEdit()
    campo_total.setPlaceholderText("Ejemplo: 1.060,00")
    formulario.addRow("Total factura (€):", campo_total)

    distribucion.addLayout(formulario)

    # Sección de conceptos adicionales
    titulo_conceptos = QLabel("Conceptos adicionales")
    titulo_conceptos.setStyleSheet("""
        QLabel {
            font-size: 15px;
            font-weight: bold;
            color: #1e3a5f;
            margin-top: 10px;
        }
    """)
    distribucion.addWidget(titulo_conceptos)

    # Contenedor de las filas de conceptos
    distribucion_conceptos = QVBoxLayout()
    distribucion_conceptos.setSpacing(6)
    distribucion.addLayout(distribucion_conceptos)

    # Filas de conceptos adicionales
    filas_conceptos = []

    def añadir_fila_concepto():
        fila = QHBoxLayout()

        campo_descripcion = QLineEdit()
        campo_descripcion.setPlaceholderText("Descripción del concepto")

        campo_importe = QLineEdit()
        campo_importe.setPlaceholderText("Importe (€)")

        fila.addWidget(campo_descripcion, 3)
        fila.addWidget(campo_importe, 1)

        boton_eliminar = QPushButton("×")
        boton_eliminar.setFixedWidth(32)
        boton_eliminar.setToolTip("Eliminar concepto")
        fila.addWidget(boton_eliminar)

        distribucion_conceptos.addLayout(fila)

        concepto = (campo_descripcion, campo_importe)
        filas_conceptos.append(concepto)

        def eliminar_concepto():
            filas_conceptos.remove(concepto)

            while fila.count():
                elemento = fila.takeAt(0)
                widget = elemento.widget()

                if widget is not None:
                    widget.deleteLater()

            distribucion_conceptos.removeItem(fila)
            fila.deleteLater()

        boton_eliminar.clicked.connect(eliminar_concepto)

    boton_añadir_concepto = QPushButton("+ Añadir concepto")
    boton_añadir_concepto.clicked.connect(añadir_fila_concepto)
    distribucion.addWidget(boton_añadir_concepto)

    etiqueta_resultado = QLabel(
        "Resultado: pendiente de verificación"
    )
    etiqueta_resultado.setWordWrap(True)


    def aplicar_estilo_resultado(color_fondo, color_texto):
        etiqueta_resultado.setStyleSheet(f"""
            QLabel {{
                background-color: {color_fondo};
                color: {color_texto};
                border-radius: 6px;
                padding: 14px;
                font-size: 13px;
            }}
        """)

    aplicar_estilo_resultado("#e9ecef", "#343a40")


    def limpiar_resultado():
        etiqueta_resultado.setText(
            "Resultado: pendiente de verificación"
        )

        aplicar_estilo_resultado("#e9ecef", "#343a40")


    campo_base.textChanged.connect(limpiar_resultado)
    campo_iva.textChanged.connect(limpiar_resultado)
    campo_porcentaje_iva.textChanged.connect(limpiar_resultado)
    campo_retencion.textChanged.connect(limpiar_resultado)
    campo_porcentaje_retencion.textChanged.connect(limpiar_resultado)
    campo_total.textChanged.connect(limpiar_resultado)


    def verificar_datos():
        # Recoger los conceptos introducidos
        conceptos = []

        for campo_descripcion, campo_importe in filas_conceptos:
            descripcion = campo_descripcion.text().strip()
            importe = campo_importe.text().strip()

            if not descripcion and not importe:
                continue

            conceptos.append({
                "descripcion": descripcion,
                "importe": importe,
            })

        datos = {
            "base": campo_base.text(),
            "iva": campo_iva.text(),
            "retencion": campo_retencion.text() or "0",
            "total": campo_total.text(),
        }

        if campo_porcentaje_iva.text().strip():
            datos["porcentaje_iva"] = (
                campo_porcentaje_iva.text().strip()
            )

        if campo_porcentaje_retencion.text().strip():
            datos["porcentaje_retencion"] = (
                campo_porcentaje_retencion.text().strip()
            )


        try:
            # Calcular los conceptos adicionales, si existen
            total_conceptos = None

            if conceptos:
                total_conceptos = sumar_conceptos(conceptos)

            resultado = verificar_lote_desde_texto(
                [datos],
                campo_total.text()
            )

            factura = resultado["facturas"][0]

            total_calculado = factura["total_calculado"]
            total_declarado = factura["total_declarado"]
            diferencia = factura["diferencia"]


            incidencias = resultado["incidencias"]
            detalle_incidencias = ""

            if incidencias:
                detalle_incidencias = "\n\nIncidencias detectadas:"

                for incidencia in incidencias:
                    tipo = incidencia["tipo"]
                    importe = incidencia["diferencia"]

                    detalle_incidencias += (
                        f"\n- {tipo}: {formato_euros(importe)} €"
                    )


            if resultado["sin_incidencias"]:
                estado = "CORRECTA"
                aplicar_estilo_resultado("#d4edda", "#155724")
            else:
                estado = "CON DIFERENCIAS"
                aplicar_estilo_resultado("#f8d7da", "#721c24")


            detalle_conceptos = ""

            if total_conceptos is not None:
                diferencia_conceptos = (
                    interpretar_importe(datos["base"])
                    - total_conceptos
                )

                if diferencia_conceptos == 0:
                    estado_conceptos = "Desglose cuadrado"
                else:
                    estado_conceptos = (
                        "Desglose con diferencia pendiente de justificar"
                    )

                detalle_conceptos = (
                    "\n\nDesglose de conceptos:"
                    f"\nSuma: {formato_euros(total_conceptos)} €"
                    f"\nDiferencia con la base: "
                    f"{formato_euros(diferencia_conceptos)} €"
                    f"\nEstado: {estado_conceptos}"
                )

            etiqueta_resultado.setText(
                f"Estado: {estado}\n\n"
                f"Total calculado: {formato_euros(total_calculado)} €\n"
                f"Total declarado: {formato_euros(total_declarado)} €\n"
                f"Diferencia del total: {formato_euros(diferencia)} €"
                f"{detalle_conceptos}"
                f"{detalle_incidencias}"
            )

            if resultado["sin_incidencias"]:
                QMessageBox.information(
                    ventana,
                    "Resultado",
                    "La factura es correcta."
                )

            else:
                QMessageBox.warning(
                    ventana,
                    "Factura con diferencias",
                    (
                        "La factura presenta incidencias.\n\n"
                        f"Diferencia del total: {formato_euros(diferencia)} €"
                        f"{detalle_incidencias}"
                    )
                )


        except (ValueError, KeyError) as error:
            etiqueta_resultado.setText(
                "Resultado: datos no válidos"
            )
            QMessageBox.warning(
                ventana,
                "Datos no válidos",
                str(error)
            )


    boton = QPushButton("Verificar factura")
    boton.setMinimumHeight(40)
    boton.setStyleSheet("""
        QPushButton {
            background-color: #1e3a5f;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 6px;
            padding: 8px;
        }

        QPushButton:hover {
            background-color: #2c5282;
        }

        QPushButton:pressed {
            background-color: #142b47;
        }
    """)
    boton.clicked.connect(verificar_datos)
    distribucion.addWidget(boton)


    distribucion.addWidget(etiqueta_resultado)

    # Asociar todos los controles al contenido desplazable
    contenido.setLayout(distribucion)

    # Introducir el contenido en el área de desplazamiento
    area_desplazamiento.setWidget(contenido)

    # Distribución principal de la ventana
    distribucion_ventana = QVBoxLayout()
    distribucion_ventana.setContentsMargins(0, 0, 0, 0)
    distribucion_ventana.addWidget(area_desplazamiento)

    ventana.setLayout(distribucion_ventana)
    ventana.resize(650, 550)
    ventana.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    iniciar_aplicacion()
