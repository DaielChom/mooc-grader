# Mooc-grader

### Descripcion
`Mooc-grader` es un `framework` diseñado para la implementación de `notebooks` en la elaboracion y calificacion de talleres (`PROBLEMSET`) y evaluaciones (`QUIZZES`) de un curso. La calificación se hace de manera automatica mediante el uso de calificadores o `graders` registrando las notas en una hoja de calculo de Drive compartida entre el tutor y el estudiante.

### Dependencias
`mooc-grader` es un `framework` desarrollado en `python 2.7`.
`mooc-grader` depende de las librerías documentadas en el archivo [dependencias.txt](./dependencias.txt)

### Instalación
Se puede clonar el repositorio o descargar el ZIP del mismo, independientemente de la metodologia que use se recomeinda crear un entorno virtual para el uso del framework.

	# Configuracion entorno virtual, se requiere de `virtualenv`

	~$ mkdir proyecto && cd proyecto
	~/proyecto$ virtualenv venv
	~/proyecto$ source venv/bin/active

	# En este caso se opta por clonar el repositorio

	(venv) ~/proyecto$ git clone https://github.com/DaielChom/mooc-grader.git  
	(venv) ~/proyecto$ cd mooc-grader
	(venv) mooc-grader$ pip install -r dependencias.txt
	(venv) mooc-grader$ jupyter notebook

	# Abrir el notebook instrucciones para empezar.

### Uso

Para inicar la elaboración del `curso`, es decir la implementacion del `framework`, se debe elaborar la guia de [instrucciones](./instrucciones.ipynb).
