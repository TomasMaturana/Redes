Ejecutar en consolas distintas en este orden:
1- python server_echo4
2- python proxy2.py 1818 localhost 1819
3- python proxy1.py 1818 localhost 1818
4- python client_echo2.py localhost 1818

Luego, en la consola en la que se está corriendo client_echo2, se podrá escribir un mensaje, el cual será 
enviado a server_echo4 y éste responderá con "Respuesta del servidor: {el mensaje enviado desde client_echo2}"