"""
pymys - Python implementation of the MySensors Gateways and its helpers objects
"""

import serial

from mysensors import mys_14
from mysensors import mys_15
from mysensors import mys_16


class Gateway(object):
    """ Base implementation for a MySensors Gateway. """

    def __init__(self, message_callback=None, protocol_version=None, debug=False):
        super(Gateway, self).__init__()
        self.message_callback = message_callback
        self.nodes = {}
        self.debug = debug
        self.protocol_version = protocol_version
        if self.protocol_version == 1.4:
            self._const = mys_14
        elif self.protocol_version == 1.5:
            self._const = mys_15
        elif self.protocol_version == 1.6:
            self._const = mys_16

        self.log_queue = []

    @property
    def const(self):
        return self._const

    @const.setter
    def const(self, value):
        if value == '1.4':
            self._const = mys_14
        elif value == '1.5':
            self._const = mys_15
        elif value == '1.6':
            self._const = mys_16
        else:
            # TODO Raise an exception
            pass

        self.callbacks = {self._const.MessageType.C_PRESENTATION: self.presentation,
                          self._const.MessageType.C_SET: self.set,
                          self._const.MessageType.C_REQ: self.req,
                          self._const.MessageType.C_INTERNAL: self.internal,
                          self._const.MessageType.C_STREAM: self.stream}

    def connect(self):
        pass

    def disconnect(self):
        pass

    def send(self, msg):
        """
          Sends a message to Gateway.
          Must be implemented on a specialized class.
          :param msg: Message to gateway.
        """
        pass

    def presentation(self, msg):
        """
          Processes a presentation message.
          :param msg: Message from gateway.
        """
        print(msg)

    def set(self, msg):
        """
          Processes a set and a request message.
          :param msg: Message from gateway.
        """
        print(msg)

    def req(self, msg):
        print(msg)

    def stream(self, msg):
        print(msg)

    def internal(self, msg):
        """
          Processes an internal message.
          :param msg: Message from gateway.
        """
        print(msg)

    def process(self, data):
        """
        Parse the data and respond to it appropriately.
        Response is returned to the caller and has to be sent
        data is a mysensors command string
         """
        pass

    # def alert(self, nid):
    #     """
    #     Tell anyone who wants to know that a sensor was updated. Also save
    #     sensors if persistence is enabled
    #     """
    #     pass

    # def add_sensor(self, sensorid=None):
    #     """ Adds a sensor to the gateway. """
    #     if sensorid is None:
    #         sensorid = self._get_next_id()
    #     if sensorid is not None and sensorid not in self.sensors:
    #         self.sensors[sensorid] = Sensor(sensorid)
    #         return sensorid
    #     return None

    # def is_sensor(self, sensorid, child_id=None):
    #     """ Returns True if a sensor and its child exists. """
    #     if sensorid not in self.sensors:
    #         return False
    #     if child_id is not None:
    #         return child_id in self.sensors[sensorid].children
    #     return True


class SerialGateway(Gateway):
    """ MySensors Serial Gateway. """

    def __init__(self, port, baudrate=115200, message_callback=None, protocol_version=None, **kwargs):
        self.serial = None
        self.port = port
        self.baudrate = baudrate
        self.timeout = kwargs.get('timeout', 10.0)
        super(SerialGateway, self).__init__(self, message_callback, protocol_version, **kwargs)

    def connect(self):
        """ Connects to the serial port. """

        if not self.serial:
            try:
                self.serial = serial.Serial(port=self.port, baudrate=self.baudrate,
                                            parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                                            bytesize=serial.EIGHTBITS, timeout=self.timeout)
                msg = Message()
                for _ in range(2):
                    data = self.serial.readline().decode("utf-8")
                    msg.decode(data)
                    if msg.node_id == 0 and msg.type == 3:
                        if msg.sub_type == 9:
                            self.log_queue.append(msg.payload)
                        elif msg.sub_type == 14:
                            connected = True
                # if not connected:
                #     # TODO Raise an exception here
                #     print("Not connected.")

                if self.protocol_version is None:
                    msg = Message("0;0;3;0;2;")
                    self.serial.write(msg.encode().encode("utf-8"))
                    data = self.serial.readline().decode("utf-8")
                    msg.decode(data)
                    if msg.node_id == 0 and msg.type == 3 and msg.sub_type == 2:
                        self.protocol_version = msg.payload
                        self.const = self.protocol_version
            # TODO Create exception if gateway was not started correclty.
            except serial.SerialException as err:
                # TODO Raise an custom exception here
                return False
        return True

    def disconnect(self):
        """ Disconnects from the serial port. """
        if self.serial is not None:
            self.serial.close()
            self.serial = None

    def process(self):
        """ Background thread that reads messages from the gateway. """

        data = self.serial.readline().decode("utf-8")
        if data:
            msg = Message()
            msg.decode(data)

            msg_type = self.const.MessageType(msg.type)
            self.callbacks[msg_type](msg)

            # if msg.type == self.const.MessageType.C_PRESENTATION:
            #     print("Presentation")
            # elif msg.type == self.const.MessageType.C_SET:
            #     print("Set")
            # elif msg.type == self.const.MessageType.C_REQ:
            #     print("Req")
            # elif msg.type == self.const.MessageType.C_INTERNAL:
            #     print("Internal")
            # elif msg.type == self.const.MessageType.C_STREAM:
            #     print("Stream")

        return True

    def send(self, message):
        """ Sends a Message to the gateway. """
        self.serial.write(message.encode().encode("utf-8"))


    # def __str__(self):
    #     return "Port: {} | Baudrate: {} | MyS Protocol: {}".format(self.serial.port, self.serial.baudrate,
    #                                                                self.protocol_version)


class EthernetGateway(Gateway):
    """ MySensors Ethernet Gateway (Not impemented yet) """
    pass


class Node(object):
    """ Represents a node. """

    def __init__(self, sensor_id):
        self.node_id = sensor_id
        self.sensors = {}
        self.type = None
        self.sketch_name = ""
        self.sketch_version = 0.0
        self.battery_level = 0

    def add_child_sensor(self, child_id, child_type):
        """ Creates and adds a child sensor. """
        self.children[child_id] = Sensor(child_id, child_type)

    def set_child_value(self, child_id, value_type, value):
        """ Sets a child sensor's value. """
        if child_id in self.children:
            self.children[child_id].values[value_type] = value
        # TODO: Handle error

    def __iter__(self):
        pass


class Sensor(object):
    """ Represents a sensor. """

    def __init__(self, sensor_id, sensor_type):
        self.id = child_id
        self.type = child_type
        self.values = {}


class Message(object):
    """ Represents a message from the gateway. """

    def __init__(self, data=None):
        self.node_id = 0
        self.child_id = 0
        self.type = ""
        self.ack = 0
        self.sub_type = ""
        self.payload = ""
        if data is not None:
            self.decode(data)

    def copy(self, **kwargs):
        """
        Copies a message, optionally replacing attributes with keyword
        arguments.
        """
        msg = Message(self.encode())
        for key, val in kwargs.items():
            setattr(msg, key, val)
        return msg

    def decode(self, data):
        """ Decode a message from command string. """
        data = data.rstrip().split(';')
        self.payload = data.pop()
        (self.node_id,
         self.child_id,
         self.type,
         self.ack,
         self.sub_type) = [int(f) for f in data]

    def encode(self):
        """ Encode a command string from message. """
        return ";".join([str(f) for f in [
            self.node_id,
            self.child_id,
            int(self.type),
            self.ack,
            int(self.sub_type),
            self.payload,
        ]]) + "\n"

    def __str__(self):
        return "{};{};{};{};{};{}".format(self.node_id, self.child_id, self.type, self.ack, self.sub_type, self.payload)
