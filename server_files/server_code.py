import os,socket,threading,string,random

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


def generateCode(length=10):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))


def newUser(user):
    with open(r'.\database\userDetails.csv','a') as dUser:
        content=f"{user},\n"
        dUser.write(content)
        dUser.close()
    path=f'.\database\{user}.csv'

    with open(path,'w') as userD:
        userD.close()
    print("addnewuser..")

def GroupCreation(user,groupName):
    print(groupName)
    if groupName[:4]=='http':
        addgroup=groupName.split('/')[-1]
        print(addgroup)
        path=f".\database\{addgroup}\groupaccess.csv"
        print(path)
        groupname=""
        with open(path,'r') as f:
            gName=f.read()
            print(gName)
            gName=gName.split(',')[1]
            gName=gName.split('\n')[0]
            groupname=gName
            f.close()
        print(groupname)
        with open(path,'a') as f:
            f.write(f"{user}\n")
            print("writen")
            f.close()
        with open(f"./database/{user}.csv",'a') as f:
            f.write(f"{addgroup},{groupname}\n")
            print("userfile_edited")
            f.close()

        
    else:
        code=generateCode()
        groupNameC=f"{user}-{code}"
        path=f'.\database\{groupNameC}'
        os.mkdir(path)
        print('created group..')
        accessPath=f"{path}\groupaccess.csv"
        print(accessPath)
        with open(accessPath,'w') as access:
            access.write(f'{groupNameC},{groupName}\n{user}\n')
            access.close()
        print('created group..')

        path=f'.\database\{user}.csv'
        with open(path,'a') as addgroup:
            addgroup.write(f'{groupNameC},{groupName}\n')
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
    try:
        path=f'.\database\{user}.csv'
        print(path)
        with open(path,'r') as a:
            d=a.read()
            print(d)
            if d=="":
                d="empty"
            client.send(d.encode())
            
        print("send")
    except:
        pass
def retrive(groupid):
    print("entered")
    path=f"./database/{groupid}"
    print(path)
    stream=""
    list=os.listdir(path)[1:]
    for i in list:
        i=i.split('.')[0]
        stream+=f"{i},"
    print(list)
    
    if stream=="":
        stream='empty'
    print(stream)
    client.send(stream.encode())
    print("send test details")
def community(groupid):
    path=f"./database/{groupid}/groupaccess.csv"
    with open(path,'r') as f:
        accessControl=f.read()
        client.send(accessControl.encode())
        print(accessControl)
        f.close()
def paper(contents):
    contents=contents.split(',')
    print(contents)
    path=f"./database/{contents[-2]}/{contents[0]}.txt"
    print(path)
    with open(path,'w') as f:
        f.write(f"{contents[1]}\n{contents[2]}\n{contents[3]}")
        print(f"{contents[1]}\n{contents[2]}\n{contents[3]}")
        f.close()
    print("done..")
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
                if command[0] == 'retrive':
                    retrive(command[1])
                if command[0] =="community":
                    community(command[1])
                if command[0] == 'paper':
                    paper(command[1])

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
