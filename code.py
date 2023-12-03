import analogio
import digitalio
from board import GP15, GP26_A0, GP27_A1
import digitalio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

keyboard = Keyboard(usb_hid.devices)

pin_x = GP26_A0  # Pin analógico para la coordenada X del joystick
pin_y = GP27_A1  # Pin analógico para la coordenada Y del joystick
button_pin = GP15  # Pin digital para el botón del joystick

# Configuración del ADC
adc_x = analogio.AnalogIn(pin_x)
adc_y = analogio.AnalogIn(pin_y)
button_pin = digitalio.DigitalInOut(button_pin)
button_pin.switch_to_input(pull=digitalio.Pull.UP)


# Función para leer el estado del joystick
def leer_joystick():
    x = adc_x.value
    y = adc_y.value

    resolved_x = 0

    if x > 40000:
        resolved_x = 1
    elif x < 20000:
        resolved_x = -1
    else:
        resolved_x = 0

    resolved_y = 0

    if y > 40000:
        resolved_y = 1
    elif y < 20000:
        resolved_y = -1
    else:
        resolved_y = 0

    boton_presionado = not button_pin.value

    return resolved_x, resolved_y, boton_presionado

def resolveWASD(x,y):
    if x == 0 and y == 0:
        keyboard.release(Keycode.D)
        keyboard.release(Keycode.A)
        keyboard.release(Keycode.W)
        keyboard.release(Keycode.S)
        return
    if x == -1:
        keyboard.release(Keycode.A)
        keyboard.press(Keycode.D)
    elif x == 1:
        keyboard.release(Keycode.D)
        keyboard.press(Keycode.A)
    
    if y == -1:
        keyboard.release(Keycode.S)
        keyboard.press(Keycode.W)
    elif y == 1:
        keyboard.release(Keycode.W)
        keyboard.press(Keycode.S)

# Bucle principal
while True:
    estado_x, estado_y, boton_presionado = leer_joystick()
    resolveWASD(estado_x,estado_y)

    print("Coordenada X:", estado_x)
    print("Coordenada Y:", estado_y)
    print("Botón presionado:", boton_presionado)

    time.sleep(0.1)
