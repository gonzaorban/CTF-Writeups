# Desafío 14 - Manipulando el Stack

## Análisis

La IA siempre juega perfecto por lo que es imposible ganarle dentro de la lógica del juego. La vulnerabilidad está en que el campo de nombre tiene un límite de caracteres definido en el código — al superar ese límite se produce un desbordamiento de buffer que afecta el stack.

## Explotación

Se introduce un nombre con más caracteres que el límite establecido en el código.

![Desafío 14 - Manipulando el Stack - imagen 1](images/01.png)

![Desafío 14 - Manipulando el Stack - imagen 2](images/02.png)

![Desafío 14 - Manipulando el Stack - imagen 3](images/03.png)

## Flags

```
eca0049bb012c0ab9df50049c750cdc3
```

```
38d7dd8be12354ab48711e150b977555
```
