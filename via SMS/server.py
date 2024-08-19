import serial
import time

# Same explanation as client.py
def send_sms(ser, recipient, message):
    ser.write(b'AT+CMGF=1\r')  # Set SMS mode to text
    time.sleep(1)
    ser.write(f'AT+CMGS="{recipient}"\r'.encode())
    time.sleep(1)
    ser.write(f'{message}\r'.encode())
    ser.write(b'\x1A')  # Send SMS (Ctrl+Z)
    time.sleep(3)

def read_sms(ser):
    ser.write(b'AT+CMGF=1\r')  # Set SMS mode to text
    time.sleep(1)
    ser.write(b'AT+CMGL="ALL"\r')  # List all SMS
    time.sleep(1)
    messages = ser.readlines()
    for msg in messages:
        if "Current temperature" in msg.decode():
            return msg.decode().strip()
    return None

def main():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Replace with your GSM modem's port
    time.sleep(2)

    send_sms(ser, "+0987654321", "TEMP_REQUEST")  # Replace with edge device's number

    while True:
        response = read_sms(ser)
        if response:
            print(f"Received data from edge device: {response}")
            break
        time.sleep(10)

if __name__ == "__main__":
    main()

# End of server.py