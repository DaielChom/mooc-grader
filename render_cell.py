import base64
from IPython.display import display, Javascript
from IPython.utils.py3compat import str_to_bytes, bytes_to_str

def new_cell(texto,tipo_celda):
  
  if tipo_celda == "markdown":
    
    display(Javascript("""
      var mark = IPython.notebook.insert_cell_above('markdown')
      mark.set_text("{0}")
    """.format(texto.encode('utf-8'))))
 
  if tipo_celda == "code":
    texto = bytes_to_str(base64.b64encode(str_to_bytes(texto)))
    display(Javascript("""
    var code = IPython.notebook.insert_cell_above('code')
    code.set_text(atob("{0}"))
    """.format(texto)))

def import_cells():
    dato = []

    import quiz_for_student as qft

    for i in qft.l:
        new_cell(i[0],i[1])

