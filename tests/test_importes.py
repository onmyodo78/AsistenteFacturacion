
import unittest
from decimal import Decimal

from src.importes import interpretar_importe


class TestImportes(unittest.TestCase):

    def test_formato_decimal(self):
        resultado = interpretar_importe("1950.00")
        self.assertEqual(resultado, Decimal("1950.00"))

    def test_coma_decimal(self):
        resultado = interpretar_importe("1950,00")
        self.assertEqual(resultado, Decimal("1950.00"))

    def test_formato_espanol(self):
        resultado = interpretar_importe("1.950,00")
        self.assertEqual(resultado, Decimal("1950.00"))

    def test_simbolo_euro(self):
        resultado = interpretar_importe("1.950,50 €")
        self.assertEqual(resultado, Decimal("1950.50"))

    def test_importe_negativo(self):
        resultado = interpretar_importe("-125,50")
        self.assertEqual(resultado, Decimal("-125.50"))

    def test_texto_invalido(self):
        with self.assertRaises(ValueError):
            interpretar_importe("mil euros")

    def test_importe_vacio(self):
        with self.assertRaises(ValueError):
            interpretar_importe("")

    def test_valor_infinito(self):
        with self.assertRaises(ValueError):
            interpretar_importe("Infinity")

    def test_booleano(self):
        with self.assertRaises(ValueError):
            interpretar_importe(True)


    def test_separadores_mal_colocados(self):
        valores_invalidos = [
            "1.95,0",
            "1,2,3",
            "1.23.456,78",
            "12.34",
        ]

        for valor in valores_invalidos:
            with self.subTest(valor=valor):
                with self.assertRaises(ValueError):
                    interpretar_importe(valor)

if __name__ == "__main__":
    unittest.main()
