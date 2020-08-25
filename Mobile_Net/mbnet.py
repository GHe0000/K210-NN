import sensor, image, lcd, time
import KPU as kpu

lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.set_vflip(1)
sensor.run(1)

lcd.clear()
lcd.draw_string(100, 96, "MobileNet Demo")
lcd.draw_string(100, 112, "Loading labels...")

f=open('labels.txt', 'r')
labels=f.readlines()
f.close()

task = kpu.load("mbnet.kmodel")
clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    fmap = kpu.forward(task, img)
    print("FPS:%.3f"%clock.fps())
    img = img.draw_string(1,10,"FPS:%.3f"%clock.fps())

    plist = fmap[:]
    pmax = max(plist)
    max_index = plist.index(pmax)
    img = img.draw_string(1, 224, "%.3f:%s"%(pmax, labels[max_index].strip()))
    a = lcd.display(img)

a = kpu.deinit(task)
