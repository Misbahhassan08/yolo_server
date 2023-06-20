import os
from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO,emit,send
from flask_cors import CORS, cross_origin
import datetime
import base64
import serial
import threading
import cv2
import shutil
import time
import json 
import requests
from config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app, cors_allowed_origins='*')
clients = 0
CORS(app)
app.app_context().push()
#Send data to client
_thread = False
deviceStart = False
obj = {}


class Camera(threading.Thread):
    
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.create_directory()
        self.camera1 = cv2.VideoCapture(0)
        self.camera2 = cv2.VideoCapture(1)
        self.net = sock
        self.cam1_frame = None 
        self.cam2_frame = None
        self.frame_size = (240,180)
        #self.getTime = self.db.fetch_time()
        self.ImageCount = 0
        self.obj_json = {}

        pass # end of __init__ function


    def rename_directory(self, orderId):
        folderName = ""+tempFolder+"/"+self.trasID+"/"
        folderPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Images/" + folderName)
        if not os.path.exists(folderPath):
            #os.makedirs(folderPath)
            print(f"No folder Exist with Name/Path : {folderPath}")
            pass 
        else: 
            folderName = ""+tempFolder+"/"
            folderPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Images/" + folderName)
            os.rename(f"{folderPath}{str(self.trasID)}",f"{folderPath}{str(orderId)}")
        pass # end of create directory function

    def create_directory(self):
        folderPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Images/" + tempFolder)
        if not os.path.exists(folderPath):
            print('making Parent directory ')
            os.makedirs(folderPath)
        pass # end of create directory function

    def state_page(self, state):
        self.page_start = state

    def reset_vals(self):
        self.ImageCount = 0
        self.obj_json = {}
        self.wImageCount = 0

    def getUniqueID(self):
        _time = int(time.time())
        id = f"{self.PIID}{_time}"
        self.trasID = id
        return int(id)

    def stop_process(self):
        self.is_running = False
        self.join()
        pass # end of stop_process function

    def streaming_Data(self,frame1 = None, frame2 = None):
        global url, headers
        
        bc = False
        encode_frame_1 = None
        encode_frame_2 = None
        barcode_data = {}
        barcode_detect = False
        payload={}
        img1 = {}
        img2 = {}

        if frame1 is not None:
            retval, buffer = cv2.imencode('.png', frame1)
            encode_frame_1 = buffer.tobytes()
            img_b64 = base64.b64encode(encode_frame_1)
            img_b64s_1 = img_b64.decode('utf-8')
            img1 = {'img':img_b64s_1}

        if frame2 is not None:
            retval, buffer = cv2.imencode('.png', frame2)
            encode_frame_2 = buffer.tobytes()
            img_b64 = base64.b64encode(encode_frame_2)
            img_b64s_2 = img_b64.decode('utf-8')
            img2 = {'img':img_b64s_2}


        _json = [
            {"cam_1":encode_frame_1},{"cam_2":encode_frame_2}
        ]
        self.net.emit('ControllerData', _json )
        pass


    def run(self):
        if True:#try:
            while True:
                image1_ret, image1 = self.camera1.read()
                image2_ret, image2 = self.camera2.read()
                if image1_ret:
                    frame = cv2.resize(image1, self.frame_size)
                    self.cam1_frame = frame
                    #cv2.imshow("Camera 1", self.cam1_frame)
                if image2_ret:
                    frame = cv2.resize(image2, self.frame_size)
                    self.cam2_frame = frame
                    #cv2.imshow("Camera 2", self.cam2_frame)


                self.streaming_Data(self.cam1_frame, self.cam2_frame)
                            
                cv2.waitKey(1)
        #except Exception as error:
        #    print(f"Error Found : {error}")
        self.camera1.release()
        self.camera2.release()
        pass # end of run function 
    pass # end of class Camera 
    
obj = Camera(socketio)
active = False

@socketio.on("dashboard_active_now")
def dashboard_active_now():
    global obj
    global active
    time.sleep(1)
    if active:
        obj.start()
    pass

@socketio.on("connect")
def define_connect_function():
    global active 
    print("Connect Call")
    active = True
    pass

@socketio.on('disconnect')
def test_disconnect():
    global clients
    global obj
    global active
    clients -= 1
    if active:
        obj.stop_process()
        active = False
    print('Client disconnected')
    



if __name__ == "__main__":
    socketio.run(app,debug=True, host="0.0.0.0", port=5000)
