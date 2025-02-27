import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import soundfile as sf


def animate_wave(
    filename="signal.wav",
    output_filename="wave_animation.mp4",
    duration_to_plot=0.02,
    fps=30,
    speed_factor=3,
    bitrate=3000,
    title="",
):
    """
    Genera una animación de la onda de audio cargada desde un archivo WAV y la guarda en formato MP4.

    Parámetros:
        filename (str): Ruta del archivo de audio a animar.
        output_filename (str): Nombre del archivo de salida en formato MP4.
        duration_to_plot (float): Duración en segundos de la onda que se mostrará.
        fps (int): Cuadros por segundo de la animación.
        speed_factor (int): Controla la velocidad de la animación (más alto = más rápido).
        bitrate (int): Calidad del video (más alto = mejor calidad).
    """

    # Cargar la señal desde el archivo
    wave_data, sampling = sf.read(filename)

    # Seleccionar solo los primeros 'duration_to_plot' segundos para la animación
    num_samples = int(sampling * duration_to_plot)
    wave_data = wave_data[:num_samples]
    time = np.linspace(0, duration_to_plot, num_samples)

    # Determinar los límites de la amplitud de forma automática
    amp_max = np.max(np.abs(wave_data)) * 1.1  # Ajuste para dar un margen extra

    # Crear la figura con mayor tamaño
    fig, ax = plt.subplots(
        figsize=(12, 5)
    )  # Aumentado tamaño para mejorar visualización
    ax.set_xlim(time[0], time[-1])
    ax.set_ylim(-amp_max, amp_max)  # Límites de amplitud dinámicos
    ax.set_xlabel("Tiempo [s]", fontsize=16, fontweight="bold", labelpad=10)
    ax.set_ylabel("Amplitud", fontsize=16, fontweight="bold", labelpad=10)
    ax.set_title(title, fontsize=14, fontweight="bold")

    (line,) = ax.plot([], [], lw=2, color="b")

    # Función de actualización para la animación
    def update(frame):
        index = frame * speed_factor  # Salta frames para acelerar la animación
        if index >= len(time):  # Evita que la animación salga del rango
            index = len(time) - 1
        line.set_data(time[:index], wave_data[:index])
        return (line,)

    # Crear la animación con menos frames para hacerla más rápida
    frames_to_use = len(time) // speed_factor
    ani = animation.FuncAnimation(
        fig, update, frames=frames_to_use, interval=1000 / fps, blit=True
    )

    # Guardar la animación como MP4 en la ruta ../data/animations/
    writer = animation.FFMpegWriter(fps=fps, bitrate=bitrate)
    ani.save(f"../data/animations/{output_filename}", writer=writer)

    plt.close(fig)  # Cerrar la figura para evitar que se muestre en pantalla


# Generar animaciones con mayor calidad en MP4
# animate_wave(
#     "../data/raw/440_with_noise.wav",
#     "wave_with_noise.mp4",
#     fps=30,
#     speed_factor=3,
#     bitrate=3000,
#     title="Representación Temporal de la Señal Antes del Filtrado",
# )
# animate_wave(
#     "../data/raw/440_filtered.wav",
#     "wave_filtered.mp4",
#     fps=30,
#     speed_factor=3,
#     bitrate=3000,
#     title="Representación Temporal de la Señal Después del Filtrado",
# )


animate_wave(
    "../data/raw/440.wav",
    "440.mp4",
    fps=30,
    speed_factor=3,
    bitrate=3000,
    title="Representación Temporal de la Señal Después del Filtrado",
)
