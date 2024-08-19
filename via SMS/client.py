import serial
import time
from random import randint  # Simulates temperature reading

def read_temperature():
    # Simulate temperature reading
    return randint(20, 30)

def send_sms(ser, recipient, message):
    ser.write(b'AT+CMGF=1\r')  # Set SMS mode to text
    time.sleep(1)
    ser.write(f'AT+CMGS="{recipient}"\r'.encode())
    time.sleep(1)
    ser.write(f'{message}\r'.encode())
    ser.write(b'\x1A')  # Send SMS (Ctrl+Z)
    time.sleep(3)

def check_for_sms(ser):
    ser.write(b'AT+CMGF=1\r')  # Set SMS mode to text
    time.sleep(1)
    ser.write(b'AT+CMGL="ALL"\r')  # List all SMS
    time.sleep(1)
    messages = ser.readlines()
    for msg in messages:
        if "TEMP_REQUEST" in msg.decode():
            return True
    return False

def main():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Replace with your GSM modem's port
    time.sleep(2)

    while True:
        if check_for_sms(ser):
            temperature = read_temperature()
            send_sms(ser, "+1234567890", f"Current temperature: {temperature}°C")  # Replace with server's number
        time.sleep(10)

if __name__ == "__main__":
    main()
