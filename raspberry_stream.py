import io
import socket
import struct
from picamera import PiCamera
from time import sleep

# IP address of your PC
server_ip = '192.168.2.1'
server_port = 8000

# Establish socket connection
client_socket = socket.socket()
client_socket.connect((server_ip, server_port))

try:
    with PiCamera() as camera:
        camera.resolution = (640, 480)
        # Camera warm-up time
        sleep(2)
        
        stream = io.BytesIO()
        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            # Send image size
            client_socket.sendall(struct.pack('<L', stream.tell()))
            client_socket.sendall(stream.getvalue())
            
            # Reset stream for next frame
            stream.seek(0)
            stream.truncate()

except Exception as e:
    print(f"Error: {e}")
finally:
    client_socket.close()
