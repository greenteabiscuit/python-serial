import sys
import serial
import datetime
import csv
from collections import deque
import matplotlib.pyplot as plt
import numpy as np

#ser = serial.Serial('/dev/cu.usbserial-14110', 115200) #ポートの情報を記入
ser = serial.Serial('/dev/cu.usbserial-1410', 115200) #ポートの情報を記入

d_red = deque()
d_ir = deque()
BUFFER_SIZE = 100

fig, axes = plt.subplots(1, 1)
x = np.arange(0, 100, 1)

while(1):
    line = ser.readline().decode('utf-8')
    splitted = line.split(",")
    toCsv = list(map(int, splitted))
    print(toCsv)
    d_red.append(toCsv[0])
    d_ir.append(toCsv[1])
    n_thr, red_mean, ir_mean = 0, 0, 0

    # BUFFERSIZE + 1になったらpopする
    if len(d_red) > BUFFER_SIZE:
        r = d_red.popleft()
        red_mean = sum(d_red) / BUFFER_SIZE
        print("red mean", red_mean)

    ax = []
    if len(d_ir) > BUFFER_SIZE:
        ir = d_ir.popleft()
        ir_mean = sum(d_ir)/ BUFFER_SIZE
        print("ir mean", ir_mean)
        for item in d_ir:
            ax.append(item - sum(d_ir) / BUFFER_SIZE)
        ## ここ別に4 point moving averageじゃなくてもいいかもしれない
        for i in range(BUFFER_SIZE - 4):
            ax[i] = (ax[i] + ax[i + 1] + ax[i + 2] + ax[i + 3]) / 4       
        n_thr = sum(ax) / (BUFFER_SIZE - 4)
        print("threshold:", n_thr)
        axes.set_ylim((min(ax) // 10 * 10 - 100, max(ax) // 10 * 10 + 100))
        line, = axes.plot(x, ax, color='blue')
        plt.pause(0.01)
        line.remove()
        #with open('data.csv', 'a') as f:
        #    writer = csv.writer(f)
        #    writer.writerow(ax)
    