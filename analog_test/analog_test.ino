#define analogPin A7
#define RelPin 5

short analogValue;
byte buff[6];
unsigned long duration, startTime, Duration_AC, durationLimit, Delay;
String data_array[10];
String command;

void setup() {
  Serial.begin(1000000);

  Duration_AC = 100 * pow(10, 3); // ms
  Delay = 1 * pow(10, 3); // ms
  durationLimit  = Delay + (2 * Duration_AC); //ms
  
  analogReference(DEFAULT);
  pinMode(RelPin, OUTPUT);
  pinMode(analogPin, INPUT);
  digitalWrite(RelPin, LOW);
  analogWrite(analogPin, 0);
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.readString();
    if (command == "s") {
      startTime = micros();
    } else {
      durationLimit = command.substring(command.indexOf("s") + 1).toInt();
      Duration_AC = durationLimit * 0.6;
      Delay = durationLimit * 0.1;
      startTime = micros();
    }
  }
  
  if (startTime != 0) {
    duration = micros() - startTime;
    if (duration < durationLimit) {
     
      if ( (duration >= Delay) && (duration <= (Delay + Duration_AC)) ) {
        digitalWrite(RelPin, HIGH);
      } else {
        digitalWrite(RelPin, LOW);
      }
      
      writeData();
    } else {
      digitalWrite(RelPin, LOW);
      startTime = 0;
    }
  }
}

void writeData() {
  analogValue = analogRead(analogPin);
  buff[0] = analogValue & 0xFF;
  buff[1] = analogValue >> 8 & 0xFF;
  buff[2] = duration & 0xFF;
  buff[3] = duration >> 8 & 0xFF;
  buff[4] = duration >> 16 & 0xFF;
  buff[5] = duration >> 24 & 0xFF;
  Serial.write(buff, sizeof(buff));
}
