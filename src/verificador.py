
from decimal import Decimal, ROUND_HALF_UP


def dinero(valor):
    return Decimal(str(valor)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )


def verificar_factura(base, iva, retencion, total):
    base = dinero(base)
    iva = dinero(iva)
    retencion = dinero(retencion)
    total = dinero(total)

    calculado = dinero(base + iva - retencion)
    diferencia = dinero(total - calculado)

    return {
        "total_calculado": calculado,
        "total_declarado": total,
        "diferencia": diferencia,
        "correcta": diferencia == Decimal("0.00")
    }


def verificar_lote(facturas, importe_facilitado):
    resultados = []
    total_facturas = Decimal("0.00")

    for numero, factura in enumerate(facturas, start=1):
        resultado = verificar_factura(
            factura["base"],
            factura["iva"],
            factura.get("retencion", 0),
            factura["total"]
        )

        resultado["numero"] = numero
        resultados.append(resultado)
        total_facturas += dinero(factura["total"])

    total_facturas = dinero(total_facturas)
    facilitado = dinero(importe_facilitado)

    return {
        "facturas": resultados,
        "importe_facilitado": facilitado,
        "total_facturas": total_facturas,
        "diferencia": dinero(facilitado - total_facturas),
        "todas_correctas": all(
            resultado["correcta"] for resultado in resultados
        )
    }
