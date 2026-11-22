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

def comprobar_desglose_preventivo(base, conceptos):
    """
    Comprueba si la suma de conceptos coincide con la base.

    Devuelve None cuando todavía no hay datos suficientes
    o cuando algún importe no es válido.

    Si los datos son válidos, devuelve la diferencia entre
    la base imponible y la suma de conceptos.
    """
    if not str(base).strip() or not conceptos:
        return None

    try:
        base_decimal = interpretar_importe(base)

        for concepto in conceptos:
            if not str(concepto["importe"]).strip():
                return None

        total_conceptos = sumar_conceptos(conceptos)

    except (ValueError, KeyError, TypeError):
        return None

    return (base_decimal - total_conceptos).quantize(
        Decimal("0.01")
    )