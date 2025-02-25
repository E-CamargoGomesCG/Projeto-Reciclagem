from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import serial


def abrir(nome_da_porta, taxa):
    com = serial.Serial("COM11", taxa)
    return com
 
 #envia a mensagem pro arduino, ex: vidro; ,papel; etcetera

def escreve(com: serial, dados: str):
    #passa letra por letra
    seq_bytes = dados.encode()
    #manda pro arduino letra por letra
    com.write(seq_bytes)

def aguardar(com: serial):
     
      while True:
          #retorna se ta lendo ou nao
          retorno = ler(com)
          print(retorno)
          print("\n")
          if retorno == "desocupado":
                break
                     
def enviarcomando(class_name):
     
      #abre a porta pro arduino
      com = abrir(porta, taxa)
      #manda o que ta se detectando
 
      escreve(com, class_name)
      #imediatamente, manda aguardar, pois tem material na esteira


      aguardar(com)
      


def ler(com):
    mensagem = ""
    lendo = True
    while lendo:
        dado = com.read().decode()
        if dado != ';':
            mensagem = mensagem + dado
        else:
            lendo = False  


        #if not com.in_waiting > 0:
         #lendo = False


         #retorna
    return mensagem


taxa = 9600 #int(input("Informe a velocidade: ")) numero da velocidade]
porta_aberta = True
porta = "COM11" #nome da minha porta aq do PC
com = abrir(porta, taxa)



#carregamento do modelo
model = load_model("keras_Model.h5", compile=False)
class_names = open("labels.txt", "r").readlines()


camera = cv2.VideoCapture(1)


while True:
   
    ret, image = camera.read()
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)


    cv2.imshow("Webcam Image", image)

   
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)


    image = (image / 127.5) - 1


    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    print(class_name)

    if class_name != "vazio\n":
        enviarcomando(class_name)
    #print("Class:", class_name[2:], end="")
   
    keyboard_input = cv2.waitKey(1)

    if keyboard_input == 0:
        break

camera.release()
cv2.destroyAllWindows()