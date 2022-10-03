import matplotlib.pyplot as plt
import serial
import time
import numpy as np
import pandas as pd

while True:
    print('Print "exit" to close program')
    command = input('-> ')
    arduino = serial.Serial('COM9', 250000, timeout=1)
    if command == 'exit':
        break
    elif 's' in command:
        if not arduino.isOpen():
            arduino.open()
        time.sleep(2)
        arduino.write(command.encode())
        time.sleep(2)
        data = np.array([0, 0])
        # raw_data = []
        # time_data = []
        # filt_data_exp = []
        # filt_exp_last = 0
        # teta = 0.5
        while True:
            buff = arduino.read(6)
            if buff:
                t = int.from_bytes(buff[2:], 'little')
                value = int.from_bytes(buff[:2], 'little')
                print(f'{t} -> {value}')
                # raw_data.append(value)
                # time_data.append(t)
                # filt_exp = filt_exp_last + teta * (value - filt_exp_last)
                # filt_exp_last = filt_exp
                # filt_data_exp.append(filt_exp)
                row = [int(t), int(value)]
                data = np.vstack([data, row])
            else:
                break

        plt.plot(data[:, 0], data[:, 1], '.-')
        plt.grid(linestyle='-', linewidth=1)
        plt.show()
        arduino.close()
    else:
        print(command)
        arduino.close()

# columns = {'time_data': time_data, 'raw_data': raw_data, 'exp_filter': filt_data_exp}
# data_df = pd.DataFrame(columns)

# plt.subplot (1, 1, 1)
# plt.plot(data_df['time_data'], data_df['raw_data'])
# plt.plot(data_df['time_data'], data_df['exp_filter'])
# plt.grid(linestyle='-', linewidth=1)
# plt.show()

# t = time.localtime()
# current_time = time.strftime("%H_%M_%S", t)
# data_df.to_excel(f'./{current_time}.xlsx')
