import numpy as np
import soundfile as sf


def remove_noise_fft(
    filename="signal_with_noise.wav",
    output_filename="filtered_signal.wav",
    target_freq=440,
    bandwidth=50,
    sampling_rate=44100,
):
    """
    Filtra el ruido en una señal usando FFT eliminando frecuencias fuera del rango de la señal objetivo.

    Parámetros:
        filename (str): Archivo de entrada con ruido.
        output_filename (str): Archivo de salida filtrado.
        target_freq (float): Frecuencia objetivo (Hz) a conservar.
        bandwidth (float): Rango de frecuencias permitido alrededor de target_freq.
        sampling_rate (int): Frecuencia de muestreo de la señal.
    """
    wave, sampling = sf.read(filename)

    fft_wave = np.fft.fft(wave)
    freqs = np.fft.fftfreq(len(wave), 1 / sampling_rate)

    # Filtrar frecuencias fuera del rango deseado
    mask = (freqs > target_freq - bandwidth) & (freqs < target_freq + bandwidth)
    filtered_fft = np.where(mask, fft_wave, 0)

    # Transformada inversa para reconstruir la señal
    filtered_wave = np.fft.ifft(filtered_fft).real

    # Guardar el archivo filtrado
    sf.write(output_filename, filtered_wave, sampling, subtype="PCM_16")


remove_noise_fft("../data/raw/440_with_noise.wav", "../data/raw/440_filtered.wav")
