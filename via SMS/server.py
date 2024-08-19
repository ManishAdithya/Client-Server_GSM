import serial
import time
import hmac
import hashlib
from cryptography.fernet import Fernet

# Secret keys for HMAC and Fernet (should be securely shared)
HMAC_KEY = b'secret_hmac_key'  # Must be the same on both server and client
FERNET_KEY = Fernet.generate_key()  # Use the same key for both server and client
cipher = Fernet(FERNET_KEY)

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
        if b"Current temperature" in msg:
            return msg.decode().strip()
    return None

def verify_hmac(message, hmac_to_verify):
    calculated_hmac = hmac.new(HMAC_KEY, message, hashlib.sha256).digest()
    return hmac.compare_digest(calculated_hmac, hmac_to_verify)

def main():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(2)

    send_sms(ser, "+0987654321", "TEMP_REQUEST")  # Replace with edge device's number

    while True:
        response = read_sms(ser)
        if response:
            # Split response into the encrypted message and the HMAC
            encrypted_message, received_hmac = response.split(':')
            encrypted_message = encrypted_message.encode()
            received_hmac = bytes.fromhex(received_hmac)

            if verify_hmac(encrypted_message, received_hmac):
                decrypted_message = cipher.decrypt(encrypted_message)
                print(f"Received data from edge device: {decrypted_message.decode()}")
            else:
                print("HMAC verification failed! Data integrity compromised.")
            break
        time.sleep(10)

if __name__ == "__main__":
    main()
