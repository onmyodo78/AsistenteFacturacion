
import re
from decimal import Decimal, InvalidOperation


def interpretar_importe(valor):
    """Convierte importes válidos a Decimal."""

    if isinstance(valor, bool):
        raise ValueError("El importe no puede ser un booleano")

    if isinstance(valor, Decimal):
        if not valor.is_finite():
            raise ValueError("El importe debe ser finito")
        return valor

    texto = str(valor).strip()
    texto = texto.replace("€", "").replace(" ", "")
    texto = texto.replace("\u00a0", "").replace("\u202f", "")

    # Formato español con miles: 1.950,50
    patron_espanol_miles = r"-?\d{1,3}(\.\d{3})+,\d{1,2}"

    # Formato español sin miles: 1950,50
    patron_espanol_simple = r"-?\d+,\d{1,2}"

    # Formato decimal con punto: 1950.00
    patron_decimal_punto = r"-?\d+\.\d{2}"

    # Números enteros: 1950
    patron_entero = r"-?\d+"

    if re.fullmatch(patron_espanol_miles, texto):
        texto = texto.replace(".", "").replace(",", ".")

    elif re.fullmatch(patron_espanol_simple, texto):
        texto = texto.replace(",", ".")

    elif re.fullmatch(patron_decimal_punto, texto):
        pass

    elif re.fullmatch(patron_entero, texto):
        pass

    else:
        raise ValueError(
            f"Formato de importe no válido o ambiguo: {valor!r}"
        )

    try:
        importe = Decimal(texto)
    except InvalidOperation as error:
        raise ValueError(
            f"Importe no válido: {valor!r}"
        ) from error

    if not importe.is_finite():
        raise ValueError("El importe debe ser finito")

    return importe
