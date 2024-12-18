

// Defining pins numbers
const int SW_pin = 2; // button pin
const int X_pin = 0; // analog X pin
const int Y_pin = 1; // analog Y pin


void setup() {
  pinMode(SW_pin, INPUT);
  digitalWrite(SW_pin, HIGH);
  Serial.begin(9600);
}

void loop() {
  int bouton = digitalRead(SW_pin);
  
  int axeX = analogRead(X_pin);
  int axeY = analogRead(Y_pin);
  String  donnees = "" + String(bouton) + "|" + String(axeX) + "|" + String(axeY) + "";
  Serial.print(donnees);
  Serial.print("\n");
  delay(16);
}
