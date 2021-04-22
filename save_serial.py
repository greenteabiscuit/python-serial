import sys
import serial
import datetime
import csv

ser = serial.Serial('/dev/cu.usbserial-1410', 115200) #ポートの情報を記入

while(1):
    line = ser.readline().decode('utf-8')
    splitted = line.split()
    if len(splitted) > 3:
        print(splitted)
        with open('data.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(splitted)
    