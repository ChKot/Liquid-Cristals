import matplotlib.pyplot as plt
import serial
import time
import numpy as np


def mid_filter(data, N):
    temp_arr = []
    y = []
    for i in range(0, N):
        temp_arr.append(0)
    for i in range(np.shape(data)[0]):
        for j in range(0, N-1):
            temp_arr[j] = temp_arr[j+1]
        temp_arr[N-1] = data[i, 1]
        if i >= N:
            y.append(sum(temp_arr)/N)
        else:
            y.append(data[i, 1])
    return y

def med_filter(data, N):
    temp_arr = []
    temp_arr2 = []
    y = []
    for i in range(0, N):
        temp_arr.append(0)
        temp_arr2.append(0)
    for i in range(np.shape(data)[0]):
        for j in range(0, N-1):
            temp_arr[j] = temp_arr[j+1]
        temp_arr[N-1] = data[i, 1]
        for j in range(0, N-1):
            temp_arr2[j] = temp_arr[j]
        temp_arr2.sort()
        if i >= N:
            if N % 2:
                y.append(temp_arr2[N / 2])
            else:
                y.append((temp_arr2[int(N / 2)] + temp_arr2[int((N / 2) - 1)]) / 2)
        else:
            y.append(data[i, 1])
    return y

arduino = serial.Serial('COM5', 1000000, timeout=1)     #тут поставить нужный компорт, но должен быть 5й
time.sleep(2)
arduino.write('s1000000'.encode())          #то что после s - время процесса в мк секундах
time.sleep(0.05)
while not arduino.in_waiting:
    time.sleep(0.01)
data = np.array([0, 0, 0, 0])
buff = []

while True:
    d_byte = arduino.read(8)
    if d_byte:
        buff.append(d_byte)
    else:
        break

for i in buff:
    t = int.from_bytes(i[4:], 'little')
    value = int.from_bytes(i[:2], 'little')
    valueBtm = int.from_bytes(i[2:4], 'little')
    diriv = valueBtm/value
    print(f'{t} -> {value} -> {valueBtm}')
    row = [t, value, valueBtm, diriv]
    data = np.vstack([data, row])

# filtred_data1 = mid_filter(data, 12)
# data= np.column_stack([data, filtred_data1])
# filtred_data2 = med_filter(data, 6)
# data= np.column_stack([data, filtred_data2])


t_name = time.localtime()
name = time.strftime("%H_%M_%S", t_name)
np.savetxt(f'./data/{name}.csv', data, delimiter=',', fmt='%s')

fig = plt.figure()
plt.plot(data[:, 0], data[:, 1], '.-')
plt.plot(data[:, 0], data[:, 2], '.-')
plt.plot(data[:, 0], data[:, 3], '.-')
