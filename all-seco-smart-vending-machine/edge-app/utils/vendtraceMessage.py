
from enum import Enum


class MessageType (Enum) :
    UNKNOWN = -1

class VendtraceMessage:

    __source_value          = None
    __type : MessageType    = None
    
    __MESSAGE_HEADER        = bytearray('$'.encode())
    __MESSAGE_FOOTER        = bytearray('\r\n'.encode())

    def __init__(self, payload:str = None) -> None:
        if str:
            self.__source_value = payload


    def load_message (self, payload:str) -> MessageType:
        self.__source_value = payload
        self


    def serialize (self) -> bytearray:
        return self.__MESSAGE_HEADER + bytearray(self.__source_value.encode()) + self.__MESSAGE_FOOTER