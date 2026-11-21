
import unittest
from decimal import Decimal

from src.entrada_facturas import preparar_factura


class TestEntradaFacturas(unittest.TestCase):

    def test_factura_española(self):
        datos = {
            "base": "1.000,00 €",
            "iva": "210,00 €",
            "retencion": "150,00 €",
            "total": "1.060,00 €"
        }

        factura = preparar_factura(datos)

        self.assertEqual(
            factura["base"], Decimal("1000.00")
        )
        self.assertEqual(
            factura["total"], Decimal("1060.00")
        )

    def test_importe_ambiguo(self):
        datos = {
            "base": "1.000",
            "iva": "2,59",
            "total": "14,93"
        }

        with self.assertRaises(ValueError):
            preparar_factura(datos)

    def test_falta_total(self):
        datos = {
            "base": "100,00",
            "iva": "21,00"
        }

        with self.assertRaises(ValueError):
            preparar_factura(datos)

    def test_retencion_opcional(self):
        datos = {
            "base": "100,00",
            "iva": "21,00",
            "total": "121,00"
        }

        factura = preparar_factura(datos)

        self.assertEqual(
            factura["retencion"], Decimal("0")
        )


    def test_lote_completo_desde_texto(self):
        from src.entrada_facturas import verificar_lote_desde_texto

        facturas = [
            {
                "base": "1.000,00 €",
                "iva": "210,00 €",
                "porcentaje_iva": "21",
                "retencion": "150,00 €",
                "porcentaje_retencion": "15",
                "total": "1.060,00 €"
            }
        ]

        resultado = verificar_lote_desde_texto(
            facturas,
            "1.060,00 €"
        )

        self.assertTrue(resultado["lote_cuadrado"])
        self.assertTrue(resultado["sin_incidencias"])
        self.assertTrue(resultado["impuestos_verificados"])

        self.assertEqual(
            resultado["total_facturas"],
            Decimal("1060.00")
        )


    def test_porcentajes_validos(self):
        datos = {
            "base": "1000",
            "iva": "210",
            "retencion": "150",
            "total": "1060",
            "porcentaje_iva": "21",
            "porcentaje_retencion": "15",
        }

        factura = preparar_factura(datos)

        self.assertEqual(
            factura["porcentaje_iva"],
            Decimal("21")
        )
        self.assertEqual(
            factura["porcentaje_retencion"],
            Decimal("15")
        )

    def test_porcentajes_invalidos(self):
        for porcentaje in ("abc", "-21", "150", "NaN"):
            datos = {
                "base": "1000",
                "iva": "210",
                "total": "1210",
                "porcentaje_iva": porcentaje,
            }

            with self.subTest(porcentaje=porcentaje):
                with self.assertRaises(ValueError):
                    preparar_factura(datos)

if __name__ == "__main__":
    unittest.main()
