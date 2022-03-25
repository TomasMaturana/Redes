import os, signal
import sys, threading
import jsockets

if len(sys.argv) != 4:
    print('Use: '+sys.argv[0]+' hostPort host serverPort')
    sys.exit(1)

class ClientThread(threading.Thread):
    def __init__(self, addr, s):
        threading.Thread.__init__(self)
        self.sock = s
    def run(self):
        print('Cliente Conectado')

        s2 = jsockets.socket_udp_connect(sys.argv[2], sys.argv[3])
        if s2 is None:
            print('No se pudo conectar a proxy2')
            sys.exit(1)
        
        while True:
            try:
                data = self.sock.recv(1024)
            except: break
            
            
            s2.send(data)
            print('Datos enviados a proxy2')
            try:
                data2=s2.recv(4096) #.decode()
            except:
                print('Error: proxy2 no está en ejecución.')
                errMsj='Error: proxy2 no está en ejecución. \n'
                self.sock.send(errMsj.encode())
                break
            if data2.decode() == '#_$#ERROR#$_#':
                print('Error: server_echo4 se ha cerrado inesperadamente. Reinicie la conexión.')
                errMsj='Error: server_echo4 se ha cerrado inesperadamente. Reinicie la conexión. \n'
                self.sock.send(errMsj.encode())
                break
            self.sock.send(data2)
            print('Datos enviados a client_echo2')

        s2.close()
            
        self.sock.close()
        print('Cliente desconectado')
    
s = jsockets.socket_tcp_bind(sys.argv[1])
if s is None:
    print('could not open socket')
    sys.exit(1)
while True:
    conn, addr = s.accept();
    newthread = ClientThread(addr, conn)
    newthread.start()



