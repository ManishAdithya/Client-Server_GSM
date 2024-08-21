#include <SoftwareSerial.h>
#include "DHT.h" //if needed

// Define DHT sensor type and pin
#define DHTPIN 12
#define DHTTYPE DHT11 //can use DHT12 also
DHT dht(DHTPIN, DHTTYPE);

SoftwareSerial SIM900(8, 7); // GSM module connected here

// Server IP and port
const String SERVER_IP = "127.0.0.1"; // Replace with your actual server IP
const String SERVER_PORT = "5001"; // Replace with your server port
const String SERVER_URL = "/send-temperature"; // Endpoint URL on your server

//creates the setup
void setup() {
  Serial.begin(9600);  //baude rate for data transfer in RSP32 
  SIM900.begin(9600);  //baude rate for data transfer between RSP32 and GSM
  dht.begin();  //initialises the DHT sensor
  pinMode(6, OUTPUT); //Output pin (pin which connects RSP32 and GSM)
  digitalWrite(6, HIGH); //Powering up the GSM

  delay(10000);  // Give time to log on to network

  // Initialize GSM module
  SIM900.print("AT+CMGF=1\r"); // Set SMS mode to text (required before sending HTTP requests)
  delay(1000);
  SIM900.println("AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"\r"); // Set GPRS mode
  delay(1000);
  SIM900.println("AT+SAPBR=3,1,\"APN\",\"your_apn\"\r"); // Set your network's APN
  delay(1000);
  SIM900.println("AT+SAPBR=1,1\r"); // Open GPRS context (enabling GSM to use mobile data)
  delay(3000);
}

void sendHTTPPost(String message) {
  SIM900.println("AT+HTTPINIT\r"); // Initialize HTTP service on the GSM module
  delay(1000);
  SIM900.println("AT+HTTPPARA=\"CID\",1\r"); // Sets the Connection Id for the HTTP session
  delay(1000);
  SIM900.println("AT+HTTPPARA=\"URL\",\"http://" + SERVER_IP + ":" + SERVER_PORT + SERVER_URL + "\"\r"); // Set server URL
  delay(1000);
  SIM900.println("AT+HTTPPARA=\"CONTENT\",\"application/json\"\r"); // Set content type to JSON
  delay(1000);

  // Start sending data
  int data_length = message.length();
  SIM900.println("AT+HTTPDATA=" + String(data_length) + ",10000\r"); // Set data length
  delay(1000);
  SIM900.print(message); // Send the actual data
  delay(1000);
  SIM900.println("AT+HTTPACTION=1\r"); // Send HTTP POST
  delay(1000);

  // Read the response
  String response = "";
  while (SIM900.available()) {
    response += char(SIM900.read());
  }
  Serial.println("Server Response: " + response);

  SIM900.println("AT+HTTPTERM\r"); // Terminate HTTP service
  delay(1000);
}

String getTemperature() {
  int t = dht.readTemperature();
  if (isnan(t)) {
    return "Failed to read temperature";
  }
  return String(t);
}

void checkForRequest() {
  SIM900.println("AT+HTTPINIT\r");
  delay(1000);
  SIM900.println("AT+HTTPPARA=\"CID\",1\r");
  delay(1000);
  SIM900.println("AT+HTTPPARA=\"URL\",\"http://" + SERVER_IP + ":" + SERVER_PORT + "/get-temperature\"\r"); // URL to check for requests
  delay(1000);
  SIM900.println("AT+HTTPACTION=0\r"); // HTTP GET request
  delay(1000);

  String response = "";
  while (SIM900.available()) {
    response += char(SIM900.read());
  }

  if (response.indexOf("CHECK_TEMP") >= 0) {
    String temp = getTemperature();
    sendHTTPPost("{\"temperature\": " + temp + "}");
  }

  SIM900.println("AT+HTTPTERM\r");
  delay(1000);
}

void loop() {
  checkForRequest(); // Check if the server is asking for the temperature

  // Send temperature at regular intervals
  delay(2000);
  String message = "{\"temperature\": " + getTemperature() + "}";
  sendHTTPPost(message);

  delay(1800000); // Wait for 30 minutes (1800 seconds) before sending the next data
}

//End of the code 