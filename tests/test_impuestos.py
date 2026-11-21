
import unittest
from decimal import Decimal

from src.impuestos import (
    calcular_porcentaje,
    verificar_iva,
    verificar_retencion
)


class TestImpuestos(unittest.TestCase):

    def test_iva_21(self):
        resultado = verificar_iva("100", "21", "21")
        self.assertTrue(resultado["correcto"])

    def test_iva_10(self):
        resultado = verificar_iva("100", "10", "10")
        self.assertTrue(resultado["correcto"])

    def test_iva_4(self):
        resultado = verificar_iva("100", "4", "4")
        self.assertTrue(resultado["correcto"])

    def test_iva_incorrecto(self):
        resultado = verificar_iva("100", "21", "19")
        self.assertFalse(resultado["correcto"])
        self.assertEqual(
            resultado["diferencia"], Decimal("-2.00")
        )

    def test_retencion_15(self):
        resultado = verificar_retencion(
            "100", "15", "15"
        )
        self.assertTrue(resultado["correcta"])

    def test_redondeo(self):
        resultado = calcular_porcentaje("10.05", "21")
        self.assertEqual(resultado, Decimal("2.11"))


if __name__ == "__main__":
    unittest.main()
