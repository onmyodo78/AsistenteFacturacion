
import unittest
from decimal import Decimal

from src.verificador_completo import verificar_lote_completo


class TestVerificadorCompleto(unittest.TestCase):

    def test_lote_correcto(self):
        facturas = [
            {
                "base": "100.00",
                "iva": "21.00",
                "porcentaje_iva": "21",
                "retencion": "0.00",
                "total": "121.00"
            }
            for _ in range(10)
        ]

        resultado = verificar_lote_completo(
            facturas, "1210.00"
        )

        self.assertTrue(resultado["lote_cuadrado"])
        self.assertTrue(resultado["sin_incidencias"])
        self.assertTrue(resultado["impuestos_verificados"])

    def test_iva_incorrecto(self):
        facturas = [{
            "base": "100.00",
            "iva": "19.00",
            "porcentaje_iva": "21",
            "retencion": "0.00",
            "total": "119.00"
        }]

        resultado = verificar_lote_completo(
            facturas, "119.00"
        )

        self.assertTrue(resultado["lote_cuadrado"])
        self.assertFalse(resultado["sin_incidencias"])
        self.assertEqual(
            resultado["incidencias"][0]["tipo"], "IVA"
        )

    def test_diferencia_dinero_facilitado(self):
        facturas = [{
            "base": "100.00",
            "iva": "21.00",
            "porcentaje_iva": "21",
            "retencion": "0.00",
            "total": "121.00"
        }]

        resultado = verificar_lote_completo(
            facturas, "150.00"
        )

        self.assertFalse(resultado["lote_cuadrado"])
        self.assertEqual(
            resultado["diferencia"], Decimal("29.00")
        )


if __name__ == "__main__":
    unittest.main()
