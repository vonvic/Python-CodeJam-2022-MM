import json
import threading
import time

import PyQt6.QtGui as QtGui
import PyQt6.QtWidgets as QtWidgets
import websocket
from PyQt6.QtCore import Qt


def communicate():
    """Displays message from input box into the messages box."""
    if ws is None:
        alert_box = QtWidgets.QMessageBox()
        alert_box.setText("You must join a room before sending messages!")
        alert_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        alert_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        alert_box.exec()
        return

    msgs.insertPlainText(f"{name}: {input_text.text()}\n")

    ws.send(
        json.dumps(
            {
                "type": "message_sent",
                "username": name,
                "content": input_text.text()
            }
        )
    )

    input_text.setText("")


def check_for_messages():
    """Constantly checks for messages received from the server and displays the message once one is received."""
    global current_room, user_list
    while True:
        if ws is not None:
            try:
                data = json.loads(ws.recv())
            
            except:
                continue

            user = data["username"]

            if data["type"] == "room_join_success":
                room_info_group.setTitle(f"Connected to: {join_room_input.text()}")
                msgs.insertPlainText("You have joined the room!\n")
                join_room_input.setText("")
                current_room = data["room_id"]
                user_list = data["users"]
                room_info_group.setTitle(f"Connected to {current_room} with {len(user_list)} other users")
            
            elif data["type"] == "user_join" and user != name:
                msgs.insertPlainText(f"{user} has joined the room!\n")
                user_list = data["users"]
                room_info_group.setTitle(f"Connected to {current_room} with {len(user_list)} other users")
            
            elif data["type"] == "room_disconnect_success" and user != name:
                msgs.insertPlainText(f"{user} has left the room\n")
                user_list = data["users"]
                room_info_group.setTitle(f"Connected to {current_room} with {len(user_list)-1} other users")
            
            elif data["type"] == "message_sent" and user != name:
                message = data["content"]
                msgs.insertPlainText(f"{user}: {message}\n")


def join_room():
    """Joins a room at localhost."""
    global ws
    if current_room != join_room_input.text():
        if ws is not None:
            ws.close()

        join_room_input.setText(join_room_input.text().replace(" ", ""))

        if len(join_room_input.text()) == 0:
            alert_box = QtWidgets.QMessageBox()
            alert_box.setText("You may not use spaces or empty characters for room codes!")
            alert_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            alert_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            alert_box.exec()
            return

        ws = websocket.create_connection(f"ws://localhost:8000/ws/{join_room_input.text()}/{client_id}")
        ws.send(json.dumps({"type": "room_join", "room_id": join_room_input.text(), "name": name, "id": client_id}))

    else:
        alert_box = QtWidgets.QMessageBox()
        alert_box.setText("You cannot join the same room!")
        alert_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        alert_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        alert_box.exec()


def set_name():
    """Sets the username."""
    global name
    name = name_input.text()
    if len(name.replace(" ", "")) == 0:
        alert_box = QtWidgets.QMessageBox()
        alert_box.setText("Please enter a valid name")
        alert_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        alert_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        alert_box.exec()
        return

    name_input.hide()
    confirm_button.hide()
    app.quit()

def show_connected_users():
    global user_list
    alert_box = QtWidgets.QMessageBox()
    alert_box.setText("Users\n" + '\n'.join(user_list))
    alert_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
    alert_box.exec()

if __name__ == "__main__":
    # Getting username
    app = QtWidgets.QApplication([])
    window = QtWidgets.QWidget()
    grid = QtWidgets.QGridLayout()

    name = ""
    name_input = QtWidgets.QLineEdit()
    name_input.setPlaceholderText("name")
    confirm_button = QtWidgets.QPushButton("continue")
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

    header = QtWidgets.QHBoxLayout()
    header.addWidget(QtWidgets.QLabel("Dontsnoo"))
    header.addWidget(QtWidgets.QLabel(f"Logged in as: {name}"))

    grid.addLayout(header, 0, 0, 1, 2)

    msgs = QtWidgets.QPlainTextEdit()
    msgs.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    grid.addWidget(msgs, 2, 2)

    uno_canvas = QtGui.QPainter()

    grid.addWidget(QtWidgets.QPlainTextEdit("uno QPainter here"), 1, 0, 3, 2)

    input_area = QtWidgets.QHBoxLayout()
    input_text = QtWidgets.QLineEdit()
    input_text.setPlaceholderText("enter message here")
    send_button = QtWidgets.QPushButton("send")
    input_area.addWidget(input_text)
    input_area.addWidget(send_button)

    grid.addLayout(input_area, 3, 2)

    room_and_users_info_box = QtWidgets.QVBoxLayout()
    room_info_layout = QtWidgets.QVBoxLayout()

    room_info_group = QtWidgets.QGroupBox("Not connected")

    show_users = QtWidgets.QPushButton("users")

    join_room_box = QtWidgets.QHBoxLayout()
    join_room_label = QtWidgets.QLabel("Join Room:")
    join_room_input = QtWidgets.QLineEdit()
    join_room_submit = QtWidgets.QPushButton("join")
    join_room_box.addWidget(join_room_label)
    join_room_box.addWidget(join_room_input)
    join_room_box.addWidget(join_room_submit)

    room_info_layout.addLayout(join_room_box)
    room_info_layout.addWidget(room_info_group)
    room_info_layout.addWidget(show_users)

    room_and_users_info_box.addLayout(room_info_layout)

    grid.addLayout(room_and_users_info_box, 1, 2)

    window.setLayout(grid)
    window.show()

    send_button.clicked.connect(lambda: communicate())
    join_room_submit.clicked.connect(lambda: join_room())
    show_users.clicked.connect(lambda: show_connected_users())

    client_id = str(round(time.time()))
    ws = None
    current_room = None
    user_list = []

    thread = threading.Thread(target=check_for_messages)
    thread.daemon = True
    thread.start()

    app.exec()
