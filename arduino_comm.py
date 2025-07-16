import serial
import time

def send_to_arduino(porta, comandos):
    ser = serial.Serial(porta, 115200)
    time.sleep(2)
    for x, y, estado in comandos:
        if estado == 'move':
            ser.write(b'U\n')
        elif estado == 'draw':
            ser.write(b'D\n')
        ser.write(f"G X{round(x, 2)} Y{round(y, 2)}\n".encode())
        time.sleep(0.02)
    ser.write(b'U\n')
    ser.close()
