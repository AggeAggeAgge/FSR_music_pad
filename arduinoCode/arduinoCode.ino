
#define fsrpin A0

int fsrreading; //Variable to store FSR value

void setup() {
  // Begin serial communication at a baud rate of 9600:
  Serial.begin(115200);
}

void loop() {
  fsrreading = analogRead(fsrpin);

  Serial.println(fsrreading);
  delay(5);
}