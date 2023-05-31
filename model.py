import matlab.engine
from threading import Thread
# import speech_recognition as sr
import concurrent.futures
import pygame

# Metodos traidos de matlab
class Sonido:
    def __init__(self):
        # Se inicializa en engine
        self.eng = matlab.engine.start_matlab()
        # Se agrega la dirección del directorio del archivo
        self.eng.addpath('Matlab', nargout=0)
        # Llamamos la clase alojada en el archivo
        self.myobj = self.eng.Sound()


    def grabarAudio(self, path="", fs=3, write=False):
        r'''
        El path debe de contener el nombre del archivo.
        ej. \ubicacion\nombre.waw
        '''
        self.eng.recordAudio(self.myobj, path, fs, write)


    def syncYPromeGrabaciones(self, folderPath, outputFilePath):
        '''
        Esta función va a tomar todos los archivos .wav de una carpeta
        los va a alinear y va a tomar sus promedios para luego guardarlo en
        una carpeta de salida
        '''
        self.eng.synchronizeAndAverageRecordings(self.myobj, folderPath, outputFilePath)
    

    def compararDEE(self, path_wav, fs=0.6, rango=[0, 1100]):
        r'''
        Va a retornar el resultado numérico de la distancia euclidiana entre las dos funciones
        de fft.
        Es necesario poner el nombre del archivo en la dirección
        ej. \ubicacion\nombre.waw
        '''
        if rango[0] < self.eng.compareDEE(self.myobj, path_wav, fs) < rango[1]:
            return True
        else:
            return False
    
    def grabarYCompararSonido(self):
        pass

    # Reconocimiento de voz en tiempo real
    def reconocimiento_voz():
        r = sr.Recognizer()

        with sr.Microphone() as source:

            while True:
                audio = r.listen(source)
                try:
                    comando = r.recognize_google(audio)
                    print("Comando reconocido:", comando)
                except:
                    pass

# Clase que crea un hilo para que se ejecute las grabaciones y el análisis en segundo plano
class SoundRecorder(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.recording = False
        self.sound = Sonido()

    def run(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            while self.recording:
                # Define las funciones que deseas ejecutar simultáneamente
                functions = [
                    executor.submit(self.compare_and_post_event, r'Records\Avareged\start.wav', pygame.K_r),
                    executor.submit(self.compare_and_post_event, r'Records\aja.wav', pygame.K_UP),
                    executor.submit(self.compare_and_post_event, r'Records\cetre.wav', pygame.K_DOWN),
                    executor.submit(self.compare_and_post_event, r'Records\ellas.wav', pygame.K_RIGHT),
                    executor.submit(self.compare_and_post_event, r'Records\si.wav', pygame.K_LEFT)
                ]
                
                # Espera a que todas las funciones se completen
                concurrent.futures.wait(functions, return_when=concurrent.futures.ALL_COMPLETED)


            if self.sound.compararDEE(r'Records\si.wav'):
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))

    def start_recording(self):
        self.recording = True
        self.start()

    def stop_recording(self):
        self.recording = False
        self.join()
    
    def compare_and_post_event(self, filepath, key):
        if self.sound.compararDEE(filepath):
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key))

class interfaz_metodo:
    pass

class snake_game:
    pass