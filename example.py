from KDC101_control import KDC101
import time


sn_num = str("27261381")
device = KDC101()
device.init(sn_num)
device.home()

while device.device_state():
    pos = device.get_position()
    print(pos)
    time.sleep(0.2)
    if pos == 0:
        break
time.sleep(15)

device.set_movespeed(0.005, 0.02)
device.move_to(0.1)
time.sleep(1)

while device.device_state():
    pos = device.get_position()
    print(pos)
    time.sleep(0.2)
    if pos == 1:
        break
time.sleep(2)
print(device.get_position())

device.disconnect()


