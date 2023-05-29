classdef Sound < handle
    properties (Constant)

        FRECUENCIA_MUESTREO = 44100;
        DURACION_GRABACION = 3;
    end
    
    methods (Access = public)
        function audio_data = recordAudio(obj, folderPath, fs)
            
            recObj = audiorecorder(obj.FRECUENCIA_MUESTREO, 16, 1);
            
            % Grabar audio durante la duración especificada
            recordblocking(recObj, fs);
            
            % Obtener los datos grabados
            audio_data = getaudiodata(recObj);
            
            % Guardar los datos grabados en un archivo
            audiowrite(folderPath, audio_data, obj.FRECUENCIA_MUESTREO);         
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
                [recording, sampleRate] = audioread(filePath);
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
            maxDuration = obj.DURACION_GRABACION;
        
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
        

        function distance = compareFFT(obj, path_wav, path_record)
            % Leer el archivo WAV original
            [audio_wav, fs_wav] = audioread(path_wav);
        
            % Leer la grabación de audio desde el archivo WAV de la grabación
            [audio_record, fs_record] = audioread(path_record);
        
            % Realizar la Transformada Rápida de Fourier (FFT)
            fft_audio_wav = fft(audio_wav);
            fft_audio_record = fft(audio_record);
        
            % Calcular la distancia Euclidiana entre los vectores de características
            distance = norm(fft_audio_wav - fft_audio_record);
        
            % Mostrar el resultado de la comparación
            fprintf('La distancia Euclidiana entre los espectros de frecuencia es: %f\n', distance);
        end
    end
end