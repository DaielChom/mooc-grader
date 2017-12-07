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
* ~~Crear un repositorio con nombre `mooc-grader` y alli alojar todo lo que estoy haciendo. creo que lo ideal seria usar ramas, aunque aun debo aprender a usarlas XD.~~
* ~~Hacer que me pueda devovler~~
* ~~Probar que el deadline funciona~~
* ~~Probar el scrypt to_student~~
* ~~Hacer que el archivo `template` y si se puede el `RLXMOOC CONFIGS` se generen automaticamente.~~
* Añadir los notebooks `FIXCHARING` y `COMPUTEGRADER`

#### Desarollo
* El respositorio se encuentra en DaielChom/mooc-grader
* Ya sirve, si uno se equivoca en poner los parametros ya sirve volver a escribir los paramestro y corregir los archivos de configuracion
* Pues al parecer no funciona, mentira si funciona hay que configurar bien el formato que viene siendo
> course_id+"::"+problem_set_id+"::"+configvar
> 2017BG::QZ1::harddeadline	2016/01/24 22:20:15 [-0500]
2017BG::QZ1::softdeadline	2016/01/23 21:10:15 [-0500]

* Bujajajjajja el deadline funciona y lo hace automaticamente

* Listo, el script funciona


#### Reunión 17 - oct- 2017
"MERISII!! El jueves pero no puedo ir, creo que ire igualmente; Pedaleo intenso con la aux y lo mas reciente pero lo mismo de siempre mi hermana es un fastidio. De las tareas que se propusieron se hicieron la mayoria, pero lo que hay es cosas por hacer y bastantes, la reunion no se llevo en la oficina del profe si no durante la clase de bigdata pues el lunes fue festivo y pues ni modo. Listo de las tareas que se realizaron no hubo problema con ninguna tan solo con la del diccionario del curso, es mejor que el profesor la llene el mismo sin lo del for, hay que arreglar eso, dos la duda principal era lo de los deadline, ya me dijo el profesor que las asociara, entonces hago estos dos arreglos y limpio, por que se necesita una limpiada, una vez limpia recreo el curso y hago el siguiente arreglo que es hacer que el grader sirva con notas de 1 a 5 no con CORRECT y NO CORRECT. Una vez echo este cambio una nueva limpieza y a seguir con la otra tarea que esa si la veo complicada y es hacer las intrucciones de creacion de quices y un "grader" que sirva independientmeente del lengujae en el que se hagan los quices, algo complicado pero con el subprocess deberia funcionar, la idea es que el subprocess aparesca en el rlxmooc, que llame al grader y este y que lea la respuesta independientmeente de lo que haga el grader al rlxmooc solo le importa el archivo que escriba el grader con la nota. AH TRABAJR.

#### Tareas.
* ~~Arreglar lo de la estructura del curso.~~
* ~~Asociar Deadlines~~
* ~~Limpiar~~
* ~~Grader funcione con notas, crear parametros para una nota maxima y una nota minima.~~
* Grader funcione independientmeente del lenguaje. DUDA: con el grader

#### 26 - oct - 2017:
"Hablando con yes kar es hermosa XD". Ayer no solicite, oigna al otro quisque ayer hoy es jeuves, el lunes no solicite reunion con raul, por uqe ando atrasado bastante atrasado :D. o yo mio yo mio. Pero hay buenas noticias ya hice que el grade funcionara con notas de 0 a 5, la joda es que no tengo una nota maxima y una minima, creo que eso me tocara arreglarlo despues.

#### 30 - oct - 2017:
"Millonario, huelo dinero ajjaja, pero calmado. No hagas lo de la lecherita". A raul le da risa que no escriba, ajaaa. aunque a cualquiera en las reuniones hablamos de bsatantes cosas que es facil perder la cuneta de las mismas. y antes de que yo pierda la cuenta se que son 4 cosas que le debo corregir al mooc, antes de pasar a la parte de calificar con notas.
1. ~~Arreglar la parte de la definicion del curso, que el ejemplo quede de primeras y describir el mismo. y que lo de la estructura quede cuando uno va a definir la variable course.~~
2. ~~Un warning de cuando el grader entrege una nota que se salga de 0 o el limite maximo. no matarme tanto en que haga algo solo el warning, eso si indicar que si el grader entrega notas diferentes a las definidas pues los calculos no cuadraran.~~
3. ~~que muestre el link del rlxmooc que se crea, y agregar al fondo, sin necesidad de que yo corra las celdas lo de agregar los deadlines.~~
4. ~~sacar a un lado lo del template del quiz, para que al profesor le quede mas facil crear los propios.~~
5. meterle mano a la redaccion y ortografia XD. que mierda.
Una vez limpira la maquina despues de estos arreglos, y otros que recuerde, ahi si pasar a la parte a que el grade funcione independientmeente del lenguaje.
6. ~~que muestre la direccion donde se crea el copy-to-students
Listo esos son los arreglos que se le deben poner al mooc y ahi si saltar a lo de que el grader funcione independiente del lenguaje.~~
7. ~~que grabe el curso completo en el archivo mooc~~

#### 7 - Nov - 17
~~"Se debe olvidar la pequeña nacion y el blanconegro se dan garra. deberia dejar de escribir sobre el pais, pero no se aj, es triste "~~ "Y si la pacas no me deja dormir con ella  jajajajja y como estara mi prima :P eso tambien es triste malditasea". YO si que la cago y a la primera. Justamente en el titulo que es lo que el puto de Github no me estaba leyendo por la etiqueta center, habia un error de ortografia y pues no lo corregi y pues  llego diciendo pum arregle redaccion y pum ese error. ahi dios raul cada vez mas se da cuenta de como voy siendo aunque tambien trato como de pelearle jajajaj. pero bueno el caso cosas por hacer.
* Arreglar el titulo
* Arreglar lo del problema del correo del profesor
* Agregarle una etiqueta en github, que eso no tengo ni puta idea como sera
* Empezar con lo del grader independiente del lenguaje.

#### 19 - Nov - 2017:
"Hoy debe ser productivo" No he avansado nada, pase el fin de semana en aguazul y me la he pasado traabajando en el diplomado que no me he metido con el mooc-grader. pero hoy sera mero mooc grader, cabe recordar que tuve una reunion con raul y fabio y se debe hacer una exposicion el jueves con todo el trabajo que se hizo. para eso tengo que hacer dos o tres transparencias y erda creo que primero me matare con el grader y luego si con la presentacion.
* Diapositivas
* Grader independiente del lenguaje.

#### 21 - Nov - 17:
"Estoy eufrico, fue un buen dia, me relacione con muchas personas y avance bastante en mis cosas, bastantes risas y recocha. jaj un ben dia y la de vladimir paila, pero despues tengo ganas de hacer varias compras, la lista de compras ira despues". Hoy me reuni con raul durante la clase de bigdata, aunque tengo que ponerme serio con los problemsets. el caso es que hable con el y se hicieron unos pequeños cambios al proceso de check y submit, lo que se hara es ejecutar un shell .sh el cual entregue la nota, el shell debe estar encriptado y es el profesor el que se encarga de hacer dicho shell, yo solo le digo que lo ponga con cierto formato en cierto directorio, el check y submit lo desencriptan y sacan la nota, los mensajes e imprime y pues guarda la nota. y ya de esa manera queda todo funcionando, a otra cosa el binario crypt el profesor no lo entrega en el repo de los estudiantes. A bueno si, ya el jeuves a las 8:30 esta la exposicion final de esta monda, ya lo que fue fue como quien dice por ahi. me da cagada que raul no me contrate despues pa otras cosas, ya se esta dando cuenta de que soy bien brutico XD.  

#### 23 - Nov - 17:
"Setsi se nos va". Raul le da risa mi forma de entender. Esta vez no fue planeada la reunion ni nada por el estilo, llegue a la oficina de el y le pedi un rato a ver si podia y dijo que si y pues entre, despues de que el ceo hablara con el profe. Y tengo un par de nuevas tareas, tambien me dio una idea de las nuevas cosas que querian implementar en el mooc-grader. entoncs la cosa es asi.
* Arreglar lo de copy-to-students para que tambien agrege la carpeta de graders compilados
* Quitar el sucess
* hacer un ejercicio en c
* Limpiar
Y aqui un buen commit. Ahora despues de que el grader funcione independiente del lenguaje raul todavia tiene una gran cantidad de ideas, sobre todo para evitar que los estudiantes dejen tanta copia. Y es que teniendo un banco de preguntas, cada vez, en un quiz, que el estudiante se registre en el encabesado del quiz se renderice una serie de preguntas, de las cuales se tenia un md y un codigo. la idea es que los ejercicios sean aleatorios, pero que cada vez a cada estudiante se le generen los mismos, es decir que con el correo o el codigo del estudiante se gener una serie de numeros de preguntas pero por estudiante siempre se le va a generar la misma serie aleatoria. Por ahora realizar las primeras tareas y luego si matarme con lo de el renderizado.

#### 4 - Dic - 17:
"Y la reunion de QR no hace mas que aplasarse, FESTIVAL DE LOS PLANETAS con mi primo @Yeleyu". Bueno la limpieza ya quedo y al aprecer funciona la version independiente del lenguaje, pase por donde raul y no estaba, las ultimas semanas he estado algo quedado con la auxiliatura, pero buneo, creo que le dire mañana en el parcial o mejor le mando un correo, listo ya le mande el correo esperar a ver que. Bueno el caso lo que sigue es el renderizado de los quices que eso si es algo mas dificil, lo que el profesor desea es que al abrir un quiz este solo tenga la casilla de autetificacion y que cuando se autentifique se renderize una serie de preguntas(md) y ejercicio a hacer. esta serie de preguntas renderizadas salen de un banco y son diferentes por cada estudiante. pero cada vez que el estudiante ingresa al mismo quiz se genrean las mismas preguntas en el mismo orden. y esta es la tarea que tengo que hacer, complciado por ahora me tocara investigar como renderizar los quices.

#### 6 - Dic - 17:
"Ser tan dormido para ir a frances el dia que no toca". el dia de ayer estuve reunido con el profe raul, el cual creo qeu esta empezando a disgustarse por que no estoy trabajdno en el proyecto de grado, no he podido avanzar por lo del diplomado y cositas de sevent, y el no sabe eso, ya carlos y el CEO me advirtieron que ojo que depronto me regaña por andar de vago, pero tampoco le quiero decir, no quiero sonar engreido ni nada por el estilo, aunque cuando salga de cosas de la u y del diplomado me le dedico de lleno a eso, me toca a ver si este fin de semana organizo mis tareas y mis semanas para ir trabajando en todo de a poquito como suelo hacer. bueno la cosa es que tengo que hacer un pequeño cambio en lo del ejercicio de C. y es que el archivo grader mejor crearlo y eliminarlo dentro del archivo sh, que por eso no hay problema.
