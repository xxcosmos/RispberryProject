import io
import socket
import struct
import time
import threading
import picamera
import wiringpi

# GPIO 管脚
right_front = 1
left_front = 29
right_back = 5
left_back = 4

forward = "forward"
backward = "backward"
left = "left"
right = "right"
stop = "stop"
sub = 'sub'
add = 'add'

speed = 10
instruction = forward


def instruction_handler(instruction, car):
    if instruction == forward:
        car.forward()
    elif instruction == stop:
        car.stop()
    elif instruction == backward:
        car.backward()
    elif instruction == right:
        car.right()
    elif instruction == left:
        car.left()
    elif instruction == add:
        pass
    elif instruction == sub:
        car.sub_speed()
    else:
        car.stop()


"""
    小车类
"""


class Car(object):
    def __init__(self):
        wiringpi.wiringPiSetup()
        wiringpi.pinMode(left_back, 1)
        wiringpi.pinMode(left_front, 1)
        wiringpi.pinMode(right_back, 1)
        wiringpi.pinMode(right_front, 1)
        wiringpi.pwmSetClock(2)
        wiringpi.softPwmCreate(left_front, 0, 200)
        wiringpi.softPwmCreate(right_front, 0, 200)
        wiringpi.softPwmCreate(left_back, 0, 200)
        wiringpi.softPwmCreate(right_back, 0, 200)
        self.stop()

    def stop(self):
        wiringpi.softPwmWrite(left_back, 0)
        wiringpi.softPwmWrite(right_back, 0)
        wiringpi.softPwmWrite(left_front, 0)
        wiringpi.softPwmWrite(right_front, 0)

    def forward(self):
        self.stop()
        wiringpi.softPwmWrite(right_front, speed)
        wiringpi.softPwmWrite(left_front, speed)

    def backward(self):
        self.stop()
        wiringpi.softPwmWrite(left_back, speed)
        wiringpi.softPwmWrite(right_back, speed)

    def right(self):
        if instruction == forward:
            self.stop()
            wiringpi.softPwmWrite(left_front, speed)
        elif instruction == backward:
            self.stop()
            wiringpi.softPwmWrite(left_back, speed)

    def left(self):
        if instruction == forward:
            self.stop()
            wiringpi.softPwmWrite(right_front, speed)
        elif instruction == backward:
            self.stop()
            wiringpi.softPwmWrite(right_back, speed)

    def add_speed(self):
        global speed
        if speed + 10 <= 100:
            speed += 10
            instruction_handler(instruction,self)
    def sub_speed(self):
        global speed
        if speed - 10 >= 0:
            speed -= 10
            instruction_handler(instruction,self)


"""
    视频传输线程
"""


class CamThreading(threading.Thread):
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection

    def run(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (320 * 2, 240 * 2)
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
        camera.close()


"""
    小车运动线程
"""


class CarThreading(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        car = Car()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('192.168.12.1', 8080))
        server_socket.listen(5)
        while True:
            connection, address = server_socket.accept()
            rec_msg = connection.recv(1024).decode('utf-8')

            print(rec_msg)
            instruction_handler(rec_msg,car)
            global instruction
            instruction = rec_msg
            connection.close()


if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.12.128', 8888))
    connection = client_socket.makefile('wb')

    cam_threading = CamThreading(connection)
    cam_threading.start()

    car_threading = CarThreading()
    car_threading.start()
