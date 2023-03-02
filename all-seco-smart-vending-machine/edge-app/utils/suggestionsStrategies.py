
from utils import commons

from PySide6.QtCore import QObject


class SuggestionsStrategies(QObject) :

    __logger    = None
    __config    = None
    ##########


    def __init__(self, config) -> None:
        super().__init__()

        self.__logger   = commons.create_logger(__name__)


    def suggest_advertisement(self, session, available_advertisements) -> str:
        result  = ""
        # TODO Selecting those that can be used
        # TODO Randomly choosing an item
        ##FIXME TEST
        result="abcdef"
        return result
    

    def suggest_products(self, session, available_products):
        result  = []
        # TODO Selecting those that can be used
        # TODO Randomly choosing items
        ##FIXME TEST
    

    def suggest_promo(self, session, available_promos):
        result  = None
        # TODO Selecting those that can be used
        # TODO Randomly choosing an item
        ##FIXME TEST
        return result