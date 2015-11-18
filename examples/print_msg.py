from pymys import mysensors as mys


PORT = "/dev/ttyACM0"


def show_msg(msg):
    print("Read: {}".format(msg))


gw = mys.SerialGateway(PORT, message_callback=show_msg)
print("Trying to connect...")
gw.connect()
print("Connected!")

while True:
    gw.process()