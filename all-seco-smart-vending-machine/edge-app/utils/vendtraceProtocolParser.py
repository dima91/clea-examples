
# With a minimalistic vendtrace implementation (command "Wahl" and responses "Kredit", "Wahl", "WA" and possibly "DT"),
#   should it be possible to do anything you need. Ignore the other commands and responses.
####
# Different from the documentation, your VMC doesn't answer with OK to all commands. That's a really new feature.
#   In your case, the answer for the "Wahl" command is the "Wahl" response from the VMC.
####
# There are 24 choices configured and 3 dispensers. So, you could try the Wahl command with 1, 10 and 17 (all other choices are duplicates of them).
#   Possibly, the VMC detects that the dispenser is empty and you have to put something in first.
#   But you should see that in the VMC response to that command.
####

from utils import commons
from utils.vendtraceMessage import MessageType, VendtraceMessage

from PySide6.QtCore import QObject

import os, logging
from enum import Enum


class ErrorCodes (Enum) :
    OUT_OF_SERVICE                  = 0x0001
    AT_LEAST_ONE_SHAFT_EMPTY        = 0x0002
    AT_LEAST_ONE_SHAFT_DEFECTIVE    = 0x0004
    PREPAYMENT_DEfECTIVE            = 0x0008
    HOPPER_EMPTY                    = 0x0010
    OUTPUT_ERROR_HOPPER             = 0x0020
    ERROR_COIN_CHANGER              = 0x0040
    ERROR_BANKNOTE_READER           = 0x0080
    ERROR_CARD_PAYMENT_SYSTEM       = 0x0100
    ERROR_PARENTAL_CONTROL_DEVICE   = 0x0200
    ERROR_CONTROL                   = 0x0400

    
##########
##########


class VendTraceParser (QObject):

    __logger    = None
    ##########


    ##########


    def __init__(self) -> None:
        super().__init__()

        self.__logger   = commons.create_logger(logging, __name__)


    def parse_message(self, input_string) -> VendtraceMessage :
        self.__logger.debug(f"parsing  {input_string}")
        out_msg = VendtraceMessage(input_string)
        return out_msg