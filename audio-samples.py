# Tony Goodhew - poor sound output
# https://forums.pimoroni.com/t/presto-sounds/27025/8
import machine
import utime
import array #, time
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

def play_r2d2():
    # based on https://antirez.com/news/143
    pwm.freq(100000)

    f = open("r2d2.raw","rb")
    buf = bytearray(4096)

    while f.readinto(buf) > 0:
        for sample in buf:
            pwm.duty_u16(sample<<8)
            utime.sleep(0.0001)
            utime.sleep(0.0001) 
            utime.sleep(0.0001) 
            utime.sleep(0.0001) 
            utime.sleep(0.0001) 
    f.close()

def play_imperial_march():
    # based on https://antirez.com/news/143
    pwm.freq(100000)

    f = open("imperial_march.raw","rb")
    buf = bytearray(4096)

    while f.readinto(buf) > 0:
        for sample in buf:
            pwm.duty_u16(sample<<8)
            utime.sleep(0.0001) 
            utime.sleep(0.0001)  
            utime.sleep(0.0001)  
            utime.sleep(0.0001)  
            utime.sleep(0.0001)  
            utime.sleep(0.0001)  
            utime.sleep(0.0001)  
            utime.sleep(0.0001)  
    f.close()

clear_screen()
message("PWM Sound Test")

pwm = PWM(Pin(43))

play_r2d2()
play_imperial_march()

pwm.deinit()
clear_screen()
message("Finish...you can reboot")
