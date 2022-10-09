import typing
from PyQt5.QtGui import QFont

from threading import Thread
from PyQt5.QtWidgets import QGridLayout, QLabel, QPlainTextEdit, QPushButton, QWidget, QApplication

from Encoder import Encoder


class ControlWidget(QWidget):
    def __init__(self, board, encoder: Encoder,
            parent: typing.Optional['QWidget'] = None,) -> None:
        super().__init__(parent=parent)
        
        self.CreateItems()
        self.CreateLayout()
        self.CreateSignalSlot()

        self.setFont(QFont('Consolas', 12))

        self.board = board
        self.encoder = encoder

    def CreateItems(self):
        self.encode_label = QLabel("Encode String:")
        self.encode_label.setFixedWidth(200)
        self.encode_label.setFixedHeight(20)
        self.encode_input = QPlainTextEdit()
        self.encode_input.setFixedHeight(self.encode_label.height())
        self.encode_start_btn = QPushButton("Start")
        self.encode_start_btn.setFixedHeight(self.encode_label.height())

        self.decode_label = QLabel("Decode result:")
        self.decode_label.setFixedWidth(200)
        self.decode_label.setFixedHeight(20)
        self.decode_input = QPlainTextEdit()
        self.decode_input.setFixedHeight(self.decode_label.height())
        # self.decode_input.setReadOnly(True)

        self.log_box = QPlainTextEdit()
        self.log_box.setFixedHeight(100)
        self.log_box.setMaximumBlockCount(60000)

    def CreateLayout(self):
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.encode_label, 0, 0)
        self.mainLayout.addWidget(self.encode_input, 0, 1)
        self.mainLayout.addWidget(self.encode_start_btn, 0, 2)
        # self.mainLayout.addWidget(self.decode_label, 1, 0)
        # self.mainLayout.addWidget(self.decode_input, 1, 1)
        self.mainLayout.addWidget(self.log_box, 2, 0, 1, 3)
        self.mainLayout.setSpacing(5)
        self.setLayout(self.mainLayout)

    def CreateSignalSlot(self):
        self.encode_start_btn.clicked.connect(self._on_start_btn_clicked)

    def _on_start_btn_clicked(self):
        info = self.encode_input.toPlainText()
        if not info.strip(): return
        t = Thread(target=self.encoder.encode, args=(info,))
        t.start()

    def output_to_logbox(self, data):
        self.log_box.insertPlainText(f"{data}\n")

    def update_result(self, data):
        self.decode_input.clear()
        self.decode_input.insertPlainText(f"{data}")
        self.decode_input.update()
