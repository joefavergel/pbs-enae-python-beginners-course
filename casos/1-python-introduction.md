## Caso práctico 1: "Introducción a Python"

<div class="remark">
<b>Caso práctico 1 de 6 — Introducción a Python</b><br>
<b>Ponderación:</b> 10% de la nota final (acumulativo 60%).<br>
<b>Modalidad:</b> individual o grupal, según indique el profesor.<br>
<b>Fecha límite de entrega:</b> lunes 12/10/2026.<br>
<b>Entrega:</b> suba su notebook (<code>.ipynb</code>) resuelto <b>únicamente a través de la Plataforma PBS</b>. No se reciben entregas por correo electrónico.
</div><br>

1. Sean A, B y C tres variables enteras que representan las ventas de tres productos respectivamente. Escriba expresiones lógicas (booleanas) que representen las siguientes afirmaciones:
    - El producto A es el más vendido.
    - El mínimo de número de unidades vendidas para cualquiera de los tres productos es superior a 300 unidades.
    - Alguno de los tres productos tuvo ventas superiores a 1000 unidades.
    - El promedio de ventas es superior a 700.
    - El producto C no es el más vendido.


2. Escribe un programa para el que dado un valor real, calcule $f(x)$ a partir de la función definida como:


$$
f(x) = \begin{cases}
    1 & \text{if } x < -1, \\
    -x & \text{if } -1 <= x <= 1, \\
    -1 & \text{de cualquier otra manera.}
\end{cases}
$$


3. Una empresa desea calcular la estimación del aporte de impuestos que los empleados deben pagar. Para los ingresos inferiores a 9000 USD no aplica dicho recaudo. Para los comprendidos entre [9000, 20000) USD, el recaudo es del 17%. En cuanto a los comprendidos entre [20000, 40000) USD, están sujetos al 28%. Finalmente, para quienes tienen ingresos iguales o superiores a 40000 USD, el aporte es de 40%. Implemente una función `taxes(income)` que calcule los impuestos correspondientes a los ingresos del colaborador. Redondee la salida a dos cifras después de la coma.

    - Un par de ejemplos para las entradas y salidas de la función son:

        ```python
        In [6]: taxes(income=15000)
        Out[6]: 2550.0
        In [7]: taxes(income=75260)
        Out[7]: 30104.0
        ```
    - **Nota:** Tenga en cuenta que $[a, b]$ hace referencia a un intervalo cerrado, mientras que $(a,b)$ es un intervalo abierto. Cuando se dice que el intervalo es cerrado, entonces el valor del límite está incluido mientras que cuando es abierto, el valor del límite no lo está.
