import serial  # A module for accessing the serial port, used to communicate with the GSM modem.
import time
from random import randint  # Simulates temperature reading

def read_temperature():  # Simulate temperature reading
    return randint(20, 30)

def send_sms(ser, recipient, message): # Sends an SMS to the specified recipient with the given message
    ser.write(b'AT+CMGF=1\r')  # This AT command sets the GSM modem to SMS text mode.
    time.sleep(1)
    ser.write(f'AT+CMGS="{recipient}"\r'.encode())  # Prepares the modem to send an SMS to the specified recipient number.
    time.sleep(1)
    ser.write(f'{message}\r'.encode())
    ser.write(b'\x1A')  # Send SMS (Ctrl+Z), The Ctrl+Z (ASCII 26) is used to indicate the end of the message and send it
    time.sleep(3)

def check_for_sms(ser):  # Checks the GSM modem for incoming SMS messages.
    ser.write(b'AT+CMGF=1\r')  # Set SMS mode to text
    time.sleep(1)
    ser.write(b'AT+CMGL="ALL"\r')  # Lists all SMS messages stored on the GSM modem.
    time.sleep(1)
    messages = ser.readlines()  # Reads all incoming messages.
    for msg in messages:
        if "TEMP_REQUEST" in msg.decode():
            return True
    return False
    # If a message contains the keyword "TEMP_REQUEST", the function returns True, indicating that the server is requesting temperature data.

def main():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Replace with your GSM modem's port
    #  Initializes the serial connection with the GSM modem on the specified port and baud rate (9600 in this case).
    time.sleep(2)

    while True:
        if check_for_sms(ser):
            temperature = read_temperature()
            send_sms(ser, "+1234567890", f"Current temperature: {temperature}°C")  # Replace with server's number
        time.sleep(10)
    #  Adds a delay between checks to avoid overwhelming the GSM modem with requests.

if __name__ == "__main__":
    main()

# End of the client.py file