- Los parámetros del tipo de conexión "CS" y la probabilidad de pérdidas "Lx" se pueden modificar fácilmente en
el inicio del código de proxy1.py. Están enmarcados en el comienzo del código como #VARIABLES GLOBALES# y sus
nombres son "tipo" para el tipo de conexión y "perdida" para la probabilidad de pérdida.

- Para correr proxy1 se debe hacer en linux, ya que windows tira errores varios. WSL funciona tambien.

- Para efectos e la tarea, se corre con la línea "python3 proxy1.py 1818 anakena.dcc.uchile.cl 1818"

- Esta implementación, como está comentado en el informe de la entrega, es bastante ineficiente, debido al timeout
en la línea 49 del código. Se puede reducir el timeout, pero puede generar problemas, especialmente con una 
probabilidad de pérdidas grande.
