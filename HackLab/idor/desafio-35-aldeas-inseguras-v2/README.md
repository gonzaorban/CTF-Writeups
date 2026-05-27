# Desafío 35 - Aldeas Inseguras V2

Desafío 35 - Aldeas Inseguras V2 
Primero que nada es muy parecido al de Aldeas Inseguras que ya realizamos en donde ya 
supimos como enviar Oro de uno a otro en escalera, en este caso la Plata y el Bronce no 
hay límite para recibir entonces podes enviarle todos directamente a Pedro. En el caso de 
Oro hay que realizar una escalera para que vayan acumulando. 
 
Como en este caso son muchos registros en vez de hacer uno a uno realizamos un ataque 
de listas donde vamos modificando cada origen y se envía al mismo destino en el caso de 
Plata y Bronce. Pero en el caso de Oro necesitamos realizar una escalera en la cual vamos 
a tener que ir modificando uno a uno el origen y destino, entonces el ataque se realiza sobre 
dos listas.

![Desafío 35 - Aldeas Inseguras V2 - imagen 1](images/01.png)

Realizamos una petición de Enviar mercancía y la abrimos en Intruder haciendo click 
derecho. 
 
En este ejercicio el ataque “Sniper Attack” sirve solamente para la plata y el bronce, en 
cambio, para el oro se utiliza el ataque “Pitchfork”. 
El ataque Pitchfork es para listas dobles y lo que hace es hacer el primer elemento 
de la primera lista con el primer elemento de la segunda lista, luego con el segundo de la 
primera lista con el segundo elemento de la segunda lista y así sucesivamente… 
El ataque CLuster Bomb hace un producto cartesiano evaluando todas las 
posibilidades. 
 
 
 
Lista 1 
bde44e88ebd3925ff843b2e31bda83d7 
74d2afa3a1f4894c8829c6f80a7a436b 
f29ae2207b53b27bc0cfb758b910476f 
f6cb7ff9058fdfe1b6cd21de0dcb4618 
e9432dc2f3f99b5d00fb4144d232efda 
6464c004dfdf96f42bd5d64f8e3f507d 
6aca358cf89c4ee1b46cfef0ace4e0bf 
d9537eba52bbfccfb912b2bdf64d6142 
be637e3073a1e7e5cfb86c5978c9560a 
ac550a1da769ae43f800adbff174e7dc 
9fedb91a0f93706d7f09b44d0e5b94c1 
115d2db0ba51ec6f82172a6246551b17 
bdbcc9b006186e87657912bbb0411a37 
 
Lista 2 
ee2e04b3d8686ef9a055626e762c20be 
bde44e88ebd3925ff843b2e31bda83d7 
74d2afa3a1f4894c8829c6f80a7a436b 
f29ae2207b53b27bc0cfb758b910476f 
f6cb7ff9058fdfe1b6cd21de0dcb4618 
e9432dc2f3f99b5d00fb4144d232efda

![Desafío 35 - Aldeas Inseguras V2 - imagen 2](images/02.png)

6464c004dfdf96f42bd5d64f8e3f507d 
6aca358cf89c4ee1b46cfef0ace4e0bf 
d9537eba52bbfccfb912b2bdf64d6142 
be637e3073a1e7e5cfb86c5978c9560a 
ac550a1da769ae43f800adbff174e7dc 
9fedb91a0f93706d7f09b44d0e5b94c1 
115d2db0ba51ec6f82172a6246551b17 
 
Para poder realizar los ataque tuvimos que recolectar los ids de los jugadores colocándolos 
en un txt para luego subirlos en el Intruder seleccionando: solamente el origen (en el ataque 
Sniper Attack); y el origen y el destino en el ataque Pitchfork.  
En el SCRIPT se indican los primeros dos elementos de cada lista que no se deben cargar 
en ellas, en caso de que las contengan realizamos un REMOVE de esa única línea. 
 
 
(Apartado de Intruder, más abajo sigue la explicación)

![Desafío 35 - Aldeas Inseguras V2 - imagen 3](images/03.png)

Una vez seleccionado el origen le damos a Add $ arriba a la izquierda y cargamos el txt con 
las listas en el Load…  
 
 
 
 
 
 
 
 
 
 
 
 
 
En el ataque Pitchfork se ponen los ids en escalera cosa que se puedan ir intercambiando el 
oro sucesivamente. En los otros ataques no hace falta ya que, es una sola lista.  
 
Asi debería quedar con la lista cargada

![Desafío 35 - Aldeas Inseguras V2 - imagen 4](images/04.png)

![Desafío 35 - Aldeas Inseguras V2 - imagen 5](images/05.png)

![Desafío 35 - Aldeas Inseguras V2 - imagen 6](images/06.png)

136868cdc797f8c6698d5d1b1761aaf7

![Desafío 35 - Aldeas Inseguras V2 - imagen 7](images/07.png)
