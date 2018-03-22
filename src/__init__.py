if __name__ == '__main__':
    from sys import argv, exit
    from PyQt5.QtWidgets import QApplication
    from main_script import MainWindow
    app = QApplication(argv)
    win = MainWindow()
    win.show()
    exit(app.exec_())
