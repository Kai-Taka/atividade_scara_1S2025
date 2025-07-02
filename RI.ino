#include <Servo.h>
#include <math.h>

// --- 1. CONFIGURAÇÕES E DEFINIÇÕES ---

// --- Pinos dos Servos ---
#define SERVO_PIN_1 9
#define SERVO_PIN_2 10
#define SERVO_PIN_3 11

// --- Definições do Robô e Controle ---
const int NUM_JOINTS = 3;
const float ALPHA = 0.8; // Ganho do controle. Ajuste este valor (entre 0.1 e 1.5) para mudar a velocidade de convergência.

// --- Objetos dos Servos ---
Servo servo1;
Servo servo2;
Servo servo3;

// --- Estado do Robô (ângulos das juntas em RADIANOS) ---
// Como não há encoders, este vetor armazena a última posição comandada.
float q_current[NUM_JOINTS] = {0.0, 0.0, 0.0};

// --- Variáveis para o Loop de Controle ---
unsigned long last_time;
float delta_t;

// --- Definição da Trajetória (Linha Reta) ---
float start_pos[3] = {160.0, -30.3, 15.93}; // Posição inicial (calculada com q={0,0,0})
float end_pos[3]   = {100.0, 50.0, 100.0};  // Posição final desejada
float total_time   = 8.0; // Tempo total para completar a trajetória em segundos
float time_elapsed = 0.0;


void setup() {
  Serial.begin(115200); // Usar uma velocidade maior para imprimir mais dados
  Serial.println("Iniciando o Controle do Robo com Jacobiano Transposto...");

  // Anexa os servos aos pinos e define os limites (em microssegundos) se necessário
  servo1.attach(SERVO_PIN_1);
  servo2.attach(SERVO_PIN_2);
  servo3.attach(SERVO_PIN_3);

  // Mover para a posição inicial (q = {0,0,0})
  // Converte radianos para graus
  servo1.write(90 + degrees(q_current[0])); // Assumindo que 90 graus é a posição 'zero'
  servo2.write(90 + degrees(q_current[1]));
  servo3.write(90 + degrees(q_current[2]));

  delay(2000); // Espera o robô chegar na posição inicial

  last_time = micros(); // Inicia o contador de tempo
}


void loop() {
  // --- A. CÁLCULO DO TEMPO DO CICLO (delta_t) ---
  unsigned long current_time = micros();
  delta_t = (current_time - last_time) / 1000000.0f; // delta_t em segundos
  last_time = current_time;

  // Atualiza o tempo da trajetória
  if (time_elapsed < total_time) {
    time_elapsed += delta_t;
  }

  // --- B. CALCULAR A TRAJETÓRIA DESEJADA (x_desired) ---
  float x_desired[3];
  float path_ratio = time_elapsed / total_time;
  if (path_ratio > 1.0) path_ratio = 1.0; // Garante que não ultrapasse o ponto final

  for (int i = 0; i < 3; i++) {
    x_desired[i] = start_pos[i] + (end_pos[i] - start_pos[i]) * path_ratio;
  }

  // --- C. CALCULAR CINEMÁTICA DIRETA (onde o robô está) ---
  float x_current[3];
  forwardKinematics(q_current, x_current);

  // --- D. CALCULAR O VETOR DE ERRO ---
  float error[3];
  error[0] = x_desired[0] - x_current[0];
  error[1] = x_desired[1] - x_current[1];
  error[2] = x_desired[2] - x_current[2];

  // --- E. CALCULAR A MATRIZ JACOBIANA (apenas a parte de posição 3x3) ---
  float J[3][3];
  calculateJacobian(q_current, J);

  // --- F. CALCULAR A TRANSPOSTA DO JACOBIANO ---
  float J_T[3][3];
  transposeMatrix(J, J_T);

  // --- G. LEI DE CONTROLE: Jacobiano Transposto ---
  // q_dot = alpha * J_T * erro
  float q_dot[3];
  matrixVectorMultiply(J_T, error, q_dot);
  for (int i = 0; i < 3; i++) {
    q_dot[i] *= ALPHA;
  }

  // --- H. INTEGRAÇÃO NUMÉRICA (obter novas posições de junta) ---
  // q_novo = q_antigo + q_dot * delta_t
  for (int i = 0; i < 3; i++) {
    q_current[i] += q_dot[i] * delta_t;
  }

  // --- I. COMANDAR OS SERVOS ---
  commandServos(q_current);

  // --- J. IMPRIMIR DADOS PARA DEBUG ---
  printDebug(x_desired, x_current, error, q_current);
  
  delay(10); // Pequeno delay para estabilidade
}


// =================================================================
// --- FUNÇÕES DO ROBÔ ---
// =================================================================

/**
 * @brief Calcula a cinemática direta (apenas posição x,y,z).
 * Traduzido da sua matriz T03.
 * @param q Vetor de ângulos das juntas [q1, q2, q3] em RADIANOS.
 * @param x_current Vetor de saída para a posição cartesiana [x, y, z].
 */
void forwardKinematics(const float q[], float x_current[]) {
  float q1 = q[0], q2 = q[1], q3 = q[2];
  
  // Usando identidades trigonométricas: cos(a+b) e sin(a+b)
  float c1 = cos(q1), s1 = sin(q1);
  float c2 = cos(q2), s2 = sin(q2);
  float c23 = cos(q2 + q3), s23 = sin(q2 + q3);

  // Equações da última coluna da sua matriz T03
  x_current[0] = (80.0 * c2 + 80.0 * c23) * c1 - 30.3 * s1;
  x_current[1] = (80.0 * c2 + 80.0 * c23) * s1 + 30.3 * c1;
  x_current[2] = 80.0 * s2 + 80.0 * s23 + 15.93;
}


/**
 * @brief Calcula a matriz Jacobiana de posição (3x3).
 * Traduzido da sua matriz Jacobiana simbólica.
 * @param q Vetor de ângulos das juntas [q1, q2, q3] em RADIANOS.
 * @param J Matriz de saída 3x3 Jacobiana.
 */
void calculateJacobian(const float q[], float J[3][3]) {
  float q1 = q[0], q2 = q[1], q3 = q[2];
  
  float s1 = sin(q1), c1 = cos(q1);
  float s2 = sin(q2), c2 = cos(q2);
  float s23 = sin(q2 + q3), c23 = cos(q2 + q3);
  
  // Linha 0
  J[0][0] = -80.0 * s1 * c2 - 80.0 * s1 * c23 - 30.3 * c1;
  J[0][1] = -80.0 * (s2 + s23) * c1;
  J[0][2] = -80.0 * s23 * c1;

  // Linha 1
  J[1][0] = 30.3 * s1 + 80.0 * c1 * c2 + 80.0 * c1 * c23;
  J[1][1] = -80.0 * (s2 + s23) * s1;
  J[1][2] = -80.0 * s1 * s23;

  // Linha 2
  J[2][0] = 0;
  J[2][1] = 80.0 * c2 + 80.0 * c23;
  J[2][2] = 80.0 * c23;
}


/**
 * @brief Comanda os servos para as posições desejadas.
 * Converte radianos para graus e mapeia para a faixa do servo.
 * @param q Vetor de ângulos das juntas [q1, q2, q3] em RADIANOS.
 */
void commandServos(const float q[]) {
  // Converte radianos para graus
  float angle1_deg = degrees(q[0]);
  float angle2_deg = degrees(q[1]);
  float angle3_deg = degrees(q[2]);
  
  // Mapeia para a posição do servo.
  // IMPORTANTE: Ajuste o '90' e os limites (0, 180) conforme a montagem do seu robô.
  // '90' aqui representa a posição "zero" do sistema de coordenadas.
  int servo1_pos =  angle1_deg;
  int servo2_pos = 90 + angle2_deg;
  int servo3_pos = 90 + angle3_deg;
  
  // Limita os ângulos para a faixa segura do servo (0-180 graus)
  servo1_pos = constrain(servo1_pos, 0, 180);
  servo2_pos = constrain(servo2_pos, 0, 180);
  servo3_pos = constrain(servo3_pos, 0, 180);
  
  servo1.write(servo1_pos);
  servo2.write(servo2_pos);
  servo3.write(servo3_pos);
}


// =================================================================
// --- FUNÇÕES MATEMÁTICAS E DE DEBUG ---
// =================================================================

void transposeMatrix(const float A[3][3], float AT[3][3]) {
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      AT[i][j] = A[j][i];
    }
  }
}

void matrixVectorMultiply(const float M[3][3], const float V[3], float result[3]) {
  for (int i = 0; i < 3; i++) {
    result[i] = 0;
    for (int j = 0; j < 3; j++) {
      result[i] += M[i][j] * V[j];
    }
  }
}

void printDebug(const float des[], const float cur[], const float err[], const float q[]) {
  static unsigned long lastPrintTime = 0;
  if (millis() - lastPrintTime > 200) { // Imprime a cada 200ms
    Serial.print("Des: [");
    Serial.print(des[0]); Serial.print(", ");
    Serial.print(des[1]); Serial.print(", ");
    Serial.print(des[2]); Serial.print("] | ");
    
    Serial.print("Cur: [");
    Serial.print(cur[0], 1); Serial.print(", ");
    Serial.print(cur[1], 1); Serial.print(", ");
    Serial.print(cur[2], 1); Serial.print("] | ");

    Serial.print("Err: [");
    Serial.print(err[0], 1); Serial.print(", ");
    Serial.print(err[1], 1); Serial.print(", ");
    Serial.print(err[2], 1); Serial.print("] | ");

    Serial.print("Q(deg): [");
    Serial.print(degrees(q[0]), 0); Serial.print(", ");
    Serial.print(degrees(q[1]), 0); Serial.print(", ");
    Serial.print(degrees(q[2]), 0); Serial.println("]");
    
    lastPrintTime = millis();
  }
}