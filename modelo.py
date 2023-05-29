import matlab.engine

eng = matlab.engine.start_matlab()

class Sonido:
    def __init__(self):
        self.sound = eng.Sound()

    def grabarAudio(self, path):
        self.sound.recordAudio(path)

    def syncYPromeGrabaciones(self, folderPath, outputFilePath):
        # Los path tienen que ser carpetas
        self.sound.synchronizeAndAverageRecordings(folderPath, outputFilePath)
    
    def compararFFT(self, path_wav, path_record):
        return self.sound.compareFFT(path_wav, path_record)


class interfaz_metodo:
    pass

# Crea una instancia de la clase Sound
sound_instance = eng.Sound()

# Llama a los métodos de la clase Sound
sound_instance.recordAudio('Records\down')
# print(sonido.compararFFT(r"C:\Users\Usuario\Desktop\JUAN\FINAL_METODOS\Records\up\grabacion5.wav", r"C:\Users\Usuario\Desktop\JUAN\FINAL_METODOS\Records\Avareged\a.wav"))