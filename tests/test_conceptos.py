import unittest
from decimal import Decimal

from src.conceptos import sumar_conceptos


class TestConceptos(unittest.TestCase):

    def test_factura_gas_con_descuentos(self):
        conceptos = [
            {"descripcion": "Consumo 1", "importe": "8,94"},
            {"descripcion": "Consumo 2", "importe": "4,74"},
            {"descripcion": "Disponibilidad 1", "importe": "14,60"},
            {"descripcion": "Disponibilidad 2", "importe": "6,67"},
            {"descripcion": "Descuento 1", "importe": "-1,33"},
            {"descripcion": "Descuento 2", "importe": "-2,92"},
            {"descripcion": "Alquiler", "importe": "1,22"},
        ]

        resultado = sumar_conceptos(conceptos)

        self.assertEqual(resultado, Decimal("31.92"))

    def test_sin_conceptos(self):
        self.assertEqual(
            sumar_conceptos([]),
            Decimal("0.00")
        )

    def test_importe_no_valido(self):
        conceptos = [
            {"descripcion": "Consumo", "importe": "abc"}
        ]

        with self.assertRaises(ValueError):
            sumar_conceptos(conceptos)


if __name__ == "__main__":
    unittest.main()
