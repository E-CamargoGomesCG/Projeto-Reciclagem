#include <Stepper.h>
#include <Servo.h>

//ALTERAÇÕES NO CODIGO OFICIAL
#define Num_Sen 4

Servo Papel;
Servo Metal;
Servo Plastico;
Servo Vidro;

//const int passosPorVoltar = 90;
Stepper motor_passo(90, 8, 10, 9, 11);

//MOTOR ULTRASONICO(TRIGGER, ECHO) - INDICE DO MATERIAL

// MOTOR ULTRASONICO DO VIDRO (40,41) - INDICE 0
// MOTOR ULTRASONICO DO PAPEL(42,43) - INDICE 1
// MOTOR ULTRASONICO DO PLASTICO(44,45) - INDICE 2
// MOTOR ULTRASONICO DO METAL(46,47) - INDICE 3

const int pinoTrig[Num_Sen] = {40, 42, 44, 46};
const int pinoEcho[Num_Sen] = {41, 43, 45, 47};

const int angulosAbertos[4] = {0, 125,0,90}; // {NÃO TEM COMPORTA, 1º COMPORTA, 2º COMPORTA, 3º COMPORTA} - {VIDRO, PAPEL, PLASTICO, METAL}
const int angulosFechados[4] = {0, 65,55,35}; // {NÃO TEM COMPORTA, 1º COMPORTA, 2º COMPORTA, 3º COMPORTA} - {VIDRO, PAPEL, PLASTICO, METAL}

float mediaDasDistancias[Num_Sen] = {0};
String status= "desocupado";

void setup() {
  Serial.begin(9600);

  // ANTES
  //Papel.attach(3); // PINO 3 NO ARDUINO - ERA SEGUNDA COMPORTA
  //Metal.attach(4); // PINO 4 NO ARDUINO - ERA A TERCEIRA COMPORTA
  //Plastico.attach(5); // PINO 5 NO ARDUINO - ERA PRIMEIRA COMPORTA

  // ALTERADO
  Papel.attach(5); // PINO 3 NO ARDUINO - PRIMEIRA COMPORTA
  Plastico.attach(3); // PINO 4 NO ARDUINO - SEGUNDA COMPORTA
  Metal.attach(4); // PINO 5 NO ARDUINO - TERCEIRA COMPORTA

  motor_passo.setSpeed(350);
 
  for (int i = 0; i < Num_Sen; i++) {
    // Inicializa os ultrasonicos e calcula a media de distancia de todos os sensores ultrasonicos (Quando nao tem nada passando)
    pinMode(pinoTrig[i], OUTPUT);
    pinMode(pinoEcho[i], INPUT);
    mediaDasDistancias[i] = calculaMediaDasDistancias(pinoTrig[i], pinoEcho[i]);
  }

  // Inicializa os servos nos angulos abertos (liberando a passagem da esteira)
  Papel.write(angulosAbertos[1]);
  Plastico.write(angulosAbertos[2]);
  Metal.write(angulosAbertos[3]);
 
 //Envia ao python que está desocupado
  Serial.print("desocupado");
}

void loop() {
  if (status=="desocupado") {  
    if (Serial.available() > 0) {
      String material = Serial.readStringUntil(';');
      if (material == "vidro") {
        status="ocupado";
        Serial.print(status);
        verificar(Vidro, pinoTrig[0], pinoEcho[0], 0);
      }
      else if (material == "papel") {
       status="ocupado";
        Serial.print(status);
        fecharComporta(Papel, 1);
        verificar(Papel, pinoTrig[1], pinoEcho[1], 1);
      }
      else if (material == "plastico") {
        status="ocupado";
        Serial.print(status);
        fecharComporta(Plastico, 2);
        verificar(Plastico, pinoTrig[2], pinoEcho[2], 2);
      }
      else if (material == "metal") {
        status="ocupado";
         Serial.print(status);
        fecharComporta(Metal, 3);
        verificar(Metal, pinoTrig[3], pinoEcho[3], 3);
      }
     
    }
  }
 
}

void fecharComporta(Servo servo, int i) {
  servo.write(angulosFechados[i]);
}

void verificar(Servo servo, int pinoTrig, int pinoEcho, int indice) {
  while (true) {
    float distancia = calculaMediaDasDistancias(pinoTrig, pinoEcho);
     
     motor_passo.step(-90);
    if (abs(mediaDasDistancias[indice]-distancia) >= 1.2) {
      if (indice == 0) {
        status="desocupado";
        Serial.print("desocupado");
       
        break;
      } else {
        servo.write(angulosAbertos[indice]);
       
        status="desocupado";
        Serial.print(status);
         
        break;
      }
    }
  }
}

float calculaMediaDasDistancias(int pinoTrig, int pinoEcho) {
  float distancia = 0;

    digitalWrite(pinoTrig, LOW);
    delayMicroseconds(2);
    digitalWrite(pinoTrig, HIGH);
    delayMicroseconds(10);
    digitalWrite(pinoTrig, LOW);
    float duracao = pulseIn(pinoEcho, HIGH);
    distancia += (duracao * 0.034 / 2);

  return distancia;

}