#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

float temperaturaStage=0;
float temperature=0;
const char* ssid = "xxxx";
const char* password = "xxxx";
ESP8266WebServer server(80);

void setup(void){
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  configuration();
  server.on("/", handleRoot);
  server.begin();
}

void loop(void){
  temperature = ((analogRead(0))*3.3/1023)/0.01;
  server.handleClient();
  if(temperaturaCalculation(temperature)){
    Serial.println(temperaturaStage);
  }
}

void configuration(){
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.print("Wifi");
  Serial.println(WiFi.localIP()); 
}

void handleRoot() {
 server.send(200, "text/plain", (String)temperature);
}


boolean temperaturaCalculation(float temperatura){

  if(temperaturaStage == 0){
    temperaturaStage = temperatura;
  }
  if(temperaturaStage != temperatura){
     float temperaturaDelta = temperaturaDeltaCalculation(temperatura,temperaturaStage);
      if(temperaturaDelta > 0.33 ){
        temperaturaStage = temperatura;
        return true;     
      }
    }
  return false;
}

float temperaturaDeltaCalculation (float temperaturaInicio, float temperaturaFim){
  float temperatura=0; 
  temperatura = temperaturaFim - temperaturaInicio;  
  return modulo(temperatura);
}

float modulo(float number){
  if(number < 0){
      number = number * (-1);
  }
  return number;
}
