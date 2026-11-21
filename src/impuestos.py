
from decimal import Decimal, ROUND_HALF_UP


def calcular_porcentaje(base, porcentaje):
    """Calcula un porcentaje utilizando importes decimales."""
    base = Decimal(str(base))
    porcentaje = Decimal(str(porcentaje))

    resultado = base * porcentaje / Decimal("100")

    return resultado.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )


def verificar_iva(base, porcentaje, iva_declarado):
    """Comprueba si la cuota de IVA coincide con el porcentaje."""
    iva_calculado = calcular_porcentaje(base, porcentaje)

    iva_declarado = Decimal(str(iva_declarado)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

    diferencia = iva_declarado - iva_calculado

    return {
        "iva_calculado": iva_calculado,
        "iva_declarado": iva_declarado,
        "diferencia": diferencia,
        "correcto": diferencia == Decimal("0.00")
    }


def verificar_retencion(base, porcentaje, retencion_declarada):
    """Comprueba matemáticamente una retención indicada."""
    retencion_calculada = calcular_porcentaje(base, porcentaje)

    retencion_declarada = Decimal(
        str(retencion_declarada)
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

    diferencia = retencion_declarada - retencion_calculada

    return {
        "retencion_calculada": retencion_calculada,
        "retencion_declarada": retencion_declarada,
        "diferencia": diferencia,
        "correcta": diferencia == Decimal("0.00")
    }
