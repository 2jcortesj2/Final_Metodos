import matlab.engine
from threading import Thread
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
    

    def compararDEE(self, path_wav, fs=1, rango=[0, 1100]):
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

# Clase que crea un hilo para que se ejecute las grabaciones y el análisis en segundo plano
class SoundRecorder(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.recording = False
        self.sound = Sonido()

    def run(self):
        while self.recording:
            # Process the recorded sound data as needed
            if self.sound.compararDEE(r'Records\start.wav'):
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))


            if self.sound.compararDEE(r'Records\up.wav'):
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))


            if self.sound.compararDEE(r'Records\down.wav'):
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))


            if self.sound.compararDEE(r'Records\right.wav'):
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))


            if self.sound.compararDEE(r'Records\left.wav'):
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))



    def start_recording(self):
        self.recording = True
        self.start()

    def stop_recording(self):
        self.recording = False
        self.join()

class interfaz_metodo:
    pass

class snake_game:
    pass