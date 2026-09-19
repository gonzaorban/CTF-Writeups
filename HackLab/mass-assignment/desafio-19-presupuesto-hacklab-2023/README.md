# Desafío 19 - Presupuesto (HackLab 2023)

**Plataforma:** HackLab (SoftwareSeguro)  
**Edición:** HackLab 2023  
**Categoría:** Mass Assignment  

## Análisis

El endpoint de edición de presupuestos acepta campos adicionales en el JSON. Al incluir `revisado: true` junto al monto, el servidor lo procesa sin validación.

## Explotación

Se inspecciona la estructura de la respuesta GET para identificar los campos disponibles.

![Desafío 19 - Presupuesto (HackLab 2023) - imagen 1](assets/01.png)

![Desafío 19 - Presupuesto (HackLab 2023) - imagen 2](assets/02.png)

Al presionar "Revisar", se intercepta el POST y se modifica el JSON:

```json
{
  "monto": "1000.00",
  "revisado": true
}
```

Se repite para todos los presupuestos indicados por el enunciado (se usó IA para determinar cuáles campos modificar con los datos de la tabla).

![Desafío 19 - Presupuesto (HackLab 2023) - imagen 3](assets/03.png)

![Desafío 19 - Presupuesto (HackLab 2023) - imagen 4](assets/04.png)

![Desafío 19 - Presupuesto (HackLab 2023) - imagen 5](assets/05.png)

![Desafío 19 - Presupuesto (HackLab 2023) - imagen 6](assets/06.png)

![Desafío 19 - Presupuesto (HackLab 2023) - imagen 7](assets/07.png)

Una vez modificados todos los registros indicados con `revisado: true`, se obtiene el código.

![Desafío 19 - Presupuesto (HackLab 2023) - imagen 8](assets/08.png)

## Flag

```
bf58371373e52613ae270d5acf832bad
```
