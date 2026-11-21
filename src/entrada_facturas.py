
from src.importes import interpretar_importe



def preparar_factura(datos):
    """
    Valida y convierte los importes introducidos
    por el usuario antes de verificarlos.
    """
    factura = {}

    # Importes obligatorios
    for campo in ("base", "iva", "total"):
        if campo not in datos:
            raise ValueError(
                f"Falta el campo obligatorio: {campo}"
            )

        factura[campo] = interpretar_importe(datos[campo])

    # Retención opcional
    factura["retencion"] = interpretar_importe(
        datos.get("retencion", "0")
    )

    # Porcentajes opcionales, pero validados
    for campo in ("porcentaje_iva", "porcentaje_retencion"):
        if campo in datos:
            factura[campo] = validar_porcentaje(datos[campo])

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


def validar_porcentaje(valor):
    """Valida un porcentaje entre 0 y 100."""
    from decimal import Decimal, InvalidOperation

    texto = str(valor).strip().replace(",", ".")

    try:
        porcentaje = Decimal(texto)
    except InvalidOperation as error:
        raise ValueError(
            f"Porcentaje no válido: {valor!r}"
        ) from error

    if not porcentaje.is_finite():
        raise ValueError("El porcentaje debe ser finito")

    if porcentaje < 0 or porcentaje > 100:
        raise ValueError(
            "El porcentaje debe estar entre 0 y 100"
        )

    return porcentaje
