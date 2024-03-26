#!/usr/bin/python3

radiociv="0x94"
myciv="0xc0"
baudrate = 115200
serialport = "/dev/ttyUSB0"

from datetime import datetime
import serial
import struct
import os

def send_cmd(ser,cmd):
    c = 0

    while(c < len(cmd)):
        senddata = int(bytes(cmd[c], 'UTF-8'), 16)
        ser.write(struct.pack('>B', senddata))
        c += 1

def get_resp(ser):
    s = ''
    while s != b'\xFE':
        s = ser.read()
        # Timeout?
        if len(s) == 0:
            break;

    if ser.read() == b'\xFE':
        i = 0
        rxdata = []
        while s != b'\xFD':
            s = ser.read()
            rxdata.append(s)
            i += 1

        rxdata.pop()
        return rxdata

def get_time(ser):
    cmd = [ "0xFE", "0xFE", radiociv, myciv, "0x1A", "0x05", "0x00", "0x95", "0xFD" ]
    send_cmd(ser,cmd)
    response = get_resp(ser)
    vals = [response[i].hex() for i in range (0, len(response))]
    cmd = ''.join(vals)
    rig_time = str(cmd)[-4:]
    return rig_time 

def set_time(ser):
    d = datetime.utcnow()
    cmd = [ "0xFE", "0xFE", radiociv, myciv, "0x1A", "0x05", "0x00", "0x95" ]
    cmd.append("0x" + str(d.hour))
    cmd.append("0x" + str(d.minute))
    cmd.append("0xFD")
    send_cmd(ser,cmd)

def get_date(ser):
    cmd = [ "0xFE", "0xFE", radiociv, myciv, "0x1A", "0x05", "0x00", "0x94", "0xFD" ]
    send_cmd(ser,cmd)
    response = get_resp(ser)
    vals = [response[i].hex() for i in range (0, len(response))]
    cmd = ''.join(vals)
    rig_day = str(cmd)[-2:]
    rig_month = str(cmd)[-4:-2]
    rig_year = str(cmd)[-8:-4]
    rig_date = (f"{rig_day}-{rig_month}-{rig_year}")
    return rig_date

def set_date(ser):
    d = datetime.utcnow()
    cmd = [ "0xFE", "0xFE", radiociv, myciv, "0x1A", "0x05", "0x00", "0x94" ]
    cmd.append("0x" + str(d.year)[0:2])
    cmd.append("0x" + str(d.year)[2:])
    cmd.append("0x" + str(d.strftime('%m')))
    cmd.append("0x" + str(d.strftime('%d')))
    cmd.append("0xFD")
    send_cmd(ser,cmd)

def main():
    ser = serial.Serial(serialport, baudrate)
    print("[INFO]: Serial port opened successfully.")
    print("[INFO]: Getting time from your Icom 7300.")
    i = get_time(ser)
    print(f"[INFO]: The current time on your Icom 7300 is {i}")
    ser.close()

    ser = serial.Serial(serialport, baudrate)
    print("[INFO]: Setting the time on your Icom 7300.")
    set_time(ser)
    ser.close()

    ser = serial.Serial(serialport, baudrate)
    print("[INFO]: Getting time from your Icom 7300.")
    i = get_time(ser)
    print(f"[INFO]: The current time on your Icom 7300 is {i}")
    ser.close()

    ser = serial.Serial(serialport, baudrate)
    print("[INFO]: Getting date from your Icom 7300.")
    i = get_date(ser)
    print(f"[INFO]: The current date on your Icom 7300 is {i}")
    ser.close()

    ser = serial.Serial(serialport, baudrate)
    print("[INFO]: Setting the date on your Icom 7300.")
    set_date(ser)
    ser.close()

    ser = serial.Serial(serialport, baudrate)
    print("[INFO]: Getting date from your Icom 7300.")
    i = get_date(ser)
    print(f"[INFO]: The current date on your Icom 7300 is {i}")
    ser.close()


if __name__ == "__main__":
    main()

