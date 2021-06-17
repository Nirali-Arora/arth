# 𝘾𝙧𝙚𝙖𝙩𝙞𝙣𝙜 𝙡𝙞𝙫𝙚 𝙨𝙩𝙧𝙚𝙖𝙢𝙞𝙣𝙜 𝙫𝙞𝙙𝙚𝙤 𝙘𝙝𝙖𝙩 𝙪𝙨𝙞𝙣𝙜 𝙤𝙥𝙚𝙣𝙘𝙫- Server Side

# Socket(Server)

import socket
import numpy as np
import cv2 as cv
import threading

skt = socket.socket()
skt.bind(("", 7090))
skt.listen()
session, address = skt.accept() #accepting request from any server
print(session.recv(2046)) 
cameraIndex = 'http://192.168.43.1:8080/video' # using camera from IPCamera App
camera = cv.VideoCapture(cameraIndex) # starting camera

def sender():
    while True:
        status, photo = camera.read()
        photo = cv.resize(photo, (640, 480))
        print(photo.shape)
        if status:
            session.send(np.ndarray.tobytes(photo))
        else: print("Could not get frame")

def receiver():
    framesLost = 0
    print("Entered")
    while True:
        framesLost += 1
        data = session.recv(100000000)
        if(data == b'finished'):
            print("Finished")
            camera.release()
            session.close()
        else:
            photo =  np.frombuffer(data, dtype=np.uint8)
            if len(photo) == 640*480*3:
                cv.imshow('From Client', photo.reshape(480, 640, 3))
                if cv.waitKey(1) == 13:
                    session.send(b'finished')
                    camera.release()
                    cv.destroyAllWindows()
                    break
            else:
                print("Lost {} frames".format(framesLost) )
                
threading.Thread(target=sender).start()
threading.Thread(target=receiver).start()