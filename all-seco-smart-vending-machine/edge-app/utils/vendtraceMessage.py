
from enum import Enum


class MessageType (Enum) :
    UNKNOWN = -1

class VendtraceMessage:

    __source_value          = None  # str
    __parsed_content        = None
    
    __MESSAGE_HEADER        = bytearray('$'.encode())
    __MESSAGE_FOOTER        = bytearray('\r\n'.encode())

    def __init__(self, payload:str = None) -> None:
        if str:
            self.load_message(payload)
        else:
            print (f"[!!!!!] Cannot load message {payload}")


    def load_message (self, payload:str) -> MessageType:
        self.__source_value = payload

        #TODO Fill __parsed_content basing on message type

        return self.__parsed_content


    def payload_to_string(self) -> str:
        return self.__source_value


    def serialize (self) -> bytearray:
        if self.__source_value != None:
            return self.__MESSAGE_HEADER + bytearray(self.__source_value.encode()) + self.__MESSAGE_FOOTER
        else:
            raise ValueError("Source value is None!")