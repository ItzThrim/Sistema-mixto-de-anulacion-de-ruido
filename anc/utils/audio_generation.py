import numpy as np
import soundfile as sf


def create_signal(frequency, duration, sampling=44100, filename="signal.wav"):
    """
    Crea una señal sinusoidal en mono y la guarda en un archivo WAV.

    Parámetros:
        frequency (float): Frecuencia de la señal en Hz.
        duration (float): Duración de la señal en segundos.
        sampling (int): Tasa de muestreo en Hz (por defecto 44100).
        filename (str): Nombre del archivo de salida.
    """
    time = np.linspace(0, duration, int(sampling * duration), endpoint=False)

    wave = 0.5 * np.sin(2 * np.pi * frequency * time).astype(np.float32)

    sf.write(filename, wave, sampling, subtype="PCM_16")


def create_signal_with_noise(
    frequency,
    duration,
    sampling=44100,
    noise_level=0.1,
    filename="signal_with_noise.wav",
):
    """
    Crea una señal sinusoidal con ruido añadido y la guarda en un archivo WAV.

    Parámetros:
        frequency (float): Frecuencia de la señal en Hz.
        duration (float): Duración de la señal en segundos.
        sampling (int): Tasa de muestreo en Hz (por defecto 44100).
        noise_level (float): Nivel de ruido (amplitud relativa a la señal).
        filename (str): Nombre del archivo de salida.
    """
    time = np.linspace(0, duration, int(sampling * duration), endpoint=False)

    wave = 0.5 * np.sin(2 * np.pi * frequency * time).astype(np.float32)

    noise = noise_level * np.random.randn(len(time)).astype(np.float32)

    signal_with_noise = wave + noise

    signal_with_noise = signal_with_noise / np.max(np.abs(signal_with_noise))

    sf.write(filename, signal_with_noise, sampling, subtype="PCM_16")


create_signal(440, 10, filename="../data/raw/440.wav")
create_signal_with_noise(
    440, 10, noise_level=0.5, filename="../data/raw/440_with_noise.wav"
)
