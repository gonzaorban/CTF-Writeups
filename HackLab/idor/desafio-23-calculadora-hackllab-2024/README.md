# Desafío 23 - Calculadora (HacklLab 2024)

d27fa3f8fc14ea101603d09436e28fb6 
Desafío 23 - Calculadora (HacklLab 2024) 
Descargas la calculadora.jar y de ahí extraes el RAR. 
 
El código logramos identificar porque es el único que aparece  en todo el archivo. Las partes 
roja no te permite visualizar el código que hay debajo 
 
 
Borramos la primer h del código dejando como primer elemento la a de manera que el 
decodificador funcione correctamente. 
 
aHR0cDovL2FwaS1jYWxjdWxhZG9yYS5zb2Z0d2FyZXNlZ3Vyby5jb20uYXIvdmVyaWZpY2
FyLWNvZGlnby1jYWxjdWxhZG9yYS8/dD0=

![Desafío 23 - Calculadora (HacklLab 2024) - imagen 1](images/01.png)

![Desafío 23 - Calculadora (HacklLab 2024) - imagen 2](images/02.png)

![Desafío 23 - Calculadora (HacklLab 2024) - imagen 3](images/03.png)

Abrimos el archivo .class y vemos que está en base 64. 
 
Vemos que en varias aparte aparece Base64

![Desafío 23 - Calculadora (HacklLab 2024) - imagen 4](images/04.png)

![Desafío 23 - Calculadora (HacklLab 2024) - imagen 5](images/05.png)

Entramos a esta página para poder convertir el código 
https://www.base64decode.org/es/ 
 
 
LA A AL PRINCIPIO ES MUY IMPORTANTE, ya que, las cadenas Base64 que codifican 
URLs que empiezan por http normalmente comienzan con aHR0c... (la a inicial es 
importante). 
 
Sobre el = al final. 
El = es padding. Indica que el total de bytes no llenó un bloque completo de 3 bytes. No 
forma parte del contenido, sólo fija la longitud para que el decodificador reconstruye 
correctamente los bytes finales.

![Desafío 23 - Calculadora (HacklLab 2024) - imagen 6](images/06.png)

Copiamos el URL y abrimos en otra pestaña 
https://api-calculadora.softwareseguro.com.ar/verificar-codigo-calculadora/?t= 
Lo que hay que hacer ahora es enviar ese código oculto (ABCD) al endpoint de la API. 
Eso debería devolver el HASH. 
 
 
 
110bacfb41660e03ba586822ab7600ff

![Desafío 23 - Calculadora (HacklLab 2024) - imagen 7](images/07.png)

![Desafío 23 - Calculadora (HacklLab 2024) - imagen 8](images/08.png)

![Desafío 23 - Calculadora (HacklLab 2024) - imagen 9](images/09.png)
