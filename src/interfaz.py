
import sys


from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFormLayout,
    QMessageBox,
)


def iniciar_aplicacion():
    app = QApplication(sys.argv)

    ventana = QWidget()
    ventana.setWindowTitle(
        "Asistente de Facturación y Verificación Contable"
    )
    ventana.resize(650, 400)

    distribucion = QVBoxLayout()

    titulo = QLabel(
        "Asistente de Facturación y Verificación Contable"
    )
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

    campo_retencion = QLineEdit()
    campo_retencion.setPlaceholderText("Ejemplo: 150,00")
    formulario.addRow("Retención (€):", campo_retencion)

    campo_total = QLineEdit()
    campo_total.setPlaceholderText("Ejemplo: 1.060,00")
    formulario.addRow("Total factura (€):", campo_total)

    distribucion.addLayout(formulario)


    def verificar_datos():
        from src.entrada_facturas import verificar_lote_desde_texto

        datos = {
            "base": campo_base.text(),
            "iva": campo_iva.text(),
            "retencion": campo_retencion.text() or "0",
            "total": campo_total.text(),
        }

        try:
            resultado = verificar_lote_desde_texto(
                [datos],
                campo_total.text()
            )

            if resultado["sin_incidencias"]:
                QMessageBox.information(
                    ventana,
                    "Resultado",
                    "La factura es correcta."
                )


            else:
                diferencia = resultado["facturas"][0]["diferencia"]
                diferencia_es = f"{diferencia:.2f}".replace(".", ",")

                QMessageBox.warning(
                    ventana,
                    "Factura con diferencias",
                    (
                        "La factura presenta diferencias.\n\n"
                        f"Diferencia: {diferencia_es} €\n\n"
                        "Importe positivo: el total declarado es mayor.\n"
                        "Importe negativo: el total declarado es menor."
                    )
                )

        except (ValueError, KeyError) as error:
            QMessageBox.warning(
                ventana,
                "Datos no válidos",
                str(error)
            )

    boton = QPushButton("Verificar factura")
    boton.clicked.connect(verificar_datos)
    distribucion.addWidget(boton)


    ventana.setLayout(distribucion)
    ventana.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    iniciar_aplicacion()
