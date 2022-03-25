#!/usr/bin/python3
# proxy 
# Usando procesos para multi-clientes
import os, signal
import sys
import jsockets
import threading

def childdeath(signum, frame):
    os.waitpid(-1, os.WNOHANG)

def Rdr(conn1, conn2):
    while True:
        try:
            data = conn1.recv(1500)
        except:
            data = None
        if not data: break
        conn2.send(data)
    conn2.close()
    print('lost')

# Este el servidor de un socket ya conectado
# y el cliente del verdadero servidor (host, portout)
def proxy(conn, host, portout):

    conn2 = jsockets.socket_tcp_connect(host, portout)
    if conn2 is None:
        print('conexión rechazada por '+host+', '+portout)
        sys.exit(1)

    print('Cliente conectado')

    newthread1 = threading.Thread(target=Rdr, daemon=True, args=(conn,conn2))
    newthread1.start()
    Rdr(conn2, conn)
    print('Cliente desconectado')
    
# Main    

if len(sys.argv) != 4:
    print('Use: '+sys.argv[0]+' port-in host port-out')
    sys.exit(1)

portin = sys.argv[1]
host = sys.argv[2]
portout = sys.argv[3]

signal.signal(signal.SIGCHLD, childdeath)

s = jsockets.socket_tcp_bind(portin)
if s is None:
    print('bind falló')
    sys.exit(1)

while True:
    conn, addr = s.accept();
    pid = os.fork()
    if pid == 0: # Este es el hijo
        s.close() # Cierro el socket que no voy a usar
        proxy(conn, host, portout)
        sys.exit(0)
    else:
        conn.close(); # Cierro el socket que no voy a usar
