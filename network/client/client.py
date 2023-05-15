import socketio

from network.common.messages.common import Connected
from network.common.schema import parse_message

clientio = socketio.Client(logger=True)
my_user_id = ""


@clientio.event
def connected(data: dict) -> None:
    message = parse_message(Connected, data, "아이디 부여")

    global my_user_id
    my_user_id = message.id


PORT = 10008
LOCAL_SERVER_ADDRESS = f"http://127.0.0.1:{PORT}"
