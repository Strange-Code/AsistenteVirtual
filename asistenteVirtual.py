from selenium import webdriver
import time
from speech_recognition import Microphone, Recognizer, AudioFile, UnknownValueError, RequestError
from gtts import gTTS
from playsound import playsound
import random

#DECLARAR VARIABLES UNIVERSALES
validaAuth = False
browser = webdriver


def validaQR():
    try:
        element = browser.find_element_by_tag_name("canvas")
    except:
        return False
    return True

def buscarChat(nombreChat : str):
    print("BUSCANDO CHAT : ", nombreChat)
    elements = browser.find_elements_by_tag_name("span")
    for element in elements:
        print("CHAT ENCONTRADO : " + str(element.text).lower())
        if element.text !='' and nombreChat.__contains__(str(element.text).lower()):
            element.click()
            return
    print("NO ENCONTRO CHAT")

def escribir(texto):
    print("escribiendo...")
    cajitaDeTexto = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    cajitaDeTexto.send_keys(texto)

def enviar():
    print("enviado...")
    enviar = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]')
    enviar.click()

def bootWhatsapp():
    browser.get("https://web.whatsapp.com/")
    time.sleep(5)

    ##variable de espera
    espera = True
    print("AUTENTICATE POR FAVOR")

    while espera:
        espera = validaQR()
        time.sleep(2)
        if espera == False:
            global validaAuth
            validaAuth = True
            print("SE AUTENTICO")
            break

def activarAsistente():
    escuchar()
    while True:
        time.sleep(1)

def escuchar():
    print("Escuchando...")
    recognizer =  Recognizer()
    microfono =  Microphone()

    with microfono:
        recognizer.adjust_for_ambient_noise(microfono)
    
    recognizer.listen_in_background(microfono,callback)

def callback(recognizer, source):
    print("Reconociendo...")

    try:
        reconocer = recognizer.recognize_google(source, language='es-ES')
        texto = str(reconocer).lower()
        print("Escuche : ", texto)
        if(texto.__contains__("eva")):
            print("Llamo a eva")
            texto = texto.replace("eva","")
            accion(texto)
        return

    except RequestError as exc:
        print("Error al escuhar : ", exc)
    except UnknownValueError:
        print("No entendi :c")
        playsound('./resource/errorRespuesta.mp3')
        time.sleep(1)

def accion(texto: str):
    
    print("Reconociendo accion...")

    if(texto.__contains__("abrir whatsapp")):
        print("Abriendo whatsapp...")
        playsound('./resource/abrirwts.mp3')
        time.sleep(1)
        global browser
        browser = webdriver.Edge(executable_path="./driver/edgedriver")
        bootWhatsapp()

    if(texto.__contains__("enviar mensaje a")):
        if(validaAuth == False):
            
            print("Autenticate por favor")
            playsound('./resource/abrirwts.mp3')
            time.sleep(1)
            return
        
        texto = texto.replace("enviar mensaje a", "")
        buscarChat(texto)
        return
    
    if(texto.__contains__("escribir")):
        texto = texto.replace("escribir", "")
        escribir(texto)
        return

    if(texto.__contains__("enviar")):
       enviar()
       return

    if(texto.__contains__("cuenta un chiste")):
        chiste()
        return

    if(texto.__contains__("cerrar explorador")):
        print("cerrando browser...")
        browser.close()
        return
    
    print("Accion no encontrada...")
    return

def chiste():
    print("CONTANDO CHISTE...")
    aleatorio = random.randrange(2)
    
    print("CONTANDO CHISTE : ", str(aleatorio))

    if(aleatorio == 1):
      playsound('./resource/obligame.mp3')
      #playsound('./resource/chiste1.mp3')
    else:
      playsound('./resource/chiste2.mp3')
    
    time.sleep(1)
    return

def hablar(texto: str):
    print("Hablando...")
    audio = gTTS(text=texto,lang='es-us',slow=False)
    audio.save('./resource/obligame.mp3')
    #time.sleep(1)
    #playsound('./resource/chiste1.mp3')
    return



activarAsistente() 
#hablar('obligame perro')