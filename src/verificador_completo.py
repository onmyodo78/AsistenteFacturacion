
from decimal import Decimal

from src.verificador import verificar_lote
from src.impuestos import verificar_iva, verificar_retencion


def verificar_lote_completo(facturas, importe_facilitado):
    """
    Comprueba importes, IVA y retenciones de un lote.
    Los porcentajes deben venir indicados en los datos.
    """
    resumen = verificar_lote(facturas, importe_facilitado)
    incidencias = []

    for numero, factura in enumerate(facturas, start=1):

        if "porcentaje_iva" in factura:
            resultado_iva = verificar_iva(
                factura["base"],
                factura["porcentaje_iva"],
                factura["iva"]
            )

            if not resultado_iva["correcto"]:
                incidencias.append({
                    "factura": numero,
                    "tipo": "IVA",
                    "diferencia": resultado_iva["diferencia"]
                })

        if "porcentaje_retencion" in factura:
            resultado_retencion = verificar_retencion(
                factura["base"],
                factura["porcentaje_retencion"],
                factura.get("retencion", 0)
            )

            if not resultado_retencion["correcta"]:
                incidencias.append({
                    "factura": numero,
                    "tipo": "RETENCION",
                    "diferencia": resultado_retencion["diferencia"]
                })

        resultado_base = resumen["facturas"][numero - 1]

        if not resultado_base["correcta"]:
            incidencias.append({
                "factura": numero,
                "tipo": "TOTAL",
                "diferencia": resultado_base["diferencia"]
            })

    resumen["incidencias"] = incidencias
    resumen["impuestos_verificados"] = all(
        "porcentaje_iva" in factura for factura in facturas
    )
    resumen["lote_cuadrado"] = (
        resumen["diferencia"] == Decimal("0.00")
    )
    resumen["sin_incidencias"] = (
        len(incidencias) == 0
    )

    return resumen
