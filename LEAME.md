# AsistenteFacturacion

**Herramienta de apoyo para comprobar importes y detectar diferencias en facturas.**

## 1. ¿Para qué sirve?

AsistenteFacturacion permite introducir manualmente importes de una factura y comprobar si las operaciones matemáticas cuadran.

Está pensado para pequeñas empresas y personas que necesitan revisar cantidades de forma rápida, sin utilizar un programa completo de contabilidad.

Puede ayudar a:

- Comprobar que el IVA corresponde al porcentaje indicado.
- Revisar importes de retenciones.
- Comprobar que el total de una factura coincide con sus cantidades.
- Sumar conceptos adicionales y compararlos con la base imponible.
- Detectar posibles diferencias antes de dar por revisada una factura.

## 2. Cómo utilizarlo

1. Abre AsistenteFacturacion.
2. Introduce la base imponible de la factura.
3. Escribe el importe del IVA y su porcentaje, si corresponde.
4. Introduce la retención y su porcentaje, si corresponde.
5. Escribe el importe total de la factura.
6. Si necesitas desglosar conceptos, pulsa **+ Añadir concepto** e introduce sus importes.
7. Observa los avisos preventivos que aparecen mientras escribes.
8. Pulsa **Verificar factura** para realizar la comprobación.

Los campos opcionales pueden dejarse vacíos cuando no correspondan.

### Ejemplo sencillo

Una factura contiene:

| Concepto       |  Importe |
| -------------- | -------: |
| Base imponible | 100,00 € |
| IVA (21 %)     |  21,00 € |
| Retención      |   0,00 € |
| Total          | 121,00 € |

Los importes cuadran matemáticamente.

Si el total introducido fuera 125,00 €, la aplicación podría señalar una diferencia de 4,00 €.

## 3. Qué significan los colores

- **Gris:** pendiente de verificación.
- **Amarillo:** aviso preventivo. Se ha detectado una posible diferencia mientras se introducen los datos.
- **Verde:** la verificación realizada no ha detectado diferencias.
- **Rojo:** la verificación ha detectado diferencias que conviene revisar.

Los avisos amarillos son provisionales y pueden cambiar mientras se modifican los importes.

## 4. QUE NO HACE AsistenteFacturacion

Esta aplicación no sustituye un programa de contabilidad ni el trabajo de una persona responsable de la gestión contable o fiscal.

No comprueba automáticamente:

- Si una factura es auténtica.
- Si se ha aplicado el impuesto legalmente adecuado.
- Si un cliente ha pagado realmente.
- Si el dinero físico de una caja coincide con los movimientos registrados.
- Si una factura cumple todos los requisitos fiscales.

**Que una operación cuadre matemáticamente no garantiza que sea correcta desde el punto de vista contable, fiscal o documental.**

## 5. Uso en Windows

La aplicación se distribuye mediante el archivo `AsistenteFacturacion-Windows.zip`.

Para utilizarla:

1. Descarga el ZIP correspondiente a la versión facilitada.
2. Extrae todo su contenido en una carpeta del ordenador.
3. Abre la carpeta `AsistenteFacturacion`.
4. Haz doble clic en `AsistenteFacturacion.exe`.

***Es importante no separar el ejecutable de la carpeta `_internal`.***

La versión empaquetada incluye las dependencias necesarias para ejecutarse, por lo que no es necesario instalar Python por separado.

## 6. Uso desde el código fuente en Linux

Esta modalidad está destinada principalmente a quien desarrolla o mantiene el programa.

Requiere Python y PySide6 instalados en un entorno adecuado.

Desde la carpeta principal del proyecto, con el entorno virtual preparado y activado, ejecuta:

`python3 -m src.interfaz`

## 7. Privacidad

AsistenteFacturacion realiza las comprobaciones localmente en el ordenador.

No necesita subir facturas a servidores externos para realizar sus cálculos.

La versión actual está orientada a introducir y comprobar datos manualmente, sin lectura automática de documentos.

## 8. Recomendación de uso

Utiliza AsistenteFacturacion como una segunda comprobación de los números.

Si aparece una diferencia, revisa los importes originales antes de corregir la factura o realizar cualquier ajuste contable.

El objetivo es **facilitar las comprobaciones cotidianas, no sustituir los procedimientos de la empresa**.
