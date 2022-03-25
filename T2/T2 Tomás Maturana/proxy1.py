#!/usr/bin/python3
# proxy 
# Usando procesos para multi-clientes
import os 
import signal 
import sys 
import jsockets 
import threading 
import time

####### VARIABLES GLOBALES ##########################
tipo="CS"     #tipo de conexión con anakena        ##
perdida="L1"  #probabilidad de pérdida de paquetes ##
#####################################################

def childdeath(signum, frame):
    os.waitpid(-1, os.WNOHANG)

def Rdr(conn1, conn2, e, serie, data=None):
    if data:          #transmitiendo a proxy server
        while not e.is_set():
            conn2.send(data)
            print("Datos enviados a proxy server")
            event_is_set = e.wait(0.3)
            if event_is_set:
                break
    
    else:             #esperando ACK de proxy server
        while True:
            try:
                data = conn2.recv(1024)   #ACK
                data2 =  conn2.recv(1024) #eco 
            except:
                data = None
                break
            if not data: break
            verificar=str(data.decode())
            print("ACK= " + verificar)
            verificar2=str(data2.decode())
            print("eco= " + verificar2)
            if verificar[1]==str(serie):     #ya sea un ACK o el eco, lo importante es que le llegó y hay que verificar que tenga la misma serie
                ok="A"+str(serie)
                e.set()
                conn2.send(ok.encode())
                global perdida
                if int(perdida[1])>0:
                    while True:
                        try:
                            print("Esperando última confirmación. Esto puede tardar hasta "+ perdida[1] + " segundos.")
                            conn2.settimeout(10*int(perdida[1]))
                            cosas = conn2.recv(1024)   #no llegó el ACK de ACKs?? => siguen llegando msjs "DX______"
                        except:
                            cosas=None
                            break
                        if not cosas: break
                        if len(cosas)==0: break
                        cosas2=str(cosas.decode())
                        if cosas2[1]!=str(serie):
                            break
                        else:
                            print("Retransmitiendo ACK de ACKs: "+ ok)
                            conn2.send(ok.encode())
                msj= verificar2[2:len(verificar2)]
                conn1.send(msj.encode())  #eco a client
                print(msj)
                break
            # intento de optimización de reenvío de ACK de ACKs
            # s=(serie+1)%2
            # if verificar[1]==str(s):
                # print("enviando ACK anterior")
                # ok="A"+str(s)
                # conn2.send(ok.encode())

# Este el servidor de un socket ya conectado
# y el cliente del verdadero servidor (host, portout)
def proxy(conn, host, portout, tipo, perdida):

    conn2 = jsockets.socket_udp_connect(host, portout)
    if conn2 is None:
        print('conexión rechazada por '+host+', '+portout)
        sys.exit(1)
        
    print('Cliente conectado')
    
    A0=0
    A1=0
    while not A1:     #configuración conexión => escribe A1=1 si salió bien
        A0=0
        while True:
            data=tipo
            conn2.send(data.encode())
            print(tipo+ ' enviado al proxy del servidor')
            try:
                data2=conn2.recv(1024)
                
            except:
                print('Error: El proxy del servidor no está disponible.')
                errMsj='Error: El proxy del servidor no está disponible. \n'
                conn.send(errMsj.encode())
                break
            if data2.decode() == 'A0':
                print('ACK de conexión recibido')
                A0=1
                break
        if A0:
            data=perdida
            conn2.send(data.encode())
            print('Probabilidad de pérdida 0.' +perdida[1]+ ' enviada al proxy del servidor')
            while True:
                try:
                    data2=conn2.recv(1024)
                    
                except:
                    print('Error: El proxy del servidor no está disponible.')
                    errMsj='Error: El proxy del servidor no está disponible. \n'
                    conn.send(errMsj.encode())
                    break
                if data2.decode() == 'A1':
                    print('ACK de pérdidas recibido')
                    A1=1
                    break
        else:
            break
            
    
    if A1:            #conexión establecida 
        serie=1
        while True:
            try:
                data=conn.recv(1024)
            except:
                print("Algo ha salido mal :( Haga nuevamente la conexión")
                data = None
                break
            if not data: break
            serie= (serie+1)%2
            data2="D" + str(serie) + str(data.decode())     
            print("Mensaje a enviar a proxy servidor: "+ data2)
            event = threading.Event()
            newthread1 = threading.Thread(target=Rdr, daemon=True, args=(conn, conn2, event, serie, data2.encode()))
            newthread1.start()
            Rdr(conn, conn2, event, serie)
    
    conn2.close()
    
    print('Cliente desconectado')
    
# Main    

if len(sys.argv) != 4:
    print('Use: '+sys.argv[0]+' port-in host port-out')
    sys.exit(1)

portin = sys.argv[1]
host = sys.argv[2]
portout = sys.argv[3]

signal.signal(signal.SIGCHLD, childdeath)

print("Comenzando conexión ->")

s = jsockets.socket_tcp_bind(portin)
if s is None:
    print('bind falló')
    sys.exit(1)
    
print("bind ok")

while True:
    conn, addr = s.accept()
    pid = os.fork()
    if pid == 0: # Este es el hijo
        s.close() # Cierro el socket que no voy a usar
        proxy(conn, host, portout, tipo, perdida)
        sys.exit(0)
    else:
        conn.close(); # Cierro el socket que no voy a usar
