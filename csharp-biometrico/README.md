# Sistema Biometrico de Huellas - C# + MySQL

Prototipo academico de autenticacion biometrica por comparacion de patrones. El proyecto simula plantillas de huellas como puntos de minucia y calcula un porcentaje de coincidencia para aprobar o rechazar el acceso.

## Tecnologias

- C# / .NET 8
- Programacion orientada a objetos
- MySQL como modelo de persistencia documentado en `database/schema.sql`

## Ejecutar

```powershell
dotnet run
```

## Alcance

- Registro simulado de personas y plantillas biometricas.
- Comparacion de patrones con distancia y angulo.
- Umbral de aprobacion configurable en el codigo.
- Script SQL para crear una base MySQL de referencia.

## Nota

No almacena huellas reales. Las plantillas incluidas son datos ficticios para demostrar la logica del portafolio.
