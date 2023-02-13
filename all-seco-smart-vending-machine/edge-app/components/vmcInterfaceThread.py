
from utils import commons
from utils.vendtraceMessage import VendtraceMessage, MessageDirection

from PySide6.QtCore import QThread, Signal, QMutex

import logging, serial


class VmcInterface (QThread) :

    __logger            = None
    __serial_port       = None
    __serial_port_mutex = None
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
        self.__out_messages     = []
        self.__out_messages_mux = QMutex()
        self.__still_run        = True
        self.__still_run_mux    = QMutex()


    def __send_message(self, msg):
        serialized_message      = msg.serialize()
        serialized_message_str  = msg.serialize().decode()
        serialized_message_len  = len(serialized_message)
        
        #self.__logger.debug(f"Sending {serialized_message_str} ({serialized_message_len} bytes)")

        self.__serial_port_mux.lock()
        c   = self.__serial_port.write(serialized_message)
        self.__serial_port_mux.unlock()

        if c!=len(serialized_message):
            self.__logger.error(f"Wrote {c} bytes, message len is {serialized_message_len}. Message is:\n\t\t{serialized_message_str}")


    def close(self) :
        self.__still_run_mux.lock()
        self.__still_run    = False
        self.__still_run_mux.unlock()


    def send_message(self, msg) :
        message                 = VendtraceMessage(msg, MessageDirection.PC_TO_VMC)

        # Adding message to "output_messages" list
        self.__out_messages_mux.lock()
        self.__out_messages.append(message)
        self.__out_messages_mux.unlock()

        # Checking for messages in "output_messages" list
        self.__out_messages_mux.lock()
        if len(self.__out_messages) > 0 :
            self.__send_message(self.__out_messages.pop())
        self.__out_messages_mux.unlock()


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
                
                if len(dc) > 0:
                    if dc == b'\x00':
                        print ("------------------------ Don't include it!!!")

                    if curr_status == 0 and dc != self.CR:
                        payload += dc
                    elif curr_status == 0 and dc == self.CR:
                        curr_status = 1
                    elif curr_status == 1 and dc == self.LF:
                        try :
                            # Building incoming message
                            msg = VendtraceMessage(payload, MessageDirection.VMC_TO_PC)
                            # Replying with an ACK message
                            self.send_message("OK")
                            # TODO Do something with the message
                            # Emitting NewMessage signal
                            self.NewMessage.emit(msg)
                        except Exception as e:
                            self.__logger.error(f"Catched this exception during message handling\n\t{e}")
                        
                        payload     = ""
                        curr_status = 0
                    else :
                        self.__logger.critical(f"ERROR DURING READING: received {c.decode()} in state {curr_status}")
            else:
                self.__still_run_mux.unlock()
                break