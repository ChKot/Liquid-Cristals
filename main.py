import matplotlib.pyplot as plt
import serial
import time
import numpy as np
import pandas as pd

arduino = serial.Serial('COM3', 250000, timeout=1)
time.sleep(2)
arduino.write('s900000'.encode())
time.sleep(2)
data = np.array([0, 0])
raw_data = []
time_data = []
filt_data_exp = []
filt_exp_last = 0
teta = 0.5
while True:
    try:
        buff = arduino.read(6)
        t = buff[2] | (buff[3] << 8) | (buff[4] << 16) | (buff[5] << 24)
        value = buff[0] | (buff[1] << 8)
        print(f'{t} -> {value}')
        row = [int(t), int(value)]
        data = np.vstack([data, row])
    except IndexError:
        break

# plt.plot(data[:, 0], data[:, 1], '.-')
# plt.grid(linestyle='-', linewidth=1)
# plt.show()


def exp_filter(data, teta):
    y_last= 0
    y = []
    for i in range(np.shape(data)[0]):
        if i == 1 or i == 0:
            y.append(data[i, 1])
            y_last= data[i, 1]
        else:
            y.append(y_last + teta * (data[i, 1] - y_last))
            y_last = data[i, 1]
    return y
filtred_data = exp_filter(data, 0.3)
data= np.column_stack([data, filtred_data])
print(data)
print(data[1])
print(np.shape(data))

t_name = time.localtime()
name = time.strftime("%H_%M_%S", t_name)
np.savetxt(f'./data/{name}.csv',data,delimiter=',', fmt='%s')