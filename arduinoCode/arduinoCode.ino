#define fsrpin A0
#define fsrpin2 A1


int fsrreading;
int fsrreading2;

int threshold = 400;

void setup() {
  Serial.begin(115200);
}

void loop() {
  fsrreading = analogRead(fsrpin);
  fsrreading2 = analogRead(fsrpin2);


  contactPython(fsrpin, 1, fsrreading);  
  contactPython(fsrpin2, 2, fsrreading2);  


}

void contactPython(int fsrPin, int buttonNum, int reading) {
  if (reading > threshold) {
    Serial.println(buttonNum);
    delay(50);
  }

}

/*
  if (fsrreading > threshold) {
    Serial.println("HIT");
    delay(100);
  }

  */