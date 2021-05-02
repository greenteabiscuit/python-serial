import sys
import serial
import datetime
import csv
from collections import deque

#ser = serial.Serial('/dev/cu.usbserial-14110', 115200) #ポートの情報を記入
ser = serial.Serial('/dev/cu.usbserial-1430', 115200) #ポートの情報を記入

d_red = deque()
d_ir = deque()
BUFFER_SIZE = 100

while(1):
    line = ser.readline().decode('utf-8')
    splitted = line.split(",")
    toCsv = list(map(int, splitted))
    print(toCsv)
    d_red.append(toCsv[0])
    d_ir.append(toCsv[1])

    # BUFFERSIZE + 1になったらpopする
    if len(d_red) > BUFFER_SIZE:
        r = d_red.popleft()
        print("red mean", sum(d_red) / BUFFER_SIZE)

    ax = []
    if len(d_ir) > BUFFER_SIZE:
        ir = d_ir.popleft()
        print("ir mean", sum(d_ir)/ BUFFER_SIZE)
        for item in d_ir:
            ax.append(item - sum(d_ir) / BUFFER_SIZE)
        ## ここ別に4 point moving averageじゃなくてもいいかもしれない
        for i in range(BUFFER_SIZE - 4):
            ax[i] = (ax[i] + ax[i + 1] + ax[i + 2] + ax[i + 3]) / 4       
        n_thr = sum(ax) / (BUFFER_SIZE - 4)
        print("threshold:", n_thr)

    with open('data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(toCsv)
    