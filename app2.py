import cv2
from flask import Flask, render_template, Response, redirect, url_for
import os
from roboflow import Roboflow
import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BOARD)

# Define the GPIO pin connected to the servo
servo_pin1 = 18
servo_pin2 = 22

# Set the GPIO pin as an output
GPIO.setup(servo_pin1, GPIO.OUT)
GPIO.setup(servo_pin2, GPIO.OUT)

# Create a PWM object with a frequency of 50 Hz
servo1 = GPIO.PWM(servo_pin1, 50)
servo2 = GPIO.PWM(servo_pin2, 50)

# Start the PWM with a duty cycle of 7.5% (neutral position)
servo1.start(7.5)
servo2.start(7.5)

f=0

rf = Roboflow(api_key="2crErPrBo6lHZZgyWJ7F")
project = rf.workspace().project("crack-btlnb")
model = project.version(4).model

video = cv2.VideoCapture(0)
app = Flask(__name__)

cnt = 0

def camera():
    success, frame = video.read()
    return frame

def capture_and_predict():
    global cnt
    cnt = cnt + 1
    frame = camera()
    path1 = 'E:/pipe inspection video streaming/Images'
    path2= "E:\pipe inspection video streaming\predictions"
    cv2.imwrite(os.path.join(path1, f"{cnt}.jpg"), frame)
    print(model.predict(os.path.join(path1, f"{cnt}.jpg")).json())
    model.predict(os.path.join(path1, f"{cnt}.jpg")).save(os.path.join(path2, "prediction"+f"{cnt}.jpg"))

def video_stream():
    while True:
        ret, frame = video.read()
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpeg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('camera.html')

@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def capture():
    f=1
    while f==1:
        servo2.ChangeDutyCycle(2.5)
        time.sleep(6)
        print("Clicking Image")
        #Click Picture
        capture_and_predict()

        servo2.ChangeDutyCycle(7.5)
        time.sleep(1)


        servo1.ChangeDutyCycle(2.5)
        time.sleep(6)
        print("Clicking Image")
        #Click picture
        capture_and_predict()

        servo1.ChangeDutyCycle(7.5)
        time.sleep(1)

        servo2.ChangeDutyCycle(12.5)
        time.sleep(6)
        print("Clicking Image")
        #Click picture
        capture_and_predict()

        servo2.ChangeDutyCycle(7.5)
        time.sleep(1)

        servo1.ChangeDutyCycle(12.5)
        time.sleep(6)
        print("Clicking Image")
        #Click Picture
        capture_and_predict()

        servo1.ChangeDutyCycle(7.5)
        time.sleep(1)
        f=0        
    return redirect(url_for('index'))  # 'index' is the function name, not the URL path

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)