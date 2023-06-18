import serial
import sys
import os

def main():
    # get the port name from the command line and the baud rate
    if len(sys.argv) < 3:
        print("Usage: logger.py <port name> <baud rate>")
        sys.exit(1)
    port = sys.argv[1]
    baud = int(sys.argv[2])

    # open the serial port
    ser = serial.Serial(port, baud)

    # loop forever printing serial port data
    while True:
        print(ser.readline().decode('utf-8').strip())

if __name__ == "__main__":
    main()
