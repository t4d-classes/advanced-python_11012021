# """ rate client module """

from typing import Optional
from PySide6 import QtCore
from PySide6.QtWidgets import *

import sys
import socket
import time

# import sys
# import socket
# import yaml
# import pathlib
# from typing import Any

# def read_config() -> Any:
#     """ read config """

#     with open(pathlib.Path("config", "rates_config.yaml")) as yaml_file:
#         return yaml.load(yaml_file, Loader=yaml.SafeLoader)

# config = read_config()

# host = config['server']['host']
# port = int(config['server']['port'])

class WorkerSignals(QtCore.QObject):

    status = QtCore.Signal(str)
    conn = QtCore.Signal(socket.socket)
    msg = QtCore.Signal(str)

class ConnectWorker(QtCore.QRunnable):
    """ connect thread """


    def __init__(self, host, port) -> None:
        super().__init__()
        self.host = host
        self.port = port

        self.signals = WorkerSignals()

    @QtCore.Slot()
    def run(self) -> None:
        """ run """

        self.signals.status.emit("Connecting...")
        time.sleep(1)

        socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_client.connect( (self.host, self.port) )
        self.signals.status.emit("Connected")
        time.sleep(1)

        self.signals.conn.emit(socket_client)

        self.signals.msg.emit(socket_client.recv(2048).decode('UTF-8'))

        self.signals.status.emit("Ready")
        time.sleep(1)


class MainWindow(QMainWindow):
    """ main window """

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Rates Client")

        self.status = QLabel(self)

        self.status.setText("Hello!")

        self.status_bar = QStatusBar(self)
        self.status_bar.addPermanentWidget(self.status)
        self.setStatusBar(self.status_bar)

        connect_button = QPushButton("Connect")
        connect_button.clicked.connect(self.rates_server_connect)
        disconnect_button = QPushButton("Disconnect")
        disconnect_button.clicked.connect(self.rates_server_disconnect)

        connect_layout = QHBoxLayout()
        connect_layout.addWidget(connect_button)
        connect_layout.addWidget(disconnect_button)

        connect_widget = QWidget()
        connect_widget.setLayout(connect_layout)


        command_label = QLabel("Command")
        self.command_textbox = QLineEdit("")
        command_button = QPushButton("Send")
        command_button.clicked.connect(self.send_command)

        command_layout = QHBoxLayout()
        command_layout.addWidget(command_label)
        command_layout.addWidget(self.command_textbox)
        command_layout.addWidget(command_button)

        command_widget = QWidget()
        command_widget.setLayout(command_layout)

        self.command_history = QListWidget()


        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(connect_widget)
        vbox_layout.addWidget(command_widget)
        vbox_layout.addWidget(self.command_history)

        main_widget = QWidget()
        main_widget.setLayout(vbox_layout)

        self.setCentralWidget(main_widget)

        self.conn: Optional[socket.socket] = None
        self.threadpool = QtCore.QThreadPool()


        self.setStyleSheet("""
            QPushButton { max-width: 100px }
        """)

    def send_command(self) -> None:
        """ send_command """

        self.conn.sendall(str(self.command_textbox.text()).encode('UTF-8'))
        self.command_history.addItem(self.conn.recv(2048).decode('UTF-8'))        

    def rates_server_connect(self) -> None:
        """ connect to rates server """

        connect_worker = ConnectWorker('127.0.0.1', 5050)
        connect_worker.signals.status.connect(self.status.setText)
        connect_worker.signals.conn.connect(self.set_conn)
        connect_worker.signals.msg.connect(self.command_history.addItem)
        self.threadpool.start(connect_worker)


    def set_conn(self, conn: socket.socket):
        self.conn = conn

    def rates_server_disconnect(self) -> None:
        """ disconnect from rates server """

        if self.conn:
            self.conn.close()
            self.conn = None
            self.status.setText("Disconnected")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

# Start the event loop.
app.exec()