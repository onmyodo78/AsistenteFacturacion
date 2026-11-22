
import unittest
from decimal import Decimal

from src.avisos_preventivos import generar_avisos_preventivos


class TestAvisosPreventivos(unittest.TestCase):

    def test_factura_correcta_sin_avisos(self):
        datos = {
            "base": "100",
            "iva": "21",
            "porcentaje_iva": "21",
            "total": "121",
        }

        self.assertEqual(generar_avisos_preventivos(datos), [])

    def test_iva_incorrecto(self):
        datos = {
            "base": "100",
            "iva": "25",
            "porcentaje_iva": "21",
            "total": "125",
        }

        avisos = generar_avisos_preventivos(datos)

        self.assertEqual(len(avisos), 1)
        self.assertEqual(avisos[0]["tipo"], "iva")
        self.assertEqual(avisos[0]["diferencia"], Decimal("4.00"))

    def test_iva_y_total_incorrectos(self):
        datos = {
            "base": "100",
            "iva": "25",
            "porcentaje_iva": "21",
            "total": "130",
        }

        avisos = generar_avisos_preventivos(datos)

        self.assertEqual(
            [aviso["tipo"] for aviso in avisos],
            ["iva", "total"]
        )

    def test_retencion_incorrecta(self):
        datos = {
            "base": "100",
            "retencion": "10",
            "porcentaje_retencion": "15",
        }

        avisos = generar_avisos_preventivos(datos)

        self.assertEqual(len(avisos), 1)
        self.assertEqual(avisos[0]["tipo"], "retencion")
        self.assertEqual(avisos[0]["diferencia"], Decimal("-5.00"))

    def test_conceptos_con_diferencia(self):
        datos = {"base": "100"}

        conceptos = [
            {"descripcion": "Servicio", "importe": "80"},
            {"descripcion": "Material", "importe": "19,50"},
        ]

        avisos = generar_avisos_preventivos(datos, conceptos)

        self.assertEqual(len(avisos), 1)
        self.assertEqual(avisos[0]["tipo"], "conceptos")
        self.assertEqual(avisos[0]["diferencia"], Decimal("0.50"))

    def test_datos_incompletos(self):
        datos = {
            "base": "100",
            "iva": "",
            "total": "",
        }

        self.assertEqual(generar_avisos_preventivos(datos), [])


    def test_retencion_invalida_no_genera_aviso_total(self):
        datos = {
            "base": "100",
            "iva": "21",
            "retencion": "abc",
            "total": "120",
        }

        avisos = generar_avisos_preventivos(datos)

        self.assertEqual(avisos, [])


if __name__ == "__main__":
    unittest.main()
