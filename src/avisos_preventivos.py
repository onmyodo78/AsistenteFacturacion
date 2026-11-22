
from src.importes import interpretar_importe
from src.impuestos import verificar_iva, verificar_retencion
from src.verificador import verificar_factura
from src.conceptos import comprobar_desglose_preventivo


def generar_avisos_preventivos(datos, conceptos=None):
    """
    Genera avisos matemáticos provisionales.

    Solo comprueba los apartados que tienen datos suficientes
    y válidos. No determina si una factura es correcta.
    """
    avisos = []
    conceptos = conceptos if conceptos is not None else []

    def importe(campo):
        texto = str(datos.get(campo, "")).strip()
        if not texto:
            return None
        try:
            return interpretar_importe(texto)
        except (ValueError, TypeError):
            return None

    base = importe("base")
    iva = importe("iva")
    retencion = importe("retencion")
    total = importe("total")

    # Comprobación de IVA
    porcentaje_iva = importe("porcentaje_iva")

    if (
        base is not None
        and iva is not None
        and porcentaje_iva is not None
    ):
        resultado = verificar_iva(base, porcentaje_iva, iva)

        if not resultado["correcto"]:
            avisos.append({
                "tipo": "iva",
                "diferencia": resultado["diferencia"],
                "mensaje": "El IVA no coincide con el porcentaje indicado."
            })

    # Comprobación de retención
    porcentaje_retencion = importe("porcentaje_retencion")

    if (
        base is not None
        and retencion is not None
        and porcentaje_retencion is not None
    ):
        resultado = verificar_retencion(
            base, porcentaje_retencion, retencion
        )

        if not resultado["correcta"]:
            avisos.append({
                "tipo": "retencion",
                "diferencia": resultado["diferencia"],
                "mensaje": "La retención no coincide con el porcentaje indicado."
            })

    # Comprobación del total
    texto_retencion = str(datos.get("retencion", "")).strip()
    retencion_valida = not texto_retencion or retencion is not None

    if (
        base is not None
        and iva is not None
        and total is not None
        and retencion_valida
    ):
        resultado = verificar_factura(
            base,
            iva,
            retencion if retencion is not None else 0,
            total
        )

        if not resultado["correcta"]:
            avisos.append({
                "tipo": "total",
                "diferencia": resultado["diferencia"],
                "mensaje": "El total no coincide con los importes indicados."
            })

    # Comprobación del desglose
    if base is not None and conceptos:
        diferencia = comprobar_desglose_preventivo(base, conceptos)

        if diferencia is not None and diferencia != 0:
            avisos.append({
                "tipo": "conceptos",
                "diferencia": diferencia,
                "mensaje": "El desglose no coincide con la base imponible."
            })

    return avisos
