# Anulación de Ruido con ANC y Resonadores de Helmholtz

## Descripcion

Este proyecto implementa un sistema de anulación de ruido combinando Control Activo de Ruido 
(ANC, Active Noise Control) y Resonadores de Helmholtz. La combinación de ambas técnicas permite
reducir eficazmente el ruido en un entorno específico, aprovechando la cancelación activa con 
algoritmos de procesamiento digital de señales y la absorción pasiva mediante resonadores acústicos.

## Caracteristicas

Control Activo de Ruido (ANC): Utiliza sensores y actuadores para generar señales opuestas a las del ruido objetivo, reduciendo su amplitud por interferencia destructiva.
Resonadores de Helmholtz: Diseñados para absorber frecuencias específicas del ruido mediante cavidades resonantes.

## Requisitos

''
pip install numpy scipy matplotlib sounddevice
''

## Uso

Ejecuta el código principal para realizar pruebas de cancelación de ruido:
''
python main.py
''




