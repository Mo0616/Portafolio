# Analisis de Datos - Python + Dashboard HTML

Proyecto de analisis de datos con datos ficticios de satisfaccion de clientes. Calcula indicadores basicos, selecciona atributos con Information Gain y genera un dashboard HTML para presentar resultados.

## Tecnologias

- Python
- CSV
- HTML/CSS
- Concepto equivalente a seleccion de atributos con Weka `InfoGainAttributeEval`

## Ejecutar

```powershell
python src/analisis.py
```

## Salida

El script crea `salidas/dashboard.html` con:

- total de registros analizados;
- porcentaje de satisfaccion;
- tiempo promedio de respuesta;
- ranking de atributos por Information Gain.

## Nota

Los datos son ficticios y no representan informacion de clientes reales.
