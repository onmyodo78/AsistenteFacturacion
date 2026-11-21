
from src.importes import interpretar_importe


def preparar_factura(datos):
    """
    Valida y convierte los importes introducidos
    por el usuario antes de verificarlos.
    """
    factura = {}

    for campo in ("base", "iva", "total"):
        if campo not in datos:
            raise ValueError(
                f"Falta el campo obligatorio: {campo}"
            )

        factura[campo] = interpretar_importe(
            datos[campo]
        )

    factura["retencion"] = interpretar_importe(
        datos.get("retencion", "0")
    )

    for campo in (
        "porcentaje_iva",
        "porcentaje_retencion"
    ):
        if campo in datos:
            factura[campo] = datos[campo]

    return factura


def verificar_lote_desde_texto(facturas, importe_facilitado):
    """
    Prepara las facturas y comprueba el lote.
    """
    from src.verificador_completo import verificar_lote_completo

    facturas_preparadas = [
        preparar_factura(factura)
        for factura in facturas
    ]

    importe_preparado = interpretar_importe(
        importe_facilitado
    )

    return verificar_lote_completo(
        facturas_preparadas,
        importe_preparado
    )
