import cv2
import socket
import struct
import numpy as np

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen()

conn, addr = server_socket.accept()
data = b""
payload_size = struct.calcsize("<L")

while True:
    while len(data) < payload_size:
        data += conn.recv(4096)
        
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("<L", packed_msg_size)[0]
    
    while len(data) < msg_size:
        data += conn.recv(4096)
    
    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Convert image bytes to OpenCV format
    frame = cv2.imdecode(np.frombuffer(frame_data, dtype='uint8'), cv2.IMREAD_COLOR)
    
    # Here, you can process the frame with YOLOv8
    # ...

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
