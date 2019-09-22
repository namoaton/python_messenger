import threading
from time import sleep

import datetime
import requests
from PyQt5 import QtWidgets

import clientui


# pyuic5 messenger.ui -o clientui.py

class ExampleApp(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.last_time = 0
        self.setupUi(self)
        self.pushButton.clicked.connect(self.send)
        threading.Thread(target=self.refresh).start()

    def send(self):
        username = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
        text = self.lineEdit.text()
        data = {
            'username': username,
            'password': password,
            'text': text
        }
        if username == "" or password == "" or text == "":
            return
        response = requests.post("http://127.0.0.1:5000/login", json=data)
        print("Login response", response.json())
        if response.json()['ok']:
            self.lineEdit.setText('')
            self.statusbar.showMessage("Login ok", 5000)
            response = requests.post("http://127.0.0.1:5000/send", json=data)
            print("Send response", response.json())
        else:
            print("Login error!!!")

    def refresh(self):
        """
         refressh message window
        :return:
        """
        self.last_time = 0
        while True:
            try:
                response = requests.get('http://127.0.0.1:5000/messages', params={'after': self.last_time})
            except:
                print("Connection error")
                sleep(1)
                continue
            for message in response.json()['messages']:
                self.last_time = message['time']
                self.textBrowser.append(f"{datetime.datetime.fromtimestamp(message['time'])}")
                self.textBrowser.append(f"{message['username']} ")
                self.textBrowser.append(f"{message['text']}")
                self.textBrowser.append("")
                self.textBrowser.ensureCursorVisible()

                print(message)
            # self.textBrowser.repaint()
            sleep(1)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = ExampleApp()
    window.show()
    app.exec_()
