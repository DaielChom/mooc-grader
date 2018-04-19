# Mooc-grader

### Descripcion
`Mooc-grader` es un `framework` diseñado para la implementación de `notebooks` en la elaboracion y calificacion de talleres (`PROBLEMSET`) y evaluaciones (`QUIZZES`) de un curso. La calificación se hace de manera automatica mediante el uso de calificadores o `graders` registrando las notas en una hoja de calculo de Drive compartida entre el tutor y el estudiante.

`Mooc-grader` cuenta con la siguiente arquitectura

![arquitectura](./img/arquitectura_moocgrader.svg)

### Dependencias
`mooc-grader` es un `framework` desarrollado en `python 2.7` y depende de las librerías documentadas en el archivo [dependencias.txt](./dependencias.txt)

### Instalación
Se puede clonar el repositorio o descargar el ZIP del mismo, independientemente de la metodologia que use se recomeinda crear un entorno virtual para el uso del framework.



	~$ mkdir proyecto && cd proyecto

	~/proyecto$ git clone https://github.com/DaielChom/mooc-grader.git  
	~/proyecto$ cd mooc-grader
	~/proyecto$ sudo apt-get install python-pip python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev libjpeg8-dev zlib1g-dev
	~/proyecto$ sudo apt-get install lib32stdc++6
	~/proyecto$ sudo apt-get install libcairo2-dev
	~/proyecto/mooc-grader$ pip install -r dependencias.txt
	~/proyecto/mooc-grader$ jupyter notebook

	# Abrir el notebook instrucciones para empezar.

### Uso
Para inicar la elaboración del `curso`, es decir la implementacion del `framework`, se debe elaborar la guia de [instrucciones](./instrucciones.ipynb).

### Autores
`mooc-grader` exista gracias a:
* [@rramosp](https://sites.google.com/site/rulixrp/)
* [@famarcar](https://sites.google.com/site/fmartinezc21/)
