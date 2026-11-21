from decimal import Decimal

from src.importes import interpretar_importe


def sumar_conceptos(conceptos):
    """
    Suma los importes de una lista de conceptos.

    Cada concepto contiene una descripción y un importe.
    Los importes negativos representan descuentos.
    """
    total = Decimal("0.00")

    for concepto in conceptos:
        importe = interpretar_importe(concepto["importe"])
        total += importe

    return total.quantize(Decimal("0.01"))
