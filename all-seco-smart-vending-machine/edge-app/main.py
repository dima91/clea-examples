
import sys, argparse, configparser
from PySide6.QtWidgets import QApplication
from mainWindow import MainWindow




def main (args) :
    config          = configparser.ConfigParser ()
    config.read (args.config)

    app             = QApplication ([])
    main_window     = MainWindow (config)

    with open(f"style/{config['app']['style_file']}", 'r') as f:
        app.setStyleSheet(f.read().replace('\n', ''))
    
    main_window.showFullScreen()
    sys.exit(app.exec())
    


if __name__ == "__main__" :
    parser  = argparse.ArgumentParser (prog="All SECO Smart Vending Machine")
    parser.add_argument ('-c', '--config')
    main (parser.parse_args())