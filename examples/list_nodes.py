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

input("You should initialize/reinitialize all your nodes and press ENTER")

while True:
    data = input("Write 'all' or the specific id which you want to see: ")
    if data == 'all':
        for node_id in gw.nodes:
            print(gw[node_id])
    else:
        node_id = int(data)
        print(gw[node_id])
        for sensor_id in gw[node_id].sensors:
            print(gw[node_id][sensor_id])
