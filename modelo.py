import matlab.engine

class Sonido:
    def __init__(self):
        self.eng = matlab.engine.start_matlab('-desktop')
        self.eng.addpath('Matlab', nargout=0)
        self.myobj = self.eng.Sound()

    def grabarAudio(self, path):
        self.eng.recordAudio(self.myobj, path)

    def syncYPromeGrabaciones(self, folderPath, outputFilePath):
        # Los path tienen que ser carpetas
        self.eng.synchronizeAndAverageRecordings(self.myobj, folderPath, outputFilePath)
    
    def compararFFT(self, path_wav, path_record):
        return self.eng.compareFFT(self.myobj, path_wav, path_record)


class interfaz_metodo:
    pass

sonido = Sonido()
sonido.grabarAudio(r'Records\down\adios.wav')
# print(sonido.compararFFT(r"C:\Users\Usuario\Desktop\JUAN\FINAL_METODOS\Records\up\grabacion5.wav", r"C:\Users\Usuario\Desktop\JUAN\FINAL_METODOS\Records\Avareged\a.wav"))