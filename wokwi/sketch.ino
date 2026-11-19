#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <ESP32Servo.h>
#include <ArduinoJson.h>

// Wi-Fi Config for Wokwi
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// MQTT Config
// Using EMQX public broker (very stable with Wokwi virtual WiFi gateway)
const char* mqtt_server = "broker.emqx.io";
const int mqtt_port = 1883;
const char* topic_base = "bmu/iotnaa/smartparking-g01";
const char* node_id = "A";

// Pin Definitions
const int TRIG_PINS[4] = {13, 14, 26, 33};
const int ECHO_PINS[4] = {12, 27, 25, 32};
const int RED_LEDS[4]  = {18, 19, 23, 5};
const int GREEN_LED    = 2;
const int SERVO_PIN    = 4;
const int BUZZER_PIN   = 15;

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
Servo gateServo;
WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastPublishTime = 0;
const unsigned long publishInterval = 5000;
int slotOccupancy[4] = {0, 0, 0, 0};
float slotDistances[4] = {0, 0, 0, 0};

float readUltrasonic(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  long duration = pulseIn(echoPin, HIGH, 30000);
  if (duration == 0) return 400.0;
  float distance = duration * 0.034 / 2.0;
  return distance;
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  message.trim();
  Serial.print("MQTT Command [");
  Serial.print(topic);
  Serial.print("]: ");
  Serial.println(message);

  if (message == "open") {
    gateServo.write(90);
    digitalWrite(BUZZER_PIN, HIGH);
    delay(100);
    digitalWrite(BUZZER_PIN, LOW);
  } else if (message == "close") {
    gateServo.write(0);
    digitalWrite(BUZZER_PIN, HIGH);
    delay(50);
    digitalWrite(BUZZER_PIN, LOW);
    delay(50);
    digitalWrite(BUZZER_PIN, HIGH);
    delay(50);
    digitalWrite(BUZZER_PIN, LOW);
  }
}

void reconnectMQTT() {
  int attempts = 0;
  while (!client.connected() && attempts < 5) {
    attempts++;
    Serial.print("Connecting to MQTT broker (");
    Serial.print(mqtt_server);
    Serial.print(")...");
    
    // Generate clean unique client ID
    String clientId = "ESP32-SmartParking-" + String((uint32_t)ESP.getEfuseMac(), HEX);
    
    if (client.connect(clientId.c_str())) {
      Serial.println(" connected successfully!");
      char cmdTopic[80];
      snprintf(cmdTopic, sizeof(cmdTopic), "%s/%s/cmd/gate", topic_base, node_id);
      client.subscribe(cmdTopic);
      Serial.print("Subscribed to command topic: ");
      Serial.println(cmdTopic);
    } else {
      Serial.print(" failed, rc=");
      Serial.print(client.state());
      Serial.println(" (retrying in 2 seconds)...");
      delay(2000);
    }
  }
}

void updateOLED() {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("BMU SMART PARKING");
  display.drawLine(0, 10, 127, 10, SSD1306_WHITE);

  int occupiedCount = 0;
  for (int i = 0; i < 4; i++) {
    if (slotOccupancy[i] == 1) occupiedCount++;
  }
  int freeSlots = 4 - occupiedCount;

  display.setCursor(0, 16);
  display.printf("Zone A: %d/4 Occupied\n", occupiedCount);
  display.setCursor(0, 28);
  display.printf("Free Slots: %d\n", freeSlots);

  display.setCursor(0, 42);
  for (int i = 0; i < 4; i++) {
    display.printf("S%d:%s ", i + 1, slotOccupancy[i] ? "OCC" : "VAC");
  }

  display.setCursor(0, 54);
  display.print(freeSlots > 0 ? "[LOT AVAILABLE]" : "[LOT FULL]");
  display.display();
}

void setup() {
  Serial.begin(115200);
  delay(100);
  Serial.println("\nStarting ESP32 Smart Parking Node A...");

  for (int i = 0; i < 4; i++) {
    pinMode(TRIG_PINS[i], OUTPUT);
    pinMode(ECHO_PINS[i], INPUT);
    pinMode(RED_LEDS[i], OUTPUT);
    digitalWrite(RED_LEDS[i], LOW);
  }
  pinMode(GREEN_LED, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);

  gateServo.attach(SERVO_PIN);
  gateServo.write(0);

  Wire.begin(21, 22);
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("SSD1306 OLED initialization failed");
  } else {
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(10, 20);
    display.println("Connecting WiFi...");
    display.display();
  }

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wokwi Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" Connected!");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());

  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(mqttCallback);
  client.setBufferSize(512);
  client.setKeepAlive(30);

  reconnectMQTT();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    WiFi.begin(ssid, password);
    delay(500);
    return;
  }
  
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastPublishTime >= publishInterval) {
    lastPublishTime = now;
    int anyAvailable = 0;

    for (int i = 0; i < 4; i++) {
      float dist = readUltrasonic(TRIG_PINS[i], ECHO_PINS[i]);
      slotDistances[i] = dist;
      int occ = (dist < 10.0) ? 1 : 0;
      slotOccupancy[i] = occ;

      digitalWrite(RED_LEDS[i], occ ? HIGH : LOW);
      if (!occ) anyAvailable = 1;

      StaticJsonDocument<200> doc;
      doc["node"] = node_id;
      doc["slot"] = i + 1;
      doc["dist"] = round(dist * 10.0) / 10.0;
      doc["occ"] = occ;
      doc["ts"] = (unsigned long)(time(nullptr) > 100000 ? time(nullptr) : now / 1000);
      doc["src"] = "wokwi";

      char jsonBuffer[256];
      serializeJson(doc, jsonBuffer);

      char topic[80];
      snprintf(topic, sizeof(topic), "%s/%s/slot%d", topic_base, node_id, i + 1);
      
      if (client.connected()) {
        client.publish(topic, jsonBuffer);
        Serial.print("Published to ");
        Serial.print(topic);
        Serial.print(": ");
        Serial.println(jsonBuffer);
      }
    }

    digitalWrite(GREEN_LED, anyAvailable ? HIGH : LOW);
    updateOLED();
  }
}
