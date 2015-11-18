import threading

from pymys import mysensors as mys


PORT = "/dev/ttyACM0"


def run_gateway():
    while True:
        gw.process()


def show_msg(msg):
    print("Read: {}".format(msg))

gw = mys.SerialGateway(PORT, message_callback=show_msg)
print("Trying to connect...")
gw.connect()
print("Connected!")

t = threading.Thread(target=run_gateway)
t.start()

while True:
    data = input("")
    msg = mys.Message(data)
    gw.send(msg)