import socket
from tkinter import *
from threading import Thread
import time
import os
from PIL import Image, ImageTk

pokeid = "000"
stats = [100,100,100,100,100,100,"Torche","","Garde Mystik","None",["NORMAL","NONE"]]
with open(os.path.join(os.path.dirname(__file__), "log.log")) as f:
    popo = f.read()
popo = popo.split("--Randomized Evolutions--")
    
popo = popo[1].split("--Pokemon Base Stats & Types--")
randomizedevo = popo[0]
    
popo = popo[1].split("--Removing Impossible Evolutions--")
randomizedpoke = popo[0]
    
popo = popo[1].split("--Move Data--")
popo = popo[1].split("--Pokemon Movesets--")
randomizedmovedata = popo[0]

popo = popo[1].split("--Trainers Pokemon--")
randomizedmoveset = popo[0]

randomizedmovedata = randomizedmovedata.replace(' ','').split('\n')[2:]
for i in range(0,len(randomizedmovedata)):
    randomizedmovedata[i] = randomizedmovedata[i].split('|')
randomizedmovedata = randomizedmovedata[:-2]

randomizedpoke = randomizedpoke.replace(' ','').split('\n')[1:-2]
for i in range(0,len(randomizedpoke)):
    randomizedpoke[i] = randomizedpoke[i].split('|')
    randomizedpoke[i][2] = randomizedpoke[i][2].split('/')
    if len(randomizedpoke[i][2]) == 1 :
        randomizedpoke[i][2] = [randomizedpoke[i][2][0],'NONE']
def getinfo(id):
    for i in range(0,len(randomizedpoke)):
        if randomizedpoke[i][0] == id:
            return randomizedpoke[i][3],randomizedpoke[i][4],randomizedpoke[i][5],randomizedpoke[i][6],randomizedpoke[i][7],randomizedpoke[i][8],randomizedpoke[i][9],randomizedpoke[i][10],randomizedpoke[i][11],randomizedpoke[i][1],randomizedpoke[i][2]

class SocketClient:
    def __init__(self):
        self.HOST, self.PORT = '127.0.0.1', 5000
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.HOST, self.PORT))
        server.listen(1)
        print("Listening on port", self.PORT)
        self.conn, self.addr = server.accept()
        print("Connected by", self.addr)

        self.threadsocket = Thread(target=self.socketthreadfunction, daemon=True)
        self.threadsocket.start()
    def socketthreadfunction(self):
        global stats,pokeid
        try:
            while True:
                data = self.conn.recv(1024)
                if not data:
                    print("Client disconnected")
                    break
                for line in data.decode().splitlines():
                    species_id = line.strip()
                    if int(species_id) == 0 or int(species_id) > 650: species_id = '0'
                    if not pokeid == species_id:
                        print("activation !")
                        pokeid = species_id
                        if int(pokeid) == 0:
                            stats= [100,100,100,100,100,100,"Torche","","Garde Mystik","None",["NONE","NONE"]]
                        else: stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],stats[6],stats[7],stats[8],stats[9],stats[10] = getinfo(pokeid)
                        print(stats)
        except OSError as e:
            print("Socket error:", e)
        finally:
            self.conn.close()

iluvsocks = SocketClient()
class ImageManager:
    def __init__(self, folder):
        self.folder = folder
        self.cache = {}
    def get(self, name,size1,size2):
        if name not in self.cache:
            path = os.path.join(self.folder, f"{name}.png")
            img = Image.open(path).resize((size1, size2), Image.LANCZOS)
            self.cache[name] = ImageTk.PhotoImage(img)
        return self.cache[name]

class IHM(Tk):
    
    def seuil(self,stat):
        if stat < 50:
            return "red"
        elif stat >= 50 and stat < 100:
            return "yellow"
        elif stat >= 100 and stat < 130:
            return "green"
        elif stat >= 130 and stat < 150:
            return "blue"
        elif stat >= 150:
            return "purple"
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.canvas = Canvas(self, width=600, height=400)
        self.canvas.pack()

        base = os.path.dirname(__file__)
        self.hpstat = self.canvas.create_text(110,100,text="100",font=("Minecraft",12,NORMAL))
        self.atkstat = self.canvas.create_text(110,150,text="100",font=("Minecraft",12,NORMAL))
        self.defensestat = self.canvas.create_text(110,200,text="100",font=("Minecraft",12,NORMAL))
        self.atkspestat = self.canvas.create_text(110,250,text="100",font=("Minecraft",12,NORMAL))
        self.defspestat = self.canvas.create_text(110,300,text="100",font=("Minecraft",12,NORMAL))
        self.spestat = self.canvas.create_text(110,350,text="100",font=("Minecraft",12,NORMAL))
        
        self.hp = self.canvas.create_text(17,100,text="HP",font=("Minecraft",15,NORMAL))
        self.atk = self.canvas.create_text(40,150,text="ATTACK",font=("Minecraft",15,NORMAL))
        self.defense = self.canvas.create_text(45,200,text="DEFENSE",font=("Minecraft",15,NORMAL))
        self.atkspe = self.canvas.create_text(35,250,text="SP.ATK",font=("Minecraft",15,NORMAL))
        self.defspe = self.canvas.create_text(35,300,text="SP.DEF",font=("Minecraft",15,NORMAL))
        self.spe = self.canvas.create_text(35,350,text="SPEED",font=("Minecraft",15,NORMAL))
        
        self.hpbar = self.canvas.create_line(125,100,stats[0]*1.11+140,100,fill=self.seuil(stats[0]),width=9)
        self.atkbar = self.canvas.create_line(125,150,stats[1]*1.27+140,150,fill=self.seuil(stats[1]),width=9)
        self.defbar = self.canvas.create_line(125,200,stats[2]*1.27+140,200,fill=self.seuil(stats[2]),width=9)
        self.atkspebar = self.canvas.create_line(125,250,stats[3]*1.27+140,250,fill=self.seuil(stats[3]),width=9)
        self.defspebar = self.canvas.create_line(125,300,stats[4]*1.27+140,300,fill=self.seuil(stats[4]),width=9)
        self.spebar = self.canvas.create_line(125,350,stats[5]*1.27+140,350,fill=self.seuil(stats[5]),width=9)
        self.abilitylab1 = self.canvas.create_text(585,250,text="1",font=("Minecraft",12,NORMAL))
        self.abilitylab2 = self.canvas.create_text(585,270,text="2",font=("Minecraft",12,NORMAL))
        self.abilitylab3 = self.canvas.create_text(575,290,text="HIDDEN",font=("Minecraft",12,NORMAL))
        self.ability1 = self.canvas.create_text(475,250,text="TALENT 1",font=("Minecraft",15,NORMAL))
        self.ability2 = self.canvas.create_text(475,270,text="TALENT 2",font=("Minecraft",15,NORMAL))
        self.ability3 = self.canvas.create_text(475,290,text="TALENT CACHE",font=("Minecraft",15,NORMAL))
        self.name = self.canvas.create_text(150,10,text="ARCEUS",font=("Minecraft",15,NORMAL),anchor='e',justify='left')
        self.img_mgr = ImageManager(os.path.join(base, "types"))
        self.img_mgr_id = ImageManager(os.path.join(base, "pokemon"))

        self.img1 = self.img_mgr.get(stats[10][1],128,64)
        self.img2 = self.img_mgr.get(stats[10][0],128,64)
        if len(pokeid) == 3 : temp=pokeid
        if len(pokeid) == 2 : temp='0' + pokeid
        if len(pokeid) == 1 : temp='00' + pokeid
        self.img3 = self.img_mgr_id.get(temp,200,200)

        self.id1 = self.canvas.create_image(530, 30, image=self.img1)
        self.id2 = self.canvas.create_image(400, 30, image=self.img2)
        self.id3 = self.canvas.create_image(475, 110, image=self.img3)
        
        
        
        self.canvas.images = [self.img1, self.img2, self.img3]

        self.thread = Thread(target=self.update_images, daemon=True)
        self.thread.start()

    def update_images(self):
        global stats , pokeid
        while True:
            self.canvas.itemconfig(self.hpstat,text=stats[0])
            self.canvas.itemconfig(self.atkstat,text=stats[1])
            self.canvas.itemconfig(self.defensestat,text=stats[2])
            self.canvas.itemconfig(self.atkspestat,text=stats[3])
            self.canvas.itemconfig(self.defspestat,text=stats[4])
            self.canvas.itemconfig(self.spestat,text=stats[5])
            self.canvas.itemconfig(self.ability1,text=stats[6])
            self.canvas.itemconfig(self.ability2,text=stats[7])
            self.canvas.itemconfig(self.ability3,text=stats[8])
            self.canvas.itemconfig(self.name,text=stats[9])
            self.canvas.coords(self.hpbar,125,100,int(stats[0])*1.11+140,100)
            self.canvas.coords(self.atkbar,125,150,int(stats[1])*1.27+140,150)
            self.canvas.coords(self.defbar,125,200,int(stats[2])*1.27+140,200)
            self.canvas.coords(self.atkspebar,125,250,int(stats[3])*1.27+140,250)
            self.canvas.coords(self.defspebar,125,300,int(stats[4])*1.27+140,300)
            self.canvas.coords(self.spebar,125,350,int(stats[5])*1.27+140,350)
            self.canvas.itemconfig(self.hpbar,fill=self.seuil(int(stats[0])))
            self.canvas.itemconfig(self.atkbar,fill=self.seuil(int(stats[1])))
            self.canvas.itemconfig(self.defbar,fill=self.seuil(int(stats[2])))
            self.canvas.itemconfig(self.atkspebar,fill=self.seuil(int(stats[3])))
            self.canvas.itemconfig(self.defspebar,fill=self.seuil(int(stats[4])))
            self.canvas.itemconfig(self.spebar,fill=self.seuil(int(stats[5])))
            img1 = self.img_mgr.get(stats[10][1],128,64)
            img2 = self.img_mgr.get(stats[10][0],128,64)
            if len(pokeid) == 3 : temp=pokeid
            if len(pokeid) == 2 : temp='0' + pokeid
            if len(pokeid) == 1 : temp='00' + pokeid
            img3 = self.img_mgr_id.get(temp,200,200)

            self.canvas.after(0, lambda img=img1: self.canvas.itemconfig(self.id1, image=img))
            self.canvas.after(0, lambda img=img2: self.canvas.itemconfig(self.id2, image=img))
            self.canvas.after(0, lambda img=img3: self.canvas.itemconfig(self.id3, image=img))
            self.canvas.images = [img1, img2, img3]

            time.sleep(2)


if __name__ == "__main__":
    app = IHM()
    app.mainloop()




'''
HOST, PORT = '127.0.0.1', 5000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print("Listening on port", PORT)
conn, addr = server.accept()
print("Connected by", addr)
with conn:
    while True:
        data = conn.recv(1024)
        if not data: break
        for line in data.decode().splitlines():
            species_id = int(line.strip())
            print("Enemy species ID:", species_id)
            # Add further logic here
            '''