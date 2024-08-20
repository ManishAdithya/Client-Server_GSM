
  ## Establishing a connection between an "edge" device and a server via GSM to send and request data without Wi-Fi

# Introduction
This research explores the implementation of a client-server model using GSM technology to enable data transmission between an edge device and a central server (without the usage of Wi-Fi). The primary focus is on creating a reliable communication channel where the edge device periodically sends temperature data and responds to server requests for real-time information. The server can also ping the client at any point of time and also ask for the current data. This system is intended for applications that require continuous environmental monitoring and low-latency data exchange.
# Scenario
Consider a remote agricultural field equipped with an edge device that monitors temperature. The edge device, connected via GSM, sends temperature data to a central server every 30 minutes. If sudden weather changes occur, the server can request real-time temperature data from the edge device. The edge device detects the current temperature and immediately transmits the data back to the server. This 
# Objectives
To establish a reliable GSM connection between the edge device and server for data transmission.
To ensure the edge device can send temperature data to the server at regular intervals (every 30 minutes).
To enable the server to request real-time temperature data from the edge device and receive prompt responses.
To evaluate the efficiency and reliability of the GSM-based communication system in varying network conditions.
# Hypothesis
It is hypothesised that a GSM-based communication model can provide reliable and efficient data transmission between an edge device and a server, allowing for timely data requests and regular reporting of temperature readings, even in low-connectivity scenarios.
# Methodology and Methods
System Design: Develop a client-server architecture where the edge device serves as the client and the central server handles data processing and requests.
GSM Integration: Implement GSM modules on the edge device for data transmission and request handling.
Data Transmission Protocol: Configure the edge device to send temperature data to the server every 30 minutes. Additionally, design a mechanism for the server to request temperature data at any time.
 Before sending, each message is encrypted using this shared key, ensuring that only parties with the key can decrypt and read the messages.
Hashing with SHA-256 to ensure data integrity by verifying that the message has not been altered during transmission.
Testing and Evaluation: Conduct tests to evaluate the system’s reliability, response time, and data integrity under various network conditions. Analyse the performance of the GSM connection in both stable and fluctuating signal environments.


# References
Similar project where the temperature data is requested using gsm and arduino (via SMS):

https://www.electroniclinic.com/request-temperature-data-using-gsm-and-arduino/  


Similar project where the green-house effect is monitored:

https://nevonprojects.com/iot-based-greenhouse-monitoring-system-using-raspberry-pi/


Similar projects with source code:

https://techatronic.com/category/gsm-projects/


Sample server examples that can ping GSM data:

https://github.com/vshymanskyy/TinyGSM/blob/master/README.md

https://github.com/ptrkrysik/gr-gsm?tab=readme-ov-file





