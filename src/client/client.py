import io
import socket
import struct
import time
import threading
import picamera
import wiringpi


class Car(object):
    def __init__(self):
        wiringpi.wiringPiSetup()
        wiringpi.pinMode(1, 1)
        wiringpi.pinMode(4, 1)
        wiringpi.pinMode(5, 1)
        wiringpi.pinMode(6, 1)
        self.Stop()

    def Stop(self):
        wiringpi.digitalWrite(1, 0)
        wiringpi.digitalWrite(4, 0)
        wiringpi.digitalWrite(5, 0)
        wiringpi.digitalWrite(6, 0)

    def forward(self):
        wiringpi.digitalWrite(1, 0)
        wiringpi.digitalWrite(4, 1)
        wiringpi.digitalWrite(5, 1)
        wiringpi.digitalWrite(6, 0)

    def backward(self):
        wiringpi.digitalWrite(1, 1)
        wiringpi.digitalWrite(4, 0)
        wiringpi.digitalWrite(5, 0)
        wiringpi.digitalWrite(6, 1)

    def right(self):
        wiringpi.digitalWrite(1, 0)
        wiringpi.digitalWrite(4, 0)
        wiringpi.digitalWrite(5, 1)
        wiringpi.digitalWrite(6, 0)

    def left(self):
        wiringpi.digitalWrite(1, 0)
        wiringpi.digitalWrite(4, 1)
        wiringpi.digitalWrite(5, 0)
        wiringpi.digitalWrite(6, 0)


class CamThreading(threading.Thread):
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection

    def run(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (320, 240)
            camera.framerate = 15
            time.sleep(2)
            stream = io.BytesIO()

            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                self.connection.write(struct.pack('<L', stream.tell()))
                self.connection.flush()
                stream.seek(0)
                self.connection.write(stream.read())
                stream.seek(0)
                stream.truncate()
        self.connection.write(struct.pack('<L', 0))


class CarThreading(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        car = Car()
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_socket.bind(('192.168.12.1',8080))
        server_socket.listen(5)
        while True:
            connection ,address = server_socket.accept()
            rec_msg = connection.recv(1024).decode('utf-8')
            print(rec_msg)
            if rec_msg == "Forward":
                car.forward()
            elif rec_msg == "Stop":
                car.Stop()
            elif rec_msg == "Backward":
                car.backward()
            elif rec_msg == "Right":
                car.right()
            elif rec_msg == "Left":
                car.left()
            else:
                car.Stop()
            connection.close()


if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.12.128', 8888))
    connection = client_socket.makefile('wb')
    cam_threading = CamThreading(connection)
    cam_threading.start()
    car_threading = CarThreading()
    car_threading.start()
