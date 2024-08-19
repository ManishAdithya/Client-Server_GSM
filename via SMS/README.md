# GSM Communication Using SMS

This document provides an explanation of the Python code used for communication between an edge device (client) and a server via GSM, using SMS to send and receive temperature data.

## `client.py` (Edge Device Code)

```python
import serial
import time
from random import randint
serial: A module for accessing the serial port, used to communicate with the GSM modem.
time: Provides various time-related functions, including delays.
randint: A function from the random module that generates random integers, used here to simulate temperature readings.
python
Copy code
def read_temperature():
    # Simulate temperature reading
    return randint(20, 30)
read_temperature: Simulates a temperature sensor by returning a random integer between 20 and 30. This function represents the temperature reading from the edge device.
python
Copy code
def send_sms(ser, recipient, message):
    ser.write(b'AT+CMGF=1\r')  # Set SMS mode to text
    time.sleep(1)
    ser.write(f'AT+CMGS="{recipient}"\r'.encode())
    time.sleep(1)
    ser.write(f'{message}\r'.encode())
    ser.write(b'\x1A')  # Send SMS (Ctrl+Z)
    time.sleep(3)
send_sms: Sends an SMS to the specified recipient with the given message.
AT+CMGF=1: This AT command sets the GSM modem to SMS text mode.
AT+CMGS: Prepares the modem to send an SMS to the specified recipient number.
message: The body of the SMS is sent after preparing the modem. The Ctrl+Z (ASCII 26) is used to indicate the end of the message and send it.
time.sleep(): Introduces delays to allow the GSM modem to process the commands properly.
python
Copy code
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
check_for_sms: Checks the GSM modem for incoming SMS messages.
AT+CMGL="ALL": Lists all SMS messages stored on the GSM modem.
ser.readlines(): Reads all incoming messages.
Message Parsing: If a message contains the keyword "TEMP_REQUEST", the function returns True, indicating that the server is requesting temperature data.
python
Copy code
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
main: The main loop of the client program.
serial.Serial(): Initializes the serial connection with the GSM modem on the specified port and baud rate (9600 in this case).
Main Loop: Continuously checks for an SMS from the server. If a "TEMP_REQUEST" is detected, the edge device reads the simulated temperature and sends it back to the server via SMS.
time.sleep(10): Adds a delay between checks to avoid overwhelming the GSM modem with requests.
server.py (Server Code)
python
Copy code
import serial
import time
Same as in the client code, these modules are imported to handle serial communication and timing.
python
Copy code
def send_sms(ser, recipient, message):
    ser.write(b'AT+CMGF=1\r')  # Set SMS mode to text
    time.sleep(1)
    ser.write(f'AT+CMGS="{recipient}"\r'.encode())
    time.sleep(1)
    ser.write(f'{message}\r'.encode())
    ser.write(b'\x1A')  # Send SMS (Ctrl+Z)
    time.sleep(3)
send_sms: The same function as in the client code, used here by the server to request temperature data from the client.
python
Copy code
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
read_sms: Reads SMS messages received by the server and checks for a response from the client containing the current temperature.
python
Copy code
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
main: The server's main function.
serial.Serial(): Initializes the serial connection with the GSM modem.
send_sms: Sends a "TEMP_REQUEST" SMS to the client to request the current temperature.
Main Loop: Continuously checks for a response from the client. When the temperature data is received, it prints the data and breaks the loop.
GSM and SMS Communication
GSM (Global System for Mobile Communications): A standard developed to describe protocols for second-generation (2G) cellular networks. GSM modems use AT commands to communicate with other devices.

SMS (Short Message Service): A text messaging service component of GSM. It allows the transmission of short text messages between mobile devices.

How Data is Transferred
Initialization: Both the client and server initialize their GSM modems using the serial port.
Requesting Data:
The server sends an SMS with the message "TEMP_REQUEST" to the client.
Client Response:
The client checks its received messages for "TEMP_REQUEST".
Upon finding the request, the client reads the temperature (simulated) and sends it back to the server via SMS.
Data Reception:
The server continuously checks its incoming messages for a response containing the temperature.
Once received, it displays the temperature data.
This method allows simple and reliable communication between devices over large distances using the GSM network, making it suitable for remote monitoring applications.
