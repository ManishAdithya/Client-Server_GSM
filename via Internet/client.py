import serial
import time
import requests
import random

# Configure the GSM module
gsm_serial = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)  # Replace with the correct serial port for your setup

# APN details (replace with your carrier's details)
APN = "your_apn_here"
USERNAME = "your_username_here"
PASSWORD = "your_password_here"

SERVER_URL = "http://<server_ip>:5000/send-temperature"  # Replace with your server's public IP or domain

def send_at_command(command, expected_response="OK", timeout=5):
    gsm_serial.write((command + "\r").encode())
    time.sleep(1)
    response = gsm_serial.read(timeout).decode()
    print(f"Command: {command}, Response: {response}")
    return expected_response in response

def establish_gprs_connection():
    send_at_command("AT")  # Check if the module is ready
    send_at_command("AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"")
    send_at_command(f"AT+SAPBR=3,1,\"APN\",\"{APN}\"")
    send_at_command(f"AT+SAPBR=3,1,\"USER\",\"{USERNAME}\"")
    send_at_command(f"AT+SAPBR=3,1,\"PWD\",\"{PASSWORD}\"")
    send_at_command("AT+SAPBR=1,1")  # Open GPRS context
    send_at_command("AT+SAPBR=2,1")  # Query the context

def close_gprs_connection():
    send_at_command("AT+SAPBR=0,1")  # Close GPRS context

def send_temperature(temperature):
    try:
        data = {'temperature': temperature}
        response = requests.post(SERVER_URL, json=data)
        print(f"Data sent: {temperature}C, Response: {response.status_code}")
    except Exception as e:
        print(f"Failed to send data: {e}")

if __name__ == "__main__":
    establish_gprs_connection()
    while True:
        temperature = round(random.uniform(20.0, 30.0), 2)  # Simulate temperature reading
        send_temperature(temperature)
        time.sleep(1800)  # Wait for 30 minutes before sending the next data
    close_gprs_connection()
