import serial
import time
import hmac
import hashlib
from cryptography.fernet import Fernet
from random import randint

# Secret keys for HMAC and Fernet (should be securely shared)
HMAC_KEY = b'secret_hmac_key'  # Must be the same on both server and client
FERNET_KEY = Fernet.generate_key()  # Use the same key for both server and client
cipher = Fernet(FERNET_KEY)

def read_temperature():
    return randint(20, 30)

def send_sms(ser, recipient, message):
    ser.write(b'AT+CMGF=1\r')
    time.sleep(1)
    ser.write(f'AT+CMGS="{recipient}"\r'.encode())
    time.sleep(1)
    ser.write(f'{message}\r'.encode())
    ser.write(b'\x1A')  # Send SMS (Ctrl+Z)
    time.sleep(3)

def generate_hmac(message):
    return hmac.new(HMAC_KEY, message, hashlib.sha256).digest()

def check_for_sms(ser):
    ser.write(b'AT+CMGF=1\r')
    time.sleep(1)
    ser.write(b'AT+CMGL="ALL"\r')
    time.sleep(1)
    messages = ser.readlines()
    for msg in messages:
        if "TEMP_REQUEST" in msg.decode():
            return True
    return False

def main():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(2)

    while True:
        if check_for_sms(ser):
            temperature = read_temperature()
            data = f"Current temperature: {temperature}°C".encode()

            # Encrypt the data
            encrypted_data = cipher.encrypt(data)

            # Generate HMAC
            hmac_value = generate_hmac(encrypted_data)

            # Combine encrypted data with HMAC (separated by ':')
            message_to_send = f"{encrypted_data.decode()}:{hmac_value.hex()}"

            # Send the combined message
            send_sms(ser, "+1234567890", message_to_send)  # Replace with server's number
        time.sleep(10)

if __name__ == "__main__":
    main()
