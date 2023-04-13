
import os


class LocalDB:

    __db_file_path          = None
    __short_coffee_counter  = 0
    __long_coffee_counter   = 0


    def __init__(self, db_file_path) -> None:

        self.__db_file_path = db_file_path
        
        # Creating local DB if not existing
        if not os.path.exists(self.__db_file_path):
            print (f"Creating local db at  {self.__db_file_path}")
            f   = open(self.__db_file_path, "x")
            f.close()
            self.__dump_db()
        
        # Loading values from local DB
        f   = open(self.__db_file_path, "r")
        self.__short_coffee_counter = int(f.readline())
        self.__long_coffee_counter  = int(f.readline())
        f.close()


    def __dump_db(self):
        f   = open(self.__db_file_path, "w+")
        f.write(f"{self.__short_coffee_counter}\n")
        f.write(f"{self.__long_coffee_counter}\n")
        f.close()


    def get_short_coffee_counter(self):
        return self.__short_coffee_counter
    
    def get_long_coffee_counter(self):
        return self.__long_coffee_counter
    
    def new_short_coffee(self):
        self.__short_coffee_counter += 1
        self.__dump_db()
    
    def new_long_coffee(self):
        self.__long_coffee_counter += 1
        self.__dump_db()