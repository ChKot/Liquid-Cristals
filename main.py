import matplotlib.pyplot as plt
import serial
import time
import numpy as np
import pandas as pd

arduino = serial.Serial('COM9', 250000, timeout=1)
time.sleep(2)
arduino.write('s9000000'.encode())
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
        raw_data.append(value)
        time_data.append(t)
        filt_exp = filt_exp_last + teta * (value - filt_exp_last)
        filt_exp_last = filt_exp
        filt_data_exp.append(filt_exp)
        row = [int(t), int(value)]
        data = np.vstack([data, row])
    except IndexError:
        break

# plt.plot(data[:, 0], data[:, 1], '.-')
# plt.grid(linestyle='-', linewidth=1)
# plt.show()

columns = {'time_data': time_data, 'raw_data': raw_data, 'exp_filter': filt_data_exp}
data_df = pd.DataFrame(columns)

# plt.subplot (1, 1, 1)
plt.plot(data_df['time_data'], data_df['raw_data'])
plt.plot(data_df['time_data'], data_df['exp_filter'])
plt.grid(linestyle='-', linewidth=1)
plt.show()

# t = time.localtime()
# current_time = time.strftime("%H_%M_%S", t)
# data_df.to_excel(f'./{current_time}.xlsx')
