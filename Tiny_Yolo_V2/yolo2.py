import sensor, image, lcd, time
import KPU as kpu

lcd.init(freq=15000000, invert=1)#
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)
sensor.run(1)

clock = time.clock()

classes = ['plane', 'bicycle', 'bird',
           'boat', 'bottle', 'bus', 'car',
           'cat', 'chair', 'cow', 'diningtable',
           'dog', 'horse', 'motorbike',
           'person', 'pottedplant', 'sheep',
           'sofa', 'train', 'monitor']
task = kpu.load("yolo2.kmodel")
anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)

while(True):
    clock.tick()
    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img)
    #print("FPS:%.3f"%clock.fps())
    img = img.draw_string(1,10,"FPS:%.3f"%clock.fps())
    if code:
        for i in code:
            img = img.draw_rectangle(i.rect())
            for i in code:
                img = img.draw_string(i.x(), i.y(), classes[i.classid()])
                img = img.draw_string(i.x(), i.y()+12, "%.3f"%i.value())
    lcd.display(img)
kpu.deinit(task)
