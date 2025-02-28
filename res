import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import soundfile as sf
from scipy.signal import butter, lfilter
from google.colab import files  # Para descargar archivos en Colab

# Función para filtro pasa bajo
def lowpass_filter(data, cutoff, fs, order=8):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, data)

# Función para filtro pasa alto
def highpass_filter(data, cutoff, fs, order=8):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return lfilter(b, a, data)

# Parámetros de la señal
sampling_rate = 44100  # Frecuencia de muestreo
duration = 10  # Duración en segundos
frequencies = [100, 150, 200, 440]  # Frecuencias presentes
noise_level = 0.5  # Nivel de ruido

# Generar señal
time = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
signal = sum(0.5 * np.sin(2 * np.pi * f * time) for f in frequencies)

# Generar ruido de baja frecuencia (< 250 Hz)
noise = noise_level * np.random.randn(len(time))
noise = lowpass_filter(noise, 250, sampling_rate)
signal_with_noise = signal + noise
sf.write("signal_with_noise.wav", signal_with_noise, sampling_rate)

# Filtrar señal eliminando frecuencias < 250 Hz
filtered_signal = highpass_filter(signal_with_noise, 250, sampling_rate)
sf.write("filtered_signal.wav", filtered_signal, sampling_rate)

# Función para animar la onda
def animate_wave(wave_data, time, output_filename, title, color):
    num_samples = int(sampling_rate * 0.02)  # 20 ms de señal para animar
    wave_data = wave_data[:num_samples]
    time = time[:num_samples]

    amp_max = np.max(np.abs(wave_data)) * 1.1
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_xlim(time[0], time[-1])
    ax.set_ylim(-amp_max, amp_max)
    ax.set_xlabel("Tiempo [s]", fontsize=14, fontweight="bold")
    ax.set_ylabel("Amplitud", fontsize=14, fontweight="bold")
    ax.set_title(title, fontsize=16, fontweight="bold")
    (line,) = ax.plot([], [], lw=2, color=color)

    def update(frame):
        index = frame * 3  # Factor de velocidad
        if index >= len(time):
            index = len(time) - 1
        line.set_data(time[:index], wave_data[:index])
        return (line,)

    frames_to_use = len(time) // 3
    ani = animation.FuncAnimation(fig, update, frames=frames_to_use, interval=1000 / 30, blit=True)
    writer = animation.FFMpegWriter(fps=30, bitrate=3000)
    ani.save(output_filename, writer=writer)
    plt.close(fig)

# Generar animaciones
animate_wave(signal_with_noise, time, "signal_with_noise.mp4", "Señal Original con Ruido", "b")
animate_wave(filtered_signal, time, "filtered_signal.mp4", "Señal Filtrada (> 250 Hz)", "r")

# Descargar archivos
files.download("signal_with_noise.wav")
files.download("filtered_signal.wav")
files.download("signal_with_noise.mp4")
files.download("filtered_signal.mp4")
