
import unittest
from decimal import Decimal

from src.verificador import verificar_factura, verificar_lote


class TestVerificador(unittest.TestCase):

    def test_factura_correcta(self):
        resultado = verificar_factura(
            "100.00", "21.00", "0.00", "121.00"
        )
        self.assertTrue(resultado["correcta"])

    def test_factura_incorrecta(self):
        resultado = verificar_factura(
            "100.00", "21.00", "0.00", "120.00"
        )
        self.assertFalse(resultado["correcta"])
        self.assertEqual(
            resultado["diferencia"], Decimal("-1.00")
        )

    def test_lote_1950_euros(self):
        facturas = [
            {
                "base": "100.00",
                "iva": "21.00",
                "retencion": "0.00",
                "total": "121.00"
            }
            for _ in range(10)
        ]

        resultado = verificar_lote(facturas, "1950.00")

        self.assertEqual(
            resultado["total_facturas"], Decimal("1210.00")
        )
        self.assertEqual(
            resultado["diferencia"], Decimal("740.00")
        )
        self.assertTrue(resultado["todas_correctas"])


if __name__ == "__main__":
    unittest.main()
