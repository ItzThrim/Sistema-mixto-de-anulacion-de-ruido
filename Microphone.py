import pyaudio
import numpy as np
import time
import wave
import matplotlib.pyplot as plt

# Configuración del audio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # Frecuencia de muestreo
CHUNK = 1024  # Tamaño del buffer de audio
DURATION = 5  # Duración de la grabación en segundos

def obtener_frecuencia(datos, tasa_muestreo):
    fft_vals = np.fft.fft(datos)
    fft_freqs = np.fft.fftfreq(len(fft_vals), 1.0 / tasa_muestreo)
    
    # Obtener la frecuencia dominante
    indice = np.argmax(np.abs(fft_vals[:len(fft_vals)//2]))  # Solo parte positiva
    frecuencia = fft_freqs[indice]
    return abs(frecuencia)

def escuchar_microfono():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    
    print("Escuchando...")
    start_time = time.time()
    tiempos = []
    amplitudes = []
    frecuencias = []
    frames = []
    
    try:
        while time.time() - start_time < DURATION:
            data = stream.read(CHUNK, exception_on_overflow=False)
            datos = np.frombuffer(data, dtype=np.int16)
            amplitud = np.max(np.abs(datos))
            frecuencia = obtener_frecuencia(datos, RATE)
            tiempos.append(time.time() - start_time)
            amplitudes.append(amplitud)
            frecuencias.append(frecuencia)
            frames.append(data)
            print(f"Amplitud: {amplitud:.2f}, Frecuencia: {frecuencia:.2f} Hz")
    except KeyboardInterrupt:
        pass
    finally:
        print("Deteniendo...")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # Guardar archivo de audio
        with wave.open("grabacion.wav", "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b"".join(frames))
        print("Archivo grabado como grabacion.wav")
        
        # Graficar resultados
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.plot(tiempos, amplitudes, 'g-', label="Amplitud")
        ax2.plot(tiempos, frecuencias, 'b-', label="Frecuencia")
        
        ax1.set_xlabel('Tiempo (s)')
        ax1.set_ylabel('Amplitud', color='g')
        ax2.set_ylabel('Frecuencia (Hz)', color='b')
        
        plt.title("Evolución de la Amplitud y Frecuencia")
        plt.show()

if __name__ == "__main__":
    escuchar_microfono()
