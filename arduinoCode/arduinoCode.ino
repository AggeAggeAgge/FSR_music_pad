
#define fsrpin A0

int fsrreading; //Variable to store FSR value

void setup() {
  // Begin serial communication at a baud rate of 9600:
  Serial.begin(9600);
}

void loop() {
  fsrreading = analogRead(fsrpin);

  Serial.print("Analog reading = ");
  Serial.println(fsrreading);

  delay(50);
}