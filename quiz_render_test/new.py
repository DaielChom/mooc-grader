from IPython.display import display, Markdown, Audio
def new_cell(texto,tipo_celda):
  if tipo_celda == "markdown":
    display(Markdown(texto))
  if tipo_celda == "code":
    get_ipython().set_next_input(texto)