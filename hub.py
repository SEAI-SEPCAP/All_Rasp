#! /usr/bin/python3 -u

import sys
from sms import SepcapMessagingSystem as SMS
import serial


def getRedirectStream(pipeMap: dict, address: int):
    return pipeMap.get(address, [])


def main():
    if len(sys.argv) < 5:
        print("Not enough arguments", file=sys.stderr)
        # return 1

    HubToClass = open(sys.argv[1], 'wb')
    ClassToHub = open(sys.argv[2], 'rb')
    HubToInterface = open(sys.argv[3], 'wb')
    InterfaceToHub = open(sys.argv[4], 'rb')
    #ser = AutoSerial("/dev/ttyAMA0")
    ser = serial.Serial("/dev/ttyS0")

    std = SMS(sys.stdin, sys.stdout)
    classification = SMS(ClassToHub, HubToClass)
    interface = SMS(InterfaceToHub, HubToInterface)
    arduino = SMS(ser, ser, "serial")

    allPipes = [
        classification,
        interface,
        arduino
    ]
    pipeMap = {
        SMS.Address.Broadcast: [classification, interface, arduino],
        SMS.Address.Individualization: [arduino],
        SMS.Address.Classification: [classification],
        SMS.Address.Distribuition: [arduino],
        SMS.Address.Interface: [interface],
    }

    print("Hub")

    while 1:
        for pipe in allPipes:
            if pipe.isData():
                address, mtype, data = pipe.readPacket()
                pipeArray = getRedirectStream(pipeMap, address)
                for redirPipe in pipeArray:
                    redirPipe.sendPacket(address, mtype, data)

        if std.isData():
            c = std.read()
            if c == '\x1b':         # x1b is ESC
                break

    ser.close()


if __name__ == "__main__":
    main()
