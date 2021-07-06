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
    n_thr_ir, n_thr_red, red_mean, ir_mean = 0, 0, 0, 0

    # BUFFERSIZE + 1になったらpopする
    red_lis, ir_lis = [], []
    if len(d_red) > BUFFER_SIZE and len(d_ir) > BUFFER_SIZE:
        r = d_red.popleft()
        red_mean = sum(d_red) / BUFFER_SIZE
        print("red mean", red_mean)
        for item in d_red:
            red_lis.append(item - sum(d_red) / BUFFER_SIZE)
        ## ここ別に4 point moving averageじゃなくてもいいかもしれない
        for i in range(BUFFER_SIZE - 4):
            red_lis[i] = (red_lis[i] + red_lis[i + 1] + red_lis[i + 2] + red_lis[i + 3]) / 4       
        n_thr_red = sum(red_lis) / (BUFFER_SIZE - 4)
        print("red threshold:", n_thr_red)
        axes.set_ylim((min(red_lis) // 10 * 10 - 100, max(red_lis) // 10 * 10 + 100))
        line_red, = axes.plot(x, red_lis, color='red')

        ir = d_ir.popleft()
        ir_mean = sum(d_ir)/ BUFFER_SIZE
        print("ir mean", ir_mean)
        for item in d_ir:
            ir_lis.append(item - sum(d_ir) / BUFFER_SIZE)
        ## ここ別に4 point moving averageじゃなくてもいいかもしれない
        for i in range(BUFFER_SIZE - 4):
            ir_lis[i] = (ir_lis[i] + ir_lis[i + 1] + ir_lis[i + 2] + ir_lis[i + 3]) / 4       
        n_thr_ir = sum(ir_lis) / (BUFFER_SIZE - 4)
        print("ir threshold:", n_thr_ir)
        min_of_both = min(min(ir_lis), min(red_lis))
        max_of_both = max(max(ir_lis), max(red_lis))
        axes.set_ylim((min_of_both // 10 * 10 - 20, max_of_both // 10 * 10 + 20))
        line_ir, = axes.plot(x, ir_lis, color='blue')
        plt.pause(0.01)
        line_ir.remove()
        line_red.remove()
        #with open('data.csv', 'a') as f:
        #    writer = csv.writer(f)
        #    writer.writerow(ax)
    