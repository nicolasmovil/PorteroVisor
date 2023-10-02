import RPi.GPIO as GPIO
import sounddevice as sd
import numpy as np

# Definición de los pines GPIO para los LEDs
pin_led4 = 16
pin_led3 = 26
pin_led2 = 13
pin_led1 = 6

# Configuración de los pines GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_led1, GPIO.OUT)
GPIO.setup(pin_led2, GPIO.OUT)
GPIO.setup(pin_led3, GPIO.OUT)
GPIO.setup(pin_led4, GPIO.OUT)

# Función para procesar el audio
def audio_callback(indata, frames, time, status):
    if status:
        print(status, flush=True)

    # Calcula la intensidad promedio del audio
    audio_intensity = np.abs(indata).mean()

    # Ajusta el umbral de detección de sonido según sea necesario
    umbral = 0.1

    if audio_intensity > umbral:
        print("Sonido detectado!")

        # Calcula el número de LEDs a encender basado en el nivel de decibeles
        num_leds = int(audio_intensity * 10)  # Puedes ajustar este factor según tu preferencia

        # Asegura que el número de LEDs esté en el rango de 1 a 4
        num_leds = min(max(num_leds, 1), 4)

        # Enciende los LEDs correspondientes
        for i in range(num_leds):
            GPIO.output([pin_led1, pin_led2, pin_led3, pin_led4][:num_leds], GPIO.HIGH)
            
    else:
        # Apaga todos los LEDs si no se detecta suficiente sonido
        
        GPIO.output([pin_led1, pin_led2, pin_led3, pin_led4], GPIO.LOW)

# Configuración de SoundDevice
sample_rate = 44100
duration = 60  # Duración de la captura en segundos

with sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate):
    sd.sleep(duration * 1000)

# Limpiar los pines GPIO al finalizar
GPIO.cleanup()

