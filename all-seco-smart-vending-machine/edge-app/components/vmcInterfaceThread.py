
from utils import commons
from utils.vendtraceMessage import VendtraceMessage
from utils.vendtraceProtocolParser import VendTraceParser

from PySide6.QtCore import QThread, Signal, QMutex

import logging, serial


class VmcInterface (QThread) :

    __logger            = None
    __serial_port       = None
    __serial_port_mutex = None
    __parser            = None
    __still_run         = None
    __still_run_mux     = None
    ##########
    CR          = '\r'  # 0x0D
    LF          = '\n'  # 0x0A
    NewMessage  = Signal(VendtraceMessage)


    ##########


    def __init__(self, config) -> None:
        super().__init__()

        self.__logger           = commons.create_logger(logging, __name__)

        # Opening serial port
        self.__serial_port      = serial.Serial(config["vmc"]["port"], int(config["vmc"]["baud"]), int(config["vmc"]["byte_size"]),
                                                config["vmc"]["parity"], int(config["vmc"]["stop_bit"]), .2)
        self.__serial_port_mux  = QMutex()
        self.__parser           = VendTraceParser()
        self.__still_run        = True
        self.__still_run_mux    = QMutex()


    def close(self) :
        self.__still_run_mux.lock()
        self.__still_run    = False
        self.__still_run_mux.unlock()


    def send_message(self, msg) :
        message                 = self.__parser.parse_message(msg)
        serialized_message      = message.serialize()
        serialized_message_str  = message.serialize().decode()
        
        self.__logger.debug(f"sending {serialized_message_str} ({len(serialized_message)} bytes)")

        # TODO Add message to "output_messages" list
        # FIXME Remove me!! -> TEST
        self.__serial_port_mux.lock()
        c   = self.__serial_port.write(message.serialize())
        self.__serial_port_mux.unlock()
        
        self.__logger.debug(f"Wrote {c} bytes\n")


    def run(self) -> None:
        payload     = ''
        curr_status = 0

        self.__logger.debug("Start reading...")

        while True:
            self.__still_run_mux.lock()
            if self.__still_run :
                self.__still_run_mux.unlock()
                
                self.__serial_port_mux.lock()
                c   = self.__serial_port.read()
                self.__serial_port_mux.unlock()
                
                dc  = c.decode()

                if curr_status == 0 and dc != self.CR:
                    payload += dc
                elif curr_status == 0 and dc == self.CR:
                    curr_status = 1
                elif curr_status == 1 and dc == self.LF:
                    msg         = self.__parser.parse_message(payload)
                    
                    # TODO Do something with the message
                    # Replying with an ACK message
                    self.send_message("OK")
                    # Emitting NewMessage signal
                    self.NewMessage.emit(msg)
                    
                    payload     = ""
                    curr_status = 0

                    # TODO Checking for messages in "output_messages" list
                else :
                    self.__logger.critical(f"ERROR DURING READING: received {c.decode()} in state {curr_status}")
            else:
                self.__still_run_mux.unlock()
                break