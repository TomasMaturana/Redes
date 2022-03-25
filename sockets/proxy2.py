import jsockets
import os, signal
import sys, threading

if len(sys.argv) != 4:
    print('Use: '+sys.argv[0]+' hostPort host serverPort')
    sys.exit(1)

s = jsockets.socket_udp_bind(sys.argv[1])
if s is None:
    print('could not open socket')
    sys.exit(1)
while True:
    data, addr = s.recvfrom(1024)
    if not data: break

    s2 = jsockets.socket_tcp_connect(sys.argv[2], sys.argv[3])
    if s2 is None:
        print('No se pudo conectar a servidor')
        sys.exit(1)

    s2.send(data)
    print('Datos enviados a server_echo4')
    dataSV=s2.recv(4096) #.decode()
    s.sendto(dataSV, addr)
    
    print('Datos enviados a proxy1')
    
    s2.close()

s.close()

