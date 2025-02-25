from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import serial
import serial.tools.list_ports



# envia a mensagem pro arduino, ex: vidro; ,papel; etcetera
def escreve(com: serial, dados: str):
    # passa letra por letra
    seq_bytes = dados.encode()
    # manda pro arduino letra por letra
    com.write(seq_bytes)

def aguardarResposta(com: serial):
    while True:
        # retorna se ta lendo ou nao
        retorno = ler(com)
        print(retorno)
       #print("\n")
        if retorno == "desocupado":
            break

def enviarcomando(com: serial, class_name):
    # abre a porta pro arduino
    #com = abrir(porta, taxa) #Não utilizar pois a porta sera aberta na função main
    # manda o que ta se detectando
    escreve(com, class_name)
    # imediatamente, manda aguardar, pois tem material na esteira
    aguardarResposta(com)


def ler(com):
    mensagem = ""
    lendo = True
    while lendo:
        dado = com.read().decode()
        if dado != ';':
            mensagem = mensagem + dado
        else:
            lendo = False

            # if not com.in_waiting > 0:3
        # lendo = False

        # retorna
    return mensagem

def aguardarNomePortaComunicacao():
    print("Certifique-se de que o Arduino esteja desconectado!\n")
    print("Caso esteja conectado, desconecte-o agora!\n")
    confirmacao = input("Arduino desconectado (S/N)? ")
    if confirmacao=="S" or confirmacao=="s":
        print("Carregando lista de portas existentes\n")
        portasIniciais = serial.tools.list_ports.comports()
    print("Conecte o Arduino agora!")
    confirmacao = input("Arduino conectado (S/N)? ")
    if confirmacao=="S" or confirmacao=="s":
        print("Carregando lista atualizada\n")
        portasAtualizadas = serial.tools.list_ports.comports()
    else:
        exit()

    nome_da_porta = ""
    for portaI in portasAtualizadas:
        porta_nova = True
        for portaII in portasIniciais:
            if portaI.device == portaII.devi66ce:
                porta_nova = False
        if porta_nova == True:
            nome_da_porta = portaI.device
            return nome_da_porta
    print("Nenhuma porta nova conectada!\n")
    if nome_da_porta == "":
        exit()

def aguardarArduino(com: serial):
    prosseguir = False
    while True:
        retorno = ler(com)
        print(retorno)
        print("\n")
        if retorno == "desocupado": #pronto ou desocupado
            break
        else:
            continue

    return prosseguir

def abrir(nome_da_porta, taxa):
    com = serial.Serial("COM11", taxa)
    return com

# INICIA O CÓDIGO PRINCIPAL (O CÓDIGO QUE ESTÁ FORA DOS MÉTODOS)

#Sequencia para abertura da porta.
taxa = 9600
porta_aberta = False
nome_da_porta = aguardarNomePortaComunicacao()
print("Porta encontrada: ", nome_da_porta)
com = abrir(nome_da_porta, taxa)
print("Conectado pela porta: ", com.portstr)

#while aguardarArduino(com) != True:
 #   continue

### A PARTIR DAQUI NÃO FIZ MODIFICACOES

np.set_printoptions(suppress=True)

# carregamento do modelo
model = load_model("keras_Model.h5", compile=False)
class_names = open("labels.txt", "r").readlines()

# Inicia captura do webcam
camera = cv2.VideoCapture(0)

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
        enviarcomando(com, class_name)
    # print("Class:", class_name[2:], end="")

    keyboard_input = cv2.waitKey(1)

    if keyboard_input == 0:
        break

camera.release()
cv2.destroyAllWindows()