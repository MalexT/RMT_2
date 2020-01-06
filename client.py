from socket import *
from time import sleep
from threading import *
import getpass
import sys
import os

class ListenThread(Thread):
    def __init__(self, sock):
        self.sock = sock
        # Calling a constructor of 'Thread' class
        super().__init__()
        # self.start() essentially runs the run() method below
        self.start()

    def run(self):
        # Prihvata odgovore od servera
        while True:
            try:
                odg = self.sock.recv(4096).decode()
                print(odg)
            except:
                self.sock.close()
                print("Greska sa serverom, iskljucite app")
                sys.exit(1)
                break

# Static vars
srv_address = 'localhost'
srv_port = 6969

# Uspostavi konekciju sa serverom
while True:
    try:
        # Napravi soket
        sock = socket(AF_INET, SOCK_STREAM)
        # Povezi se sa serverom
        sock.connect( (srv_address, srv_port) )
        # Posalji username pass i premium (ne znam sta sa tim jos uvek)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n\t\tDobrodosli!\n")
        izbor = input("Registracija/Login (izaberite opciju)\nreg/log : ")
        sock.send(izbor.encode())

        if izbor == "reg":
            username = input('Enter your username: ')
            sock.send(username.encode())
            # password = input('Enter your password: ')
            password = getpass.getpass("Enter your password: ") #Da lozinka bude bar malo sakrivena
            sock.send(password.encode())
            premium = input('Are you premium user?(y/n): ')
            sock.send(premium.encode())

        if izbor == "log":
            username = input('Enter your username: ')
            sock.send(username.encode())
            # password = input('Enter your password: ')
            password = getpass.getpass("Enter your password: ") #Da lozinka bude bar malo sakrivena
            sock.send(password.encode())
            premium = input('Quick check you are premium?(y/n): ') #ubaci cheeky proveru za ovaj deo
            sock.send(premium.encode())

        # Inicijalizuj listenera
        listener = ListenThread(sock)
        # Povezali smo se stoga mozemo izaci loopa
        break
    except:
        print('Unable to connect to the server')
        print('Retrying in 3 seconds...')
        # Ne radi nista 3 sekundi pa pokusamo opet
        sleep(3)

# Glavni loop za komande
while True:
    # Uhvati komandu
    # Posalji je serveru
    try:
        message = input()
        sock.send(message.encode())
    except:
        print("Ne moze da se posalje komanda serveru.")
        break
    

