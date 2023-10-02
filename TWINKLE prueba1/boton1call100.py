import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(4)
    if input_state == False:
        os.system('./prueba1expect.sh')

