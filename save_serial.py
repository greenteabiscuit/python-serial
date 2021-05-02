import sys
import serial
import datetime
import csv
from collections import deque

#ser = serial.Serial('/dev/cu.usbserial-14110', 115200) #ポートの情報を記入
ser = serial.Serial('/dev/cu.usbserial-1430', 115200) #ポートの情報を記入

d_red = deque()
d_ir = deque()

while(1):
    line = ser.readline().decode('utf-8')
    splitted = line.split(",")
    toCsv = list(map(int, splitted))
    print(toCsv)
    d_red.append(toCsv[0])
    d_ir.append(toCsv[1])

    if len(d_red) == 100:
        r = d_red.popleft()
        print("red", r)

    if len(d_ir) == 100:
        ir = d_ir.popleft()
        print("ir", ir)

    with open('data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(toCsv)
    