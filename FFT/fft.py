from Maix import GPIO, I2S, FFT
from board import board_info
from fpioa_manager import fm
import image, lcd, math, sensor, time

sample_rate = 38640
sample_points = 1024
fft_points = 512
hist_x_num = 50

lcd.init(freq=15000000)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)

fm.register(20, fm.fpioa.I2S0_IN_D0, force=True)
fm.register(19, fm.fpioa.I2S0_WS, force=True)
fm.register(18, fm.fpioa.I2S0_SCLK, force=True)

rx = I2S(I2S.DEVICE_0)
rx.channel_config(rx.CHANNEL_0, rx.RECEIVER, align_mode = I2S.STANDARD_MODE)
rx.set_sample_rate(sample_rate)

if hist_x_num > 320:
    hist_x_num = 320
hist_width = int(320 / hist_x_num)

x_shift = 0

clock = time.clock()

while True:
    clock.tick()
    img = sensor.snapshot()
    audio = rx.record(sample_points)

    fft_res = FFT.run(audio.to_bytes(), fft_points)
    fft_amp = FFT.amplitude(fft_res)

    img = img.clear()
    print("FPS:%.3f"%clock.fps())
    img = img.draw_string(1, 10, "FPS:%.3f"%clock.fps())

    x_shift = 0
    for i in range(hist_x_num):
        if fft_amp[i] > 240:
            hist_height = 240
        else:
            hist_height = fft_amp[i]

        img = img.draw_rectangle((x_shift, 240-hist_height, hist_width,hist_height),\
                                [255,255,255], 2, True)
        x_shift = x_shift + hist_width
    a = lcd.display(img)
    fft_amp.clear()

