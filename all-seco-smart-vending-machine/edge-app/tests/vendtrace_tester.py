
from utils import vendtrace_protocol_parser
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

    
    def __init__(self) -> None:
        global vmc_interface
        super().__init__()
        
        self.___vmc         = vmc_interface
        self.__still_run    = True


    def run(self):
        while self.__still_run:
            time.sleep (1)
            #TODO
            #self.___vmc.send_message("OK")


    def close(self):
        self.__still_run    = False




def main(args) :
    global vmc_interface
    global tester_thread

    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s : %(name)s.%(funcName)s @ %(asctime)s]  %(message)s')

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