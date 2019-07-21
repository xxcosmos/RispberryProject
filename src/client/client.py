import io
import socket
import struct
import time
import threading
import picamera
import wiringpi

# GPIO 管脚
right_front = 1
left_front = 6
right_back = 5
left_back = 4

# 指令
FORWARD = "forward"
BACKWARD = "backward"
LEFT = "left"
RIGHT = "right"
STOP = "stop"
SUB_SPEED = 'sub'
ADD_SPEED = 'add'
PAUSE = 'start'

# 初始变量
speed = 10
direction = FORWARD
movement = STOP
is_video_transmit = False


# 指令处理函数
def instruction_handler(ins):
    global direction, movement, is_video_transmit
    if ins == FORWARD:
        movement = FORWARD
        direction = FORWARD
        Car.forward()
    elif ins == STOP:
        movement = STOP
        Car.stop()
    elif ins == BACKWARD:
        movement = BACKWARD
        direction = BACKWARD
        Car.backward()
    elif ins == RIGHT:
        movement = RIGHT
        Car.right()
    elif ins == LEFT:
        movement = LEFT
        Car.left()
    elif ins == ADD_SPEED:
        Car.add_speed()
    elif ins == SUB_SPEED:
        Car.sub_speed()
    elif ins == PAUSE:
        if not is_video_transmit:
            CamThreading('192.168.1.241', 8080).start()
        is_video_transmit = not is_video_transmit
    else:
        Car.stop()


# 初始化
def init():
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
    Car.stop()


# 小车类
class Car(object):

    @staticmethod
    def stop():
        wiringpi.softPwmWrite(left_back, 0)
        wiringpi.softPwmWrite(right_back, 0)
        wiringpi.softPwmWrite(left_front, 0)
        wiringpi.softPwmWrite(right_front, 0)

    @staticmethod
    def forward():
        Car.stop()
        wiringpi.softPwmWrite(right_front, speed)
        wiringpi.softPwmWrite(left_front, speed)

    @staticmethod
    def backward():
        Car.stop()
        wiringpi.softPwmWrite(left_back, speed)
        wiringpi.softPwmWrite(right_back, speed)

    @staticmethod
    def right():
        Car.stop()
        if direction == FORWARD:
            wiringpi.softPwmWrite(left_front, speed)
        elif direction == BACKWARD:
            wiringpi.softPwmWrite(left_back, speed)

    @staticmethod
    def left():
        Car.stop()
        if direction == FORWARD:
            wiringpi.softPwmWrite(right_front, speed)
        elif direction == BACKWARD:
            wiringpi.softPwmWrite(right_back, speed)

    @staticmethod
    def add_speed():
        global speed, movement
        if speed + 10 <= 100:
            speed += 10
            instruction_handler(movement)
        print("speed now is ", speed)

    @staticmethod
    def sub_speed():
        global speed
        if speed - 10 >= 0:
            speed -= 10
            instruction_handler(movement)
        print("speed now is ", speed)


# 视频传输线程
class CamThreading(threading.Thread):
    # 初始化
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        # 服务端建立视频传输 socket
        time.sleep(1)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        print("连接成功")
        self.connection = self.socket.makefile('wb')

    def run(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (320 * 2, 240 * 2)
            camera.framerate = 15
            time.sleep(2)
            stream = io.BytesIO()

            for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                self.connection.write(struct.pack('<L', stream.tell()))
                self.connection.flush()
                stream.seek(0)
                self.connection.write(stream.read())
                stream.seek(0)
                stream.truncate()
                if not is_video_transmit:
                    break
        self.connection.write(struct.pack('<L', 0))
        # 关闭资源
        camera.close()
        self.connection.close()
        self.socket.close()


# 接收指令线程
class CarThreading(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        # 建立 socket 连接
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(5)

    def run(self):
        while True:
            connection, address = self.socket.accept()
            ins = connection.recv(1024).decode('utf-8')
            print('Instruction:', ins)
            instruction_handler(ins)
            connection.close()


if __name__ == '__main__':
    init()
    CarThreading('192.168.1.207', 8081).start()
