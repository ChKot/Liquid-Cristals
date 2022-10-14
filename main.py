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

# def med_filter(data, N):
#     temp_arr = []
#     temp_arr2 = []
#     y = []
#     for i in range(0, N):
#         temp_arr.append(0)
#     for i in range(np.shape(data)[0]):
#         for j in range(0, N-1):
#             temp_arr[j] = temp_arr[j+1]
#         temp_arr[N-1] = data[i, 1]
#         for j in range(0, N):
#             temp_arr2[j] = temp_arr[j]
#         temp_arr2.sort()
#         if i >= N:
#             if N % 2:
#                 y.append((temp_arr2[N/2]+temp_arr2[(N/2)-1])/2)
#             else:
#                 y.append(temp_arr2[N])
#         else:
#             y.append(data[i, 1])
#     return y

arduino = serial.Serial('COM4', 1000000, timeout=1)
time.sleep(2)
arduino.write('s10000000'.encode())
time.sleep(0.5)
while not arduino.in_waiting:
    time.sleep(0.01)
data = np.array([0, 0])
buff = []

while True:
    d_byte = arduino.read(6)
    if d_byte:
        buff.append(d_byte)
    else:
        break

for i in buff:
    t = int.from_bytes(i[2:], 'little')
    value = int.from_bytes(i[:2], 'little')
    print(f'{t} -> {value}')
    row = [t, value]
    data = np.vstack([data, row])

filtred_data1 = mid_filter(data, 6)
data= np.column_stack([data, filtred_data1])
# filtred_data2 = med_filter(data, 6)
# data= np.column_stack([data, filtred_data2])
# print(data)
# print(data[1])
# print(np.shape(data))

t_name = time.localtime()
name = time.strftime("%H_%M_%S", t_name)
np.savetxt(f'./data/{name}.csv', data, delimiter=',', fmt='%s')

plt.plot(data[:, 0], data[:, 1], '.-')
plt.plot(data[:, 0], data[:, 2], '.-')
plt.grid(linestyle='-', linewidth=1)
plt.show()