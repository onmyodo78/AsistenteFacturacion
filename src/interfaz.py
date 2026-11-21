
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

from src.entrada_facturas import verificar_lote_desde_texto


def formato_euros(importe):
    """Muestra un importe con formato español."""
    texto = f"{importe:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


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

    etiqueta_resultado = QLabel(
        "Resultado: pendiente de verificación"
    )
    etiqueta_resultado.setWordWrap(True)

    def limpiar_resultado():
        etiqueta_resultado.setText(
            "Resultado: pendiente de verificación"
        )

    campo_base.textChanged.connect(limpiar_resultado)
    campo_iva.textChanged.connect(limpiar_resultado)
    campo_retencion.textChanged.connect(limpiar_resultado)
    campo_total.textChanged.connect(limpiar_resultado)

    def verificar_datos():
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

            factura = resultado["facturas"][0]

            total_calculado = factura["total_calculado"]
            total_declarado = factura["total_declarado"]
            diferencia = factura["diferencia"]

            if resultado["sin_incidencias"]:
                estado = "CORRECTA"
            else:
                estado = "CON DIFERENCIAS"

            etiqueta_resultado.setText(
                f"Estado: {estado}\n\n"
                f"Total calculado: {formato_euros(total_calculado)} €\n"
                f"Total declarado: {formato_euros(total_declarado)} €\n"
                f"Diferencia: {formato_euros(diferencia)} €"
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
                        "La factura presenta diferencias.\n\n"
                        f"Diferencia: {formato_euros(diferencia)} €\n\n"
                        "Importe positivo: el total declarado es mayor.\n"
                        "Importe negativo: el total declarado es menor."
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
    boton.clicked.connect(verificar_datos)
    distribucion.addWidget(boton)

    distribucion.addWidget(etiqueta_resultado)

    ventana.setLayout(distribucion)
    ventana.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    iniciar_aplicacion()
