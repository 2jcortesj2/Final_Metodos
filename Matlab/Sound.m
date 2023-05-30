classdef Sound < handle
    properties (Constant)

        FRECUENCIA_MUESTREO = 44100;

    end
    
    methods (Access = public)
        function audio_data = recordAudio(obj, folderPath, fs, write)
            
            recObj = audiorecorder(obj.FRECUENCIA_MUESTREO, 16, 1);
            
            % Grabar audio durante la duración especificada
            recordblocking(recObj, fs);
            
            % Obtener los datos grabados
            audio_data = getaudiodata(recObj);
            
            if write
                % Guardar los datos grabados en un archivo
                audiowrite(folderPath, audio_data, obj.FRECUENCIA_MUESTREO);  
            end
        end
        

        function recordings = readWavFilesFromFolder(obj, folderPath)
            % Obtener la lista de archivos WAV en la carpeta
            filePattern = fullfile(folderPath, '*.wav');
            wavFiles = dir(filePattern);
            
            % Crear la celda "recordings"
            recordings = cell(1, numel(wavFiles));
        
            % Leer cada archivo WAV y almacenar las grabaciones de voz en la celda
            for i = 1:numel(wavFiles)
                filePath = fullfile(folderPath, wavFiles(i).name);
                [recording, ~] = audioread(filePath);
                recordings{i} = recording;
            end
        end


        function saveAsWav(obj, signal, filePath)
            % Normalizar la señal entre -1 y 1
            signal = signal / max(abs(signal));
        
            % Escribir la señal en un archivo .wav
            audiowrite(filePath, signal, obj.FRECUENCIA_MUESTREO);
        end
        

        function alignedSignal = alignDuration(obj, signal, targetDuration)
            signalDuration = length(signal);
        
            if signalDuration < targetDuration
                % Extender el signal con ceros para igualar la duración objetivo
                alignedSignal = [signal; zeros(targetDuration - signalDuration, 1)];
            else
                alignedSignal = signal;
            end
        end


        function averagedFeatures = synchronizeAndAverageRecordings(obj, folderPath, outputFilePath)
            % Obtener todas las grabaciones de una carpeta
            recordings = obj.readWavFilesFromFolder(folderPath);

            % Obtener la duración de las grabaciones
            maxDuration = max(cellfun(@length, recordings));
        
            % Sincronizar las grabaciones y obtener segmentos de interés
            segments = cell(size(recordings));
            
            % Umbral para detectar el fin del silencio
            threshold = 0.5;
                for i = 1:numel(recordings)
                    recording = recordings{i};
                    
                    % Encontrar el índice donde termina el silencio
                    endIdx = find(abs(recording) > threshold, 1, 'last');
            
                    % Extraer el segmento de interés a partir del final del silencio
                    segment = recording(endIdx+1:end);
            
                    % Alinear la duración del segmento con la duración máxima
                    segment = obj.alignDuration(segment, maxDuration);
            
                    % Guardar el segmento
                    segments{i} = segment;
                end
        
            % Calcular el promedio de los segmentos
            averagedFeatures = mean(cat(2, segments{:}), 2);
            
            % Guardar el archivo resultante como .wav
            obj.saveAsWav(averagedFeatures, outputFilePath);
        end


        function trimmedRecording = trimRecording(obj, recording)
            % Umbral para detectar el fin del silencio
            threshold = 0.5;
            
            % Encontrar el índice donde termina el silencio
            endIdx = find(abs(recording) > threshold, 1, 'last');
            
            % Extraer el segmento de interés a partir del final del silencio
            trimmedRecording = recording(endIdx+1:end);
        end

        function DEE = procesing_audio(obj, audio_wav)

            % Se normaliza la amplitud (volumen) de la señal en el tiempo.
            audio_wav = audio_wav/max(abs(audio_wav)); 
            
            % Total de muestras.
            N = length(audio_wav);
            
            % Optimización del algoritmo FFT a través de un vector de 
            % muestras que sea una potencia de 2.
            NFFT = 2^nextpow2(N); 

            % Se calcula la transformada de Fourier.
            Y = fft(audio_wav, NFFT); 

            % Como se va a trabajar con señales reales, se recorta el 
            % espectro y se trabaja con el espectro unilateral.
            Y = Y(1:NFFT/2);
            
            % Se calcula el módulo de la transformada.
            Yabs = abs(Y);

            % Densidad espectral de energía de la muestra.
            DEE = Yabs.^2;
        end


        function error = compareDEE(obj, path_wav, fs)

            % Realizamos la grabacion del audio
            record_data = obj.recordAudio('C:\Users\Usuario\Desktop\JUAN\FINAL_METODOS\Records\Avareged\a.wav', fs, false);

            % Leer el archivo WAV original
            [audio_wav, ~] = audioread(path_wav);

            % Aseguramos que ambas señales tengan la misma longitud
            sound_data = obj.alignDuration(record_data, length(audio_wav));

            % Realizar la Transformada Rápida de Fourier (FFT)
            DEE_record_data = obj.procesing_audio(sound_data);
            DEE_audio_wav = obj.procesing_audio(audio_wav);

            error = mean( ...
                abs(DEE_audio_wav(1:length(DEE_audio_wav)/2) - ...
                DEE_record_data(1:length(DEE_audio_wav)/2)) ...
                );
        end
    end
end