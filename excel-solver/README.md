# Optimizacion con Solver - Excel

Modelo de asignacion de recursos para minimizar costos y cumplir un beneficio minimo. El caso reproduce el tipo de trabajo descrito en la hoja de vida: modelamiento matematico, uso de Solver y simulacion de reduccion de costos.

## Archivos

- `datos/recursos.csv`: tabla base para abrir en Excel.
- `solver_recursos.py`: version reproducible en Python con busqueda exhaustiva.
- `resultados/asignacion_optima.csv`: se genera al ejecutar el script.

## Ejecutar la version Python

```powershell
python solver_recursos.py
```

## Replicar en Excel Solver

1. Abrir `datos/recursos.csv` en Excel.
2. Crear una columna `unidades` con valores iniciales dentro de los minimos y maximos.
3. Crear `costo_total = unidades * costo_por_unidad`.
4. Crear `beneficio_total = unidades * beneficio_por_unidad`.
5. En Solver, maximizar el beneficio total con estas restricciones:
   - Costo total menor o igual a 1800.
   - Beneficio total mayor o igual a 2600.
   - Unidades entre `minimo` y `maximo`.
   - Unidades como numeros enteros.

## Resultado esperado

El modelo entrega una asignacion de recursos que cumple las restricciones y permite explicar una reduccion simulada de costos frente a una asignacion manual.
