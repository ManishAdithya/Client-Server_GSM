import random
import time
import serial

# Set up the serial connection with your GSM module
serial_port = "/dev/ttyUSB0"  # Replace with your actual port
baud_rate = 9600  # Common baud rate for GSM modules
gsm = serial.Serial(serial_port, baud_rate, timeout=1)

# Example server IP and port (temporary)
SERVER_URL_POST = "http://127.0.0.1:5000/send-temperature"  # Replace with your actual server's IP or domain and port


def generate_temperature():
    """Generate a random temperature value between 20.0 and 30.0 degrees Celsius."""
    return round(random.uniform(20.0, 30.0), 2)


def send_temperature_via_gsm(temperature):
    """Send the temperature data to the server via GSM."""
    at_command = f'AT+HTTPPARA="URL","{SERVER_URL_POST}"\r'
    gsm.write(at_command.encode())
    time.sleep(1)

    gsm.write('AT+HTTPACTION=1\r'.encode())
    time.sleep(1)

    data_length = len(str(temperature))
    gsm.write(f'AT+HTTPDATA={data_length},10000\r'.encode())
    time.sleep(1)

    gsm.write(str(temperature).encode())
    time.sleep(1)

    gsm.write('AT+HTTPTERM\r'.encode())

    response = gsm.read(100).decode()
    print(f"Sent temperature: {temperature}C, GSM Response: {response}")


if __name__ == "__main__":
    while True:
        temperature = generate_temperature()
        send_temperature_via_gsm(temperature)
        time.sleep(1800)  # Wait for 30 minutes (1800 seconds) before sending the next data
