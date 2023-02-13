####
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
# For the “Wahl” (Election) command it should be possible to use the elections 1, 2 or 3 – if it’s not working,
#   we need to check it here in our telemetry system how it’s configured – but I’m optimistic that I’m right. 😃
####



from enum import Enum


class MessageDirection(Enum) :
    VMC_TO_PC   = 0
    PC_TO_VMC   = 1


class ErrorType(Enum) :
    OUT_OF_SERVICE                  = 0x0001
    AT_LEAST_ONE_SHAFT_EMPTY        = 0x0002
    AT_LEAST_ONE_SHAFT_DEFECTIVE    = 0x0004
    PAYMENT_DEFECTIVE               = 0x0008
    HOPPER_EMPTY                    = 0x0010
    PRODUCT_ERROR_HOPPER            = 0x0020
    ERROR_COIN_CHANGER              = 0x0040
    ERROR_BANKNOTE_READER           = 0x0080
    ERROR_CARD_PAYMENT_SYSTEM       = 0x0100
    ERROR_PARENTAL_CONTROL_DEVICE   = 0x0200
    ERROR_CONTROL                   = 0x0420

    def __str__(self) -> str:
        if self.value == self.OUT_OF_SERVICE :
            return "OUT_OF_SERVICE"
        elif self.value == self.AT_LEAST_ONE_SHAFT_EMPTY :
            return "AT_LEAST_ONE_SHAFT_EMPTY"
        elif self.value == self.AT_LEAST_ONE_SHAFT_EMPTY :
            return "AT_LEAST_ONE_SHAFT_EMPTY"
        elif self.value == self.AT_LEAST_ONE_SHAFT_DEFECTIVE :
            return "AT_LEAST_ONE_SHAFT_DEFECTIVE"
        elif self.value == self.PAYMENT_DEFECTIVE :
            return "PAYMENT_DEFECTIVE"
        elif self.value == self.HOPPER_EMPTY :
            return "HOPPER_EMPTY"
        elif self.value == self.PRODUCT_ERROR_HOPPER :
            return "PRODUCT_ERROR_HOPPER"
        elif self.value == self.ERROR_COIN_CHANGER :
            return "ERROR_COIN_CHANGER"
        elif self.value == self.ERROR_BANKNOTE_READER :
            return "ERROR_BANKNOTE_READER"
        elif self.value == self.ERROR_CARD_PAYMENT_SYSTEM :
            return "ERROR_CARD_PAYMENT_SYSTEM"
        elif self.value == self.ERROR_PARENTAL_CONTROL_DEVICE :
            return "ERROR_PARENTAL_CONTROL_DEVICE"
        elif self.value == self.ERROR_CONTROL :
            return "ERROR_CONTROL"
        else:
            raise ValueError(f"Uknown ErrorType {self.value}")


class VmcMessageType(Enum) :
    OK              = "OK"                  # Ack message
    KREDIT          = "Kredit"              # Credit information (cents)
    JS              = "JS"                  # Youth protection information
    WAHL            = "Wahl"                # Dial key information
    WA              = "WA"                  # Issue of goods
    WR              = "WR"                  # Change return
    KT              = "KT"                  # Texts of the card terminal
    AT              = "AT"                  # Status automat
    WAHL_ANNAHME    = "WahlAnnahme"         # Setting the election acceptance
    SERVICE         = "Service"             # Service status
    DBG             = "DBG"                 # Debug
    EVA             = "EVA"                 # Start EVA-DTS communication session
    DT              = "DT"                  # Tests automatic display
    VER             = "VER"                 # Version of protocol
    SETUP           = "Setup"               # Command to set settings on PC
    WARENKORB       = "Warenkorb"           # Sell-off of several elections in a row
    LOG_FIN         = "LogFin"              # Confirms the creation of the log data records
    MENU_START      = "MenuStart"           # Tells the PC that a menu item created by the PC has been entered
    MENU_TASTE      = "MenuTaste"           # Transmission of a keystroke in the PC menu
    MENU_INFO       = "MenuInfo"            # Tells the PC how many columns and rows are available on the installed display
    PAUSE           = "Pause"               # Informs the PC that the communication is interrupted
    ERR             = "ERR"                 # Error message

    TEST_AUSW       = "TstAusw"             # TODO FIXME Is it a test message???

class PcMessageType(Enum) :
    OK              = "OK"                  # Ack message
    WAHL            = "Wahl"                # Dial key information
    KREDIT          = "Kredit"              # The PC can build up a credit in the control. Indication of the amount in cents.
    EVA             = "EVA"                 # Start EVA DTS communication session in the vending machine
    JS              = "JS"                  # Youth protection information
    VER             = "VER"                 # Requests the version information of the controller and transmits the own maximum possible protocol version.
    TASTE           = "Taste"               # Simulates pressing a key on the control
    LOG             = "Log"                 # Transmits the type of the next telemetry to the controller
    WAHL_BEZ        = "WahlBez"             # Issue of election paid through the Santvend
    GELD_ANNAHME    = "GeldAnnahme"         # Deactivation or activation of money acceptance of payment devices
    WARENKORB       = "Warenkorb"           # Sell-off of several elections in a row
    SETUP           = "Setup"               # Command to set settings on the VMC
    BOOT            = "Boot"                # Boots the controller
    MENU_SETUP      = "MenuSetup"           # Creates a menu item on the VMC with the name 'Name'
    MENU_TEXT       = "MenuText"            # Displays a text on the display of the VMC
    MENU_STOP       = "MenuStop"            # Exits the currently entered PC menu and transfers menu control back to the VMC


class VendtraceMessage:

    __source_value          = None  # str
    __parsed_content        = None
    
    __MESSAGE_HEADER        = bytearray('$'.encode())
    __MESSAGE_FOOTER        = bytearray('\r\n'.encode())

    def __init__(self, payload:str, direction:MessageDirection) -> None:
        if type(payload) == str:
            self.load_message(payload, direction)
        else:
            print (f"[!!!!!] Cannot load message {payload}")


    def load_message (self, payload:str, direction:MessageDirection):
        self.__source_value = str(payload)
        error_found         = False

        # Normalizing input value
        self.__source_value = self.__source_value .rstrip('\x00')
        while self.__source_value[0] == '\x00':
            self.__source_value = self.__source_value[1:]
        while self.__source_value[0] == '$':
            self.__source_value = self.__source_value[1:]

        if not error_found:
            # Filling __parsed_content basing on message type
            if direction == MessageDirection.VMC_TO_PC:
                self.__parse_vmc_message()
            elif direction == MessageDirection.PC_TO_VMC:
                self.__parse_pc_message()
            else:
                raise TypeError (f"Wrong MessageDirection value: {direction}")

        print (f"Parsed message: {self.__parsed_content}")

        return self


    def payload_to_string(self) -> str:
        return self.__source_value


    def serialize (self) -> bytearray:
        if self.__source_value != None:
            return self.__MESSAGE_HEADER + bytearray(self.__source_value.encode()) + self.__MESSAGE_FOOTER
        else:
            raise ValueError("Source value is None!")


    def __parse_vmc_message (self):
        p_msg           = {}
        splitted_source = self.__source_value.split("*")
        if len(splitted_source) > 1 :
            splitted_source.pop()   # Removing last item
        m_type          = VmcMessageType(splitted_source[0])
        #print (f'[{__name__}] source value     {self.__source_value}')
        #print (f'[{__name__}] splitted_source  {splitted_source}')

        p_msg["message_type"]   = m_type
        if m_type == VmcMessageType.AT :
            # TODO Parsing AT messsage
            pass
        else:
            raise ValueError(f"Unsupported message type: {m_type}")

        self.__parsed_content    = p_msg


    def __parse_pc_message(self):
        p_msg           = {}
        splitted_source = self.__source_value.split("*")
        if len(splitted_source) > 1 :
            splitted_source.pop()   # Removing last item
        m_type          =  PcMessageType(splitted_source[0])
        #print (f'[{__name__}] source value     {self.__source_value}')
        #print (f'[{__name__}] splitted_source  {splitted_source}')

        # TODO
        p_msg["message_type"]   = m_type
        # if m_type == VmcMessageType.OK :
        #     # TODO Parsing OK messsage
        #     pass
        # else:
        #     raise ValueError(f"Unsupported message type: {m_type}")
        
        self.__parsed_content    = p_msg