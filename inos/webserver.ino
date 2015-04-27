/* http://playground.arduino.cc/Code/WebServerST */
/* 
   Web server sketch for IDE v1.0.3 and w5100/w5200
   Originally posted October 2012 by SurferTim
   Modified April 2013 by SurferTim
*/

#include <SPI.h>
#include <Ethernet.h>
// uncomment next line if using SD
// #include <SD.h>

// this must be unique
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEC };

// change to your network settings
IPAddress ip( 192,168,2,2 );
IPAddress gateway( 192,168,2,1 );
IPAddress subnet( 255,255,255,0 );

EthernetServer server(80);

void setup()
{
  Serial.begin(9600);

  // disable w5100 while setting up SD
  // uncomment next 5 lines if using a microSD card

  //  pinMode(10,OUTPUT);
  //  digitalWrite(10,HIGH);
  // Serial.print(F("Starting SD.."));
  // if(!SD.begin(4)) Serial.println(F("failed"));
  // else Serial.println(F("ok"));

  Ethernet.begin(mac, ip, gateway, gateway, subnet);

  delay(2000);
  server.begin();
  Serial.println(F("Ready"));
}

void loop()
{
  EthernetClient client = server.available();
  if(client) {
    boolean currentLineIsBlank = true;
    boolean currentLineIsGet = true;
    int tCount = 0;
    char tBuf[64];
    int r,t;
    char *pch;

    Serial.print(F("Client request: "));

    // this controls the timeout
    int loopCount = 0;

    while (client.connected()) {
      while(client.available()) {
        // if packet, reset loopCount
        loopCount = 0;
        char c = client.read();

        if(currentLineIsGet && tCount < 63)
        {
          tBuf[tCount] = c;
          tCount++;
        }

        if (c == '\n' && currentLineIsBlank) {
          // send a standard http response
          Serial.println(tBuf);
          Serial.print(F("POST data: "));
          while(client.available()) Serial.write(client.read());
          Serial.println();

          pch = strtok(tBuf,"?");

          while(pch != NULL)
          {
            if(strncmp(pch,"t=",2) == 0)
            {
              t = atoi(pch+2);
              Serial.print("t=");
              Serial.println(t,DEC);             
            }

            if(strncmp(pch,"r=",2) == 0)
            {
              r = atoi(pch+2);
              Serial.print("r=");              
              Serial.println(r,DEC);
            }


            pch = strtok(NULL,"& ");
          }
          Serial.println(F("Sending response"));
          client.print(F("HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n<html>"));

          client.println(F("<head><script type=\"text/javascript\">"));
          client.println(F("function show_alert() {alert(\"This is an alert\");}"));
          client.println(F("</script></head>"));


          client.println(F("<body><H1>TEST</H1>"));

          client.println(F("<form method=GET onSubmit=\"show_alert()\">T: <input type=text name=t><br>"));
          client.println(F("R: <input type=text name=r><br><input type=submit></form>"));


          client.println(F("</body></html>"));
          client.stop();
        }
        else if (c == '\n') {
          currentLineIsBlank = true;
          currentLineIsGet = false;
        } 
        else if (c != '\r') {
          currentLineIsBlank = false;
        }
      }

      loopCount++;

      // if 10000ms has passed since last packet
      if(loopCount > 10000) {
        // close connection
        client.stop();
        Serial.println("\r\nTimeout");
      }

      // delay 1ms for timeout timing
      delay(1);
    }
    Serial.println(F("done"));
  }
}
