import os,socket,threading

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('localhost',9999))

server.listen()
clients=[]
users=[]
try:
    with open(r'.\database\userDetails.csv','r') as dUser:
        detail=dUser.read()
        detail=detail.split(",\n")
        users=detail
        dUser.close()
except:
    with open(r'.\database\userDetails.csv','a') as dUser:
        dUser.close()

def newUser(user):
    with open(r'.\database\userDetails.csv','w') as dUser:
        content=f"{user},\n"
        dUser.write(content)
        dUser.close()
    path=f'.\database\{user}.csv'

    with open(path,'w') as userD:
        userD.close()
    print("addnewuser..")

def GroupCreation(user,groupName):
    groupNameC=f"{user}-{groupName}"
    path=f'.\database\{groupNameC}'
    os.mkdir(path)
    print('created group..')
    accessPath=f"{path}\groupaccess.csv"
    print(accessPath)
    with open(accessPath,'w') as access:
        access.write(f'{groupNameC}\n{user}\n')
        access.close()
    print('created group..')
    path=f'.\database\{user}.csv'
    with open(path,'a') as addgroup:
        addgroup.write(f'{groupNameC}\n')
        addgroup.close()
    print("upadated the userD..")

def createQuestionPaper(groupName,paperName):
    path=f".\database\{groupName}\{paperName}.csv"
    with open(path,'a') as file:
        file.close()
    print('createdpaper..')

def GroupUpdates(groupName,paperName):
    pass
def groupList():
    path=f'.\database\{user}.csv'
    print(path)
    with open(path,'r') as a:
        d=a.read()
        if d=="":
            d="empty"
        client.send(d.encode())
        
    print("send")
    

def chat(client,user):
    try:
        while True:
            a=client.recv(1024).decode()
            print(f"{client} : {a}")
            command=a.split(" ")
            print(command)
            try:
                if command[0] == 'count':
                    print(len(clients))
                if command[0] == 'break':
                    client.close()
                if command[0] == 'users':
                    print(users)

                if command[0] == 'whoami':
                    print(user)
                if command[0] == 'grouplist':
                    groupList()

                if command[0] == 'creategroup':
                    GroupCreation(user,command[1])    #username #groupname

                elif command[0] == 'createpaper':
                    createQuestionPaper(command[1],command[2])   #groupname papername

            except:
                pass
              
                        
    except:
        clients.remove(client)
        pass


while True:
    global user
    client,addr=server.accept()
    user=client.recv(1024).decode()
    if user not in users:
        users.append(user)
        newUser(user)
    clients.append(client)
    print(user)
    thread=threading.Thread(target=chat,args=(client,user,))
    thread.start()
