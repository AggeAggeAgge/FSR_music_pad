#define fsrpin A0

int fsrreading;
int threshold = 400;

void setup() {
  Serial.begin(115200);
}

void loop() {
  fsrreading = analogRead(fsrpin);

  if (fsrreading > threshold) {
    Serial.println("HIT");
    delay(100);
  }
}