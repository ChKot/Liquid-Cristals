#labraries
import tkinter as tk
import matplotlib.pyplot as plt
import serial
import time
import numpy as np


#variables
teta = 0.1
duration = 1000000
duration_txt = ''
data = np.array([0, 0])
arduino = 0

def exp_filter(data_d, teta):
    y_last= 0
    y = []
    for i in range(np.shape(data_d)[0]):
        if i == 1 or i == 0:
            y.append(data_d[i, 1])
            y_last= data_d[i, 1]
        else:
            y.append(y_last + teta * (data_d[i, 1] - y_last))
            y_last = data_d[i, 1]
    return y

def save_settings():   #btn_set command function
    global teta
    teta = ent_filter.get()
    global duration
    duration = ent_time.get()*1000
    btn_set['text'] = 'Настройки сохранены'

def start():    #btn_start command function
    global duration_txt
    global arduino
    global duration
    global data
    duration_txt = f's{duration}'
    arduino = serial.Serial('COM3', 250000, timeout=1)
    time.sleep(2)
    arduino.write(f'{duration_txt}'.encode())
    time.sleep(2)

    while True:
        try:
            buff = arduino.read(6)
            t = buff[2] | (buff[3] << 8) | (buff[4] << 16) | (buff[5] << 24)
            value = buff[0] | (buff[1] << 8)
            row = [int(t), int(value)]
            data = np.vstack([data, row])
        except IndexError:
            break

    filtred_data = exp_filter(data, 0.3)
    data = np.column_stack([data, filtred_data])

    t_name = time.localtime()
    name = time.strftime("%H_%M_%S", t_name)
    np.savetxt(f'./data/{name}.csv', data, delimiter=',', fmt='%s')

    plt.plot(data[:, 0], data[:, 1], '.-')
    plt.plot(data[:, 0], data[:, 2], '.-')
    plt.grid(linestyle='-', linewidth=1)
    plt.show()

#tkinter window settings
window = tk.Tk()

for i in range(3):
    window.columnconfigure(i, weight=1, minsize=100)
    window.rowconfigure(i, weight=1, minsize=75)

frm_settings = tk.Frame(master=window, width=150, height=150)
frm_settings.grid(row=0, column=0, padx=5, pady=5)

lbl_time = tk.Label(master=frm_settings, text='Время процесса(мс):')
lbl_time.grid(row=0, column=0)

lbl_filter = tk.Label(master=frm_settings, text='Парамметр сглаживания (0.1-1):')
lbl_filter.grid(row=1, column=0)

ent_time = tk.Entry(master=frm_settings)
ent_time.insert(0, '1000')
ent_time.grid(row=0, column=1)

ent_filter = tk.Entry(master=frm_settings)
ent_filter.insert(0, '0.2')
ent_filter.grid(row=1, column=1)

frm_buttons = tk.Frame(master=window, width=150, height=100)
frm_buttons.grid(row=2, column=0)

btn_set = tk.Button(master=frm_buttons, text='Сохранить настройки', command=save_settings)
btn_set.grid(row=0, column=0)

btn_strat = tk.Button(master=frm_buttons, text='Снять показания', command=start)
btn_strat.grid(row=0, column=1, padx=5, pady=5)

frm_plot = tk.Frame(master=window)
frm_plot.grid(row=0, column=1, rowspan=2, columnspan=2)

plot = tk.PhotoImage(file='./Figure_1.png')
lbl_plot = tk.Label(master=frm_plot, image=plot)
lbl_plot.pack()

window.mainloop()