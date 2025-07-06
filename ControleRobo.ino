#include <Servo.h>

#define pos_inicial 90

Servo servos[3];

int servoPin1 = 7;
int servoPin2 = 8;
int servoPin3 = 9;

void setup() {
  // put your setup code here, to run once:
  servos[0].attach(servoPin1);
  servos[1].attach(servoPin2);
  servos[2].attach(servoPin3);
  Serial.begin(9600);
  // Inicializar robo na posição inicial
  for(int i = 0; i < 3; i++) {
    servos[i].write(pos_inicial);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0)
  {
    //Ler comando
    String command = Serial.readStringUntil('\n');
    processCommand(command);
    Serial.println("1");
  }
}

void processCommand(String command)
{
  /*A estrutura do commando será a seguinte
  b'AAABBBCCC'
  AAA = 0 - 180 para pos do servo 1
  BBB = 0 - 180 para pos do servo 2
  CCC = 0 - 180 para pos do servo 3
  */
  
  String q1 = command.substring(0, 3);
  String q2 = command.substring(3, 6);
  String q3 = command.substring(6, 9);
  
  servos[0].write(q1.toInt());
  servos[1].write(q2.toInt());
  servos[2].write(q3.toInt());
}
