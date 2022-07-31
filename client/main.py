import json
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
import threading, time, requests, websocket

def communicate():
    if ws is None:
        alert_box = QMessageBox()
        alert_box.setText("You must join a room before sending messages!")
        alert_box.setIcon(QMessageBox.Icon.Warning)
        alert_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        alert_box.exec()
        return

    msgs.insertPlainText(f"{name}: {input_text.text()}\n")
    input_text.setText("")

def check_for_messages():
    pass

def join_room():
    ws = websocket.create_connection(f"ws://localhost:8000/ws/{join_room_input.text()}/{client_id}")
    ws.send(json.dumps({"type": "room_join", "room_id": join_room_input.text(), "name": name, "id": client_id}))
    
    data = json.loads(ws.recv())
    if data["type"] == "room_join_success":
        room_info_group.setTitle(f"Connected to: {join_room_input.text()}")

def set_name():
    global name
    name = name_input.text()
    name_input.hide()
    confirm_button.hide()
    app.quit()

if __name__ == "__main__":
    # Getting username
    app = QApplication([])
    window = QWidget()
    grid = QGridLayout()

    name = ""
    name_input = QLineEdit()
    name_input.setPlaceholderText("name")
    confirm_button = QPushButton("continue")
    confirm_button.clicked.connect(lambda: set_name())
    grid.addWidget(name_input)
    grid.addWidget(confirm_button)

    window.setLayout(grid)
    window.show()

    app.exec()

    # Setting up the chat interface
    grid.setColumnStretch(0, 1)
    grid.setColumnStretch(1, 0)
    grid.setColumnStretch(2, 0)

    header = QHBoxLayout()
    header.addWidget(QLabel("Dontsnoo"))
    header.addWidget(QLabel(f"Logged in as: {name}"))

    grid.addLayout(header, 0, 0, 1, 2)

    msgs = QPlainTextEdit()
    msgs.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    grid.addWidget(msgs, 2, 2)

    uno_canvas = QPainter()

    grid.addWidget(QPlainTextEdit("uno QPainter here"), 1, 0, 3, 2)

    input_area = QHBoxLayout()
    input_text = QLineEdit()
    input_text.setPlaceholderText("enter message here")
    send_button = QPushButton("send")
    input_area.addWidget(input_text)
    input_area.addWidget(send_button)

    grid.addLayout(input_area, 3, 2)

    room_and_users_info_box = QVBoxLayout()
    room_info_layout = QVBoxLayout()

    room_info_group = QGroupBox("0 Users in Room 24110")

    join_room_box = QHBoxLayout()
    join_room_label = QLabel("Join Room:")
    join_room_input = QLineEdit()
    join_room_submit = QPushButton("join")
    join_room_box.addWidget(join_room_label)
    join_room_box.addWidget(join_room_input)
    join_room_box.addWidget(join_room_submit)

    room_info_layout.addLayout(join_room_box)
    room_info_layout.addWidget(room_info_group)

    room_and_users_info_box.addLayout(room_info_layout)

    grid.addLayout(room_and_users_info_box, 1, 2)

    window.setLayout(grid)
    window.show()

    send_button.clicked.connect(lambda: communicate())
    join_room_submit.clicked.connect(lambda: join_room())

    client_id = str(round(time.time()))
    ws = None

    thread = threading.Thread(target=check_for_messages)
    thread.daemon = True
    thread.start()

    app.exec()