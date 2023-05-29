import matlab.engine

class Sonido:
    def __init__(self):
        # Se inicializa en engine
        self.eng = matlab.engine.start_matlab()
        # Se agrega la dirección del directorio del archivo
        self.eng.addpath('Matlab', nargout=0)
        # Llamamos la clase alojada en el archivo
        self.myobj = self.eng.Sound()


    def grabarAudio(self, path, fs):
        r'''
        El path debe de contener el nombre del archivo.
        ej. \ubicacion\nombre.waw
        '''
        self.eng.recordAudio(self.myobj, path, fs)


    def syncYPromeGrabaciones(self, folderPath, outputFilePath):
        '''
        Esta función va a tomar todos los archivos .wav de una carpeta
        los va a alinear y va a tomar sus promedios para luego guardarlo en
        una carpeta de salida
        '''
        self.eng.synchronizeAndAverageRecordings(self.myobj, folderPath, outputFilePath)
    

    def compararFFT(self, path_wav, path_record):
        r'''
        Va a retornar el resultado numérico de la distancia euclidiana entre las dos funciones
        de fft.
        Es necesario poner el nombre del archivo en la dirección
        ej. \ubicacion\nombre.waw
        '''
        diferencia = self.eng.compareFFT(self.myobj, path_wav, path_record)

        if 6750 < diferencia < 7150:
            return True
        else:
            return False
    
    def grabarYCompararSonido(self):
        pass


class interfaz_metodo:
    pass