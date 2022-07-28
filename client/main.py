from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *

if __name__ == "__main__":
    app = QApplication([])
    window = QWidget()
    grid = QGridLayout()

    grid.setColumnStretch(0, 1)
    grid.setColumnStretch(1, 0)
    grid.setColumnStretch(2, 0)

    header = QHBoxLayout()
    header.addWidget(QLabel("Dontsnoo"))

    grid.addLayout(header, 0, 0, 1, 2)

    msgs = QPlainTextEdit()
    msgs.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    grid.addWidget(msgs, 2, 2)

    uno_canvas = QPainter()

    grid.addWidget(QPlainTextEdit("uno QPainter here"), 1, 0, 3, 2)

    input_area = QHBoxLayout()
    input_text = QLineEdit()
    input_text.setPlaceholderText("enter message here")
    send_button = QPushButton("join")
    input_area.addWidget(input_text)
    input_area.addWidget(send_button)

    grid.addLayout(input_area, 3, 2)

    room_and_users_info_box = QVBoxLayout()
    room_info_layout = QVBoxLayout()

    room_info_group = QGroupBox("0 Users in Room 24110")

    join_room_box = QHBoxLayout()
    join_room_label = QLabel("Join Room:")
    join_room_input = QLineEdit()
    join_room_submit = QPushButton("send")
    join_room_box.addWidget(join_room_label)
    join_room_box.addWidget(join_room_input)
    join_room_box.addWidget(join_room_submit)

    room_info_layout.addLayout(join_room_box)
    room_info_layout.addWidget(room_info_group)

    room_and_users_info_box.addLayout(room_info_layout)

    grid.addLayout(room_and_users_info_box, 1, 2)

    window.setLayout(grid)
    window.show()
    app.exec()
