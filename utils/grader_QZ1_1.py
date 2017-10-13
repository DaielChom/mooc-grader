
# Grader funcion creada por el profesor, no se muestra al estudiante.
def grade():
    
    # Funcion correcta
    def adivina_respuesta():
        return "Daniel"
    
    # Comprueba y se le notifica al estudiante el posible error
    import numpy as np
    
    if adivina() != adivina_respuesta():
        print("Intenta nuevamente")
        return False
    
    return True