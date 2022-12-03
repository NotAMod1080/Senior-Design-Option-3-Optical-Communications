from gpiozero import LED
from time import sleep

led = LED(17)

while True:
    led.on()
    print("LED should be on...\n")
    sleep(1)
    led.off()
    print("LED should be off\n")
    sleep(1)