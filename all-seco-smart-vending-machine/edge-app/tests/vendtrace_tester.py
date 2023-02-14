
from utils.vendtraceMessage import VendtraceMessage, ErrorType
from components.vmcInterfaceThread import VmcInterface

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import QThread

import sys, argparse, serial, configparser, logging, time

vmc_interface : VmcInterface    = None
tester_thread                   = None




class TesterThread (QThread) :
    ___vmc      = None
    __still_run = None
    __messages  = []

    
    def __init__(self) -> None:
        global vmc_interface
        super().__init__()
        
        self.__still_run    = True
        self.___vmc         = vmc_interface
        self.___vmc.NewMessage.connect(self.__message_callback)

        self.__messages.append("VER*0*14*")
        self.__messages.append("")
        self.__messages.append("")
        self.__messages.append("")
        self.__messages.append("")
        self.__messages.append("")
        # Sending pressed item [1 || 2 || 3 || 10 || 17] -> Wahl
        self.__messages.append("Wahl*1*")


    def __message_callback (self, m:VendtraceMessage) :
        p   = m.payload_to_string()
        print (f"[TesterThread]  Received a new message:     {p}\n\t\t{m.get_message()}\n")


    def run(self):
        last_op_t           = time.time()
        messages_interval   = 4 #seconds

        while self.__still_run:
            time.sleep (.2)
            if time.time() - last_op_t > messages_interval:
                last_op_t   = time.time()
                if (len(self.__messages) > 0):
                    m   = self.__messages.pop(0)
                    if len(m) > 0:
                        print (f"Sending  {m}")
                        self.___vmc.send_message(m)
                    else :
                        pass
                        #print ("Sgnoring it")


    def close(self):
        self.__still_run    = False




def bit_testing():
    for v in ErrorType:
        print (f"name, value -> {v.name}, {v.value}")

    print (f"\n")
    err0_t  = ErrorType.ERROR_CARD_PAYMENT_SYSTEM
    err1_t  = ErrorType.AT_LEAST_ONE_SHAFT_DEFECTIVE
    print (f"err: {err0_t.value}")
    print (f"err: {format(err0_t.value, 'b')}")
    print (f"err: {type(format(err0_t.value, 'b'))}")

    err_cmp = ErrorType.AT_LEAST_ONE_SHAFT_EMPTY.value | ErrorType.ERROR_COIN_CHANGER.value
    print (f"err_cmp: {err_cmp} -> {format(err_cmp, 'b')}")
    for v in ErrorType:
        if err_cmp & v.value :
            print (f"err_cmp matches with {v.name}")




def main(args) :
    global vmc_interface
    global tester_thread

    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s : %(name)s.%(funcName)s @ %(asctime)s]  %(message)s')

    #bit_testing()

    config                  = configparser.ConfigParser ()
    config.read (args.config)

    app                     = QApplication ([])
    main_window             = QMainWindow ()
    main_window.closeEvent  = close_event

    vmc_interface           = VmcInterface (config)
    vmc_interface.start()
    tester_thread           = TesterThread()
    tester_thread.start()

    main_window.show()
    sys.exit(app.exec())


def close_event (arg : QCloseEvent) :
    global vmc_interface

    tester_thread.close()
    tester_thread.wait()

    vmc_interface.close()
    vmc_interface.wait()


if __name__ == "__main__":
    parser  = argparse.ArgumentParser()
    parser.add_argument ('-c', '--config')
    main (parser.parse_args())