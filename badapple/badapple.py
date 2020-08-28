import video, time, lcd
from Maix import GPIO
'''
fm.register(34,  fm.fpioa.I2S0_OUT_D1)
fm.register(35,  fm.fpioa.I2S0_SCLK)
fm.register(33,  fm.fpioa.I2S0_WS)
fm.register(8,  fm.fpioa.GPIO0)
'''
lcd.init(freq=15000000, invert=1) #
v = video.open("badapple.avi")
print(v)
v.volume(50)
while True:
    if v.play() == 0:
        print("play end")
        break
v.__del__()
