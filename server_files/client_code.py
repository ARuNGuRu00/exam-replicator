import socket 
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('localhost',9999))
def recives():
    client.send("grouplist".encode())
    grouplist=client.recv(20000).decode()
    return grouplist
while True:
    g=input("enter:")
    client.send(g.encode())
    if g=="break":
        client.send(g.encode())
        break
    if g=="grouplist":
        recives()