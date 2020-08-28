import sensor, lcd, time
import KPU as kpu
lcd.init(freq=15000000, invert=1)#
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
    plist = fmap[:]
    pmax = max(plist)
    max_index = plist.index(pmax)
    lcd.draw_string(1, 224, "%.3f:%s"%(pmax, labels[max_index].strip()))
    lcd.draw_string(1,10,"FPS:%.3f"%clock.fps())
    lcd.display(img)
a = kpu.deinit(task)
