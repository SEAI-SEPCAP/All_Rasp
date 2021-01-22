"""
SEPCAP Messaging System
"""

import select
import tty
import termios
import enum


class SepcapMessagingSystem(object):
    """
    docstring
    """

    stream_in = None
    stream_out = None
    old_settings = None
    sms_type = None

    class Address(enum.IntEnum):
        Broadcast = 0
        Individualization = 1
        Classification = 2
        Distribuition = 3
        Interface = 4

    class Message:

        class EmergencyStop(enum.IntEnum):
            type = 0
            Emergency = 0
            Resume = 1

        class NewCapsule(enum.IntEnum):
            type = 1

        class StartStop(enum.IntEnum):
            type = 2
            Stop = 0
            Start = 1
            Count = 2
        
        class CalibrationColor(enum.IntEnum):
            type = 3
            Yellow = 0
            Red = 1
            White = 2
            Blue = 3
            Dark_Green = 4
            Light_Green = 5
            Nude = 6
            
        class CalibrationR(enum.IntEnum):
            type = 4
        class CalibrationG(enum.IntEnum):
            type = 5
        class CalibrationB(enum.IntEnum):
            type = 6
        class CalibrationConf(enum.IntEnum):
            type = 7
            
            

    def __init__(self, stream_in, stream_out, type="tty"):
        self.stream_in = stream_in
        self.stream_out = stream_out
        self.sms_type = type

        if (self.sms_type == "tty"):
            self.old_settings = termios.tcgetattr(self.stream_in)
            tty.setcbreak(self.stream_in.fileno())

    def __del__(self):
        if (self.sms_type == "tty"):
            termios.tcsetattr(
                self.stream_in, termios.TCSADRAIN, self.old_settings)

    def isData(self):
        if self.sms_type == "serial":
            return self.stream_in.in_waiting

        return select.select([self.stream_in], [], [], 0) == ([self.stream_in], [], [])

    def read(self, n=1):
        return self.stream_in.read(n)

    def lineToMessage(self, line):
        return [i for i in list(line)]

    def getAddress(self, byte):
        return (byte & 0xF0) >> 4

    def getMessageType(self, byte):
        return byte & 0x0F

    def decodeMessage(self, message: list):
        return self.getAddress(message[0]), self.getMessageType(message[0]), message[1]

    def encodeMessage(self, address: int, messageType: int, data: int):
        return bytes([(address << 4) + messageType, data])

    def readPacket(self):
        line = bytearray(self.read(2))
        message = self.lineToMessage(line)
        return self.decodeMessage(message)

    def sendPacket(self, address: int, messageType: int, data: int):
        message = self.encodeMessage(address, messageType, data)
        if self.sms_type == "std":
            print(message, file=self.stream_out)
        else:
            self.stream_out.write(message)
        self.stream_out.flush()
