#!/usr/bin/python

import sys
sys.path.append("./utils/student_function/")

import student_QZ1_1 as st
## Calificacion de la funcion del estudiante
if st.adivina() == "Daniel":
    print "Felicitaciones##5"
else:
    print "Vuelve a intentarlo##2"