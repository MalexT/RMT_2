from socket import *
from threading import *
import json
import os
import shutil #da bi lakse koristili move
import csv
import os.path

class ClientHandler(Thread):
    def __init__(self, cl_sock, cl_address, cl_username, cl_password):
        self.sock = cl_sock
        self.address = cl_address
        self.username = cl_username
        self.password = cl_password
        self.premium = cl_premium 
        self.izbor = cl_izbor
        self.cwd = "/"
        
        # Calling a constructor of 'Thread' class
        super().__init__()
        # self.start() essentially runs the run() method below
        self.start()

    def run(self):
        print('<{}> has connected!'.format(self.username))
        if self.izbor == "reg":

            with open('C:/Users/Aleksa/Desktop/RMT2/vise_korisnika/korisnici.csv', mode='a', newline='') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow([self.username,self.password,self.premium])
            try:
                os.mkdir("./" + self.username)
            except OSError:
                client.sock.send("Nije mogao da se napravi dir..".encode())

            listToStr = ' '.join(map(str, os.listdir("./" + self.username + self.cwd))) 
            if listToStr == "":
                client.sock.send("Nemate dokumente na drajvu.".encode())
            else:
                client.sock.send(listToStr.encode())

            if self.premium == "y":
            #Da posalje poruku dobrodoslice
                client.sock.send("\n\n\t\tDobrodosli\nKomande za premium korisnika\n OTVF - otvori folder\n ZATF - zatvori folder,\n UP - upload fajla,\n NF - Novi folder,\n RN - Promena naziva foldera,\n OF - Obrisati folder,\n MV - Prebaciti fajl iz jednog foldera u drugi,\n Deli - Generise link za deljenje diska\n\n".encode()) 
            if self. premium == "n":
                client.sock.send("\n\n\t\tDobrodosli\nKomande za obicnog korisnika\n OTVF - otvori folder\n ZATF - zatvori folder\n UP - upload fajla\n DL - download fajla\n\n".encode())

        login = False
        if self.izbor == "log":
           with open('korisnici.csv', 'rt') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    if row[0] == cl_username and row[1] == cl_password:
                        client.sock.send("Login je uspesan!".encode())
                        login = True
                        break #bitan je
                if login == False:
                    client.sock.send("Uneli ste pogresne parametre molimo vas ponovo pokrenite aplikaciju!".encode())

        #izlista direktorijum za svakog korisnika
        if login == True:
            if self.premium == "y":
            #Da posalje poruku dobrodoslice
                client.sock.send("\n\n\t\tDobrodosli\n\nKomande za premium korisnika\n OTVF - otvori folder\n ZATF - zatvori folder\n NF - Novi folder,\n RN - Promena naziva foldera,\n OF - Obrisati folder,\n MV - Prebaciti fajl iz jednog foldera u drugi\n\n".encode()) 
            if self. premium == "n":
                client.sock.send("\n\n\t\tDobrodosli\n\nKomande za obicnog korisnika\n OTVF - otvori folder\n ZATF - zatvori folder\n\n".encode())
            listToStr = ' '.join(map(str, os.listdir("./" + self.username + self.cwd))) 
            if listToStr == "":
                client.sock.send("Nemate dokumente na drajvu.".encode())
            else:
                client.sock.send(listToStr.encode())

        while True:
                try:
                        text = self.sock.recv(4096).decode()
                        if text == "NF":
                            try:
                                client.sock.send("\nUnesite ime direktorijuma: ".encode())
                                ime = cl_sock.recv(4096).decode()
                                os.mkdir(self.username+self.cwd+ime+"/") #dodavanje direktorijuma
                            except OSError:
                                client.sock.send("\nDoslo je do greske prilikom kreiranja direktorijuma ".encode())
                            
                        if text == "RN": #radi
                            try:
                                client.sock.send("\nUnesite starog ime direktorijuma: ".encode())
                                staro_ime = cl_sock.recv(4096).decode()
                                client.sock.send("\nUnesite novo ime direktorijuma: ".encode())
                                novo_ime = cl_sock.recv(4096).decode()
                                os.rename(self.username+"/"+staro_ime+"/",self.username+"/"+novo_ime+"/")
                            except OSError:
                                client.sock.send("\nGreska prilikom preimenovanja foldera ".encode())
                        
                        if text =="OF":
                            client.sock.send("\nUnesite ime direktorijuma za brisanje (folder mora da bude prazan, da bi ga obrisali): ".encode())
                            obrisati = cl_sock.recv(4096).decode()
                            try:
                                os.rmdir(self.username+"/"+obrisati+"/")
                            except OSError:
                                client.sock.send("\nPAZLJIVO FOLDER NIJE PRAZAN".encode())                
                        
                        if text == "MV":
                            client.sock.send("\nUnesite ime fajla koji hocete da premestite: ".encode())
                            ime_fajla = cl_sock.recv(4096).decode()
                            # client.sock.send("\nUnesite iz kog foldera zelite da prebacite: ".encode())
                            # pocetak = cl_sock.recv(4096).decode()
                            client.sock.send("\nUnesite u koji folder zelite da prebacite: ".encode())
                            odrediste = cl_sock.recv(4096).decode()
                            try:
                                # shutil.move(self.cwd+odrediste,self.cwd+pocetak)
                                os.path.join("/slika", os.path.basename(ime_fajla))
                                posle_movea = "/Users/Aleksa/Desktop/rmt2/vise_korisnika/"+odrediste
                                listToStr = ' '.join(map(str, os.listdir(posle_movea)))
                                client.sock.send(listToStr.encode())
                            except:
                                client.sock.send("\nGreska prilikom premestanja fajla\n".encode())
                    
                        if text == "OTVF":
                            client.sock.send("\nUnesite ime foldera koji hocete da otvorite: ".encode())
                            otvf = cl_sock.recv(4096).decode()
                            self.cwd = "/" + otvf

                        if text == "ZATF":
                            client.sock.send("\nUnesite ime foldera koji hocete da zatvorite: ".encode())
                            zatf = cl_sock.recv(4096).decode()
                            self.cwd = "/"

                        if text == "Deli":
                            try:
                                posalji="./"+self.username+"/"
                                client.sock.send(posalji.encode())
                            except:
                                client.sock.send("Greska prilikom generisanja linka za deljenje".encode())
                            

                        listToStr = ' '.join(map(str, os.listdir("./" + self.username + self.cwd))) 
                        client.sock.send(listToStr.encode())
                    
                except:
                    dc_message = 'User {} has disconnected'.format(self.username)
                    print(dc_message)
                    self.sock.close()
                    break

# konstante
srv_address = 'localhost'
srv_port = 6969

# Slusaj za konekcije

# Napravi soket
srv_sock = socket(AF_INET, SOCK_STREAM)
# Bind soket za adresu i port
srv_sock.bind( (srv_address, srv_port) )
# Slusaj za konekciju
srv_sock.listen(5)
print('Server is ready to accept new connections!')

# Accept new connections
while True:
    # Get the client socket and client address when accepting the connection
    cl_sock, cl_address = srv_sock.accept()
    try:
        cl_izbor = cl_sock.recv(4096).decode()
        # We wait for the client to send us his/her username
        cl_username = cl_sock.recv(4096).decode()
        # Waiting for the client to send his/her passwrod
        cl_password = cl_sock.recv(4096).decode()
        # Evo ne znam sta da radim sa ovim...
        cl_premium = cl_sock.recv(4096).decode()

        # We initialize the ClientThread class defined above
        client = ClientHandler(cl_sock, cl_address, cl_username, cl_password)
    except:
        print("Klijent je prekinuo komunikaciju")