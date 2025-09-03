import utime
from machine import Pin, PWM
import rp2
from presto import Presto

# Setup for the Presto display
presto = Presto(full_res=True,ambient_light=True)
display = presto.display

# colours
BLACK = display.create_pen(0, 0, 0)
GREEN = display.create_pen(0, 255, 0)
display.set_font("bitmap8")

# helpers
def clear_screen(): # Clear the screen to Black
    display.set_pen(BLACK)
    display.clear()
    presto.update()

def message(text, color=GREEN):
    display.set_pen(color)
    display.text(text, 10, 10, scale=3)
    presto.update()

def volume_control():
    # based on https://www.samgalope.dev/2025/01/08/pwm-based-audio-generation-with-esp32-a-simple-guide-to-sound-creation/
    def set_volume(volume):
        pwm.duty_u16(volume)
    
    def play_tone(frequency, duration):
        pwm.freq(frequency)
        utime.sleep(duration)

    for volume in [1024, 512, 256, 128]:
        print(f"playing 440Hz at duty cycle {volume}")
        set_volume(volume)
        play_tone(440, 1)

clear_screen()
message("PWM Sound Test")

pwm = PWM(Pin(43))

volume_control()

pwm.deinit()
clear_screen()
message("Finish...you can reboot")
