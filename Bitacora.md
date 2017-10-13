# Bitacora del Capitan
DaielChom

#### Reunión 18 - sep - 17:
Me siento hacker, de haber sabido como funciona la maquina virtual desde antes hubiera sido el putas boy de la pradera city XD. Pero Volviendo a la realidad tengo que hacer un grade, practicamente crear mi propio problemset, con respuesta y corrector y tales. A ver si me acuerdo de todo lo que me dijo raul cuando lo vaya  hacer.
* Trabjar con la maquina de Hadoop
* Hacer el grade y tratar de parametrizar
* Revisar eso a ver si puedo hacer el grade sin necesidad de entrar la maquina virtual por ssh.

##### Cosas a contar:
* Solo se cuenta con un total de 1.5G de almacenamiento por archivo en el moodle.

#### Reunión 25 - sep - 17:
"Me cago en la mierda tio". Jajajajaajja voy bien, lento pero seguro, le mostre, lo que hasta el momento llevaba, al profe raul, que lo que llevo es la guia de com o hacer un notebook de quiz, ahora lo siguiente es parametrizar y hay voy de a poquito mientras "cojo callo" con linux. Aunque aprovecho para hablarme de lo sigueinte que se debe hacer y es que el documento donde se ponen las notas, toma una plantilla que tiene el profesor en su drive y lo copia en el drive de cada estudiante y luego si, sobre cada xls pone las notas. La idea es que dicho archivo se cree de una vez en el estudiante sin pasar por ningun tipo de plantilla. Y mucho mas adelante meterme con unas opciones de "configuracion" que tiene dicha plantilla.

#### Reunión 02 - oct - 17:
"Ya voy sacando callo". Viento en popa capitan, la parametrizacion ya quedo gracias a `sed` y a una ayuda de rual dado que `sed` presenta problemas con el el conjunto de caracteres `\n`, pues los toma como salto de linea, y yo necesitaba que apareciera y no que se lo saltara. Falta arreglar un error con el archivo RLXCONF dado que necesito la existencia del mismo, para que funciones el SUBMIT, una vez arreglado esto, empezar con lo de crear los archivos sin ncesidad de Template. que eso si yo digo jmm joven, no se como hacerlo.

#### Update 10 - oct - 17:
"El frio me da orinadera ala" ayer no hubo reunion, dado que estuve de vago y no adelante nada, una reunion quedo propuesta para el viernes, asi que de aqui al viernes me toca trabajar.  ayer trabaje y como que ya corregi un error que me salia por que no tenia el archivo RLX CONF. pero por cuestiones de que me comi la cuota, no he podido probar si funciona, pero parece que si pues con la chicha alexia funciono asi que se le podria decir a raul que ya esta parametrizada, abria que empezar con eso de crear un sheet, pero prefiero esperar a reestablecer la cuota. Sin embargo si toca ir pensando como y en donde meter lo de crear el archivo. Me toca llevarle algo el viernes creo que le metere mano a eso.

#### Reunión 13 - oct - 17:
"Recorte la foto esperar que reaccion tiene seria bueno que todo sea bien, pero no se". Tuve varios problemas, entre ellos la quota que se me acabo, RLXCONFS al no estar generaba errores, entre otros, ya quedaron corregidos para la presente reunion y una prueba exitosa de un grader. le explique eso a raul y ya quedo, obviamente voy un tris atrasado y ma dejo mas tareas AH!!, y por sobre todo debo subir esa miercoles a github XD jajajaj. me dio flojera hacerlo y debi de hacerlo hace rato, esa sera mi prioridad. Tambien me mostro un nuevo par de notebooks para agregar a las intrucciones que consistian en las configuraciones de los deadline y el otro para solucionar el problema que aveces no comparte un archivo drive. Entonces las tareas que se me asignaron quedan de la siguiente manera.

##### Tareas.
* Crear un repositorio con nombre `mooc-grader` y alli alojar todo lo que estoy haciendo. creo que lo ideal seria usar ramas, aunque aun debo aprender a usarlas XD.
* ~~Hacer que me pueda devovler~~
* Pribar que el deadline funciona
* Probar el scrypt to_student
* Hacer que el archivo `template` y si se puede el `RLXMOOC CONFIGS` se generen automaticamente.
* Añadir los notebooks `FIXCHARING` y `COMPUTEGRADER`
