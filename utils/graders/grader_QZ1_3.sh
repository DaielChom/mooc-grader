#!/usr/bin/python

import sys
sys.path.append("./utils/student_function/")

import student_QZ1_3 as st

def multiplicacion_grade(a,b):
    return a*b

## Calificacion de la funcion del estudiante
if st.multiplicacion(12, 24) == multiplicacion_grade(12, 24):
    print "Felicitaciones##5"
else:
    print "Vuelve a intentarlo##1.3"