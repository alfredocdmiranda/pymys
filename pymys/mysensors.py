"""
pymys - Python implementation of the MySensors Gateways and its helpers objects
"""

import time
import serial

from pymys import mys_14
from pymys import mys_15
from pymys import mys_16


class Gateway(object):
    """ Base implementation for a MySensors Gateway. """

    def __init__(self, message_callback=None, protocol_version=None):
        self.message_callback = message_callback
        self.nodes = {}
        self._protocol_version = protocol_version
        if self._protocol_version == 1.4:
            self._const = mys_14
        elif self._protocol_version == 1.5:
            self._const = mys_15
        elif self._protocol_version == 1.6:
            self._const = mys_16

        self.log_queue = []
        self.callbacks = {}

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

        for msg_type in self._const.MessageType:
            method_name = msg_type.name.split("_")[1].lower()
            self.callbacks[msg_type] = getattr(self, method_name)

    @property
    def protocol_version(self):
        return self._protocol_version

    @protocol_version.setter
    def protocol_version(self, value):
        self._protocol_version = float(value)

        if self._protocol_version == 1.4:
            self._const = mys_14
        elif self._protocol_version == 1.5:
            self._const = mys_15
        elif self._protocol_version == 1.6:
            self._const = mys_16

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

    def receive(self):
        pass

    def presentation(self, msg):
        """
          Processes a presentation message.
          :param msg: Message from gateway.
        """
        # FIXME If a node with a repeated ID was presented, it will be "merged" to the old node.

        self.const.Presentation(msg.sub_type)

        if msg.node_id not in self.nodes:
            self.nodes[msg.node_id] = Node(msg.node_id)

        self.nodes[msg.node_id].add_sensor(msg.sensor_id, self.const.Presentation(msg.sub_type))

    def set(self, msg):
        """
          Processes a set and a request message.
          :param msg: Message from gateway.
        """
        self.const.SetReq(msg.sub_type)

        self.nodes[msg.node_id].set_child_value(msg.sensor_id, self.const.SetReq(msg.sub_type), msg.payload)

    def req(self, msg):
        self.const.SetReq(msg.sub_type)

    def stream(self, msg):
        # TODO Implement
        self.const.Stream(msg.sub_type)

    def internal(self, msg):
        """
          Processes an internal message.
          :param msg: Message from gateway.
        """

        self.const.Internal(msg.sub_type)

        if msg.sub_type == self.const.Internal.I_ID_REQUEST and msg.node_id == 255:
            free_id = self.get_free_id()
            response = msg.copy(**{'sub_type': self.const.Internal.I_ID_RESPONSE, 'payload': free_id})
            self.send(response)
        elif msg.sub_type == self.const.Internal.I_LOG_MESSAGE:
            self.log_queue.append(msg)
        elif msg.sub_type == self.const.Internal.I_BATTERY_LEVEL:
            self.nodes[msg.node_id].battery_level = int(msg.payload)
        elif msg.sub_type == self.const.Internal.I_SKETCH_NAME:
            self.nodes[msg.node_id].sketch_name = msg.payload
        elif msg.sub_type == self.const.Internal.I_SKETCH_VERSION:
            self.nodes[msg.node_id].sketch_version = float(msg.payload)
        elif msg.sub_type == self.const.Internal.I_TIME:
            response = msg.copy({'payload': int(time.time())})
            self.send(response)

    def process(self):
        """
        Parse the data and respond to it appropriately.
        Response is returned to the caller and has to be sent
        data is a pymys command string
        """

        data = self.receive()
        if data:
            msg = Message(data)

            msg_type = self.const.MessageType(msg.type)
            self.callbacks[msg_type](msg)

            if self.message_callback:
                self.message_callback(msg)

    def get_free_id(self):
        free_ids = [ i for i in range(1,255) if i not in self.nodes.keys() ]
        return free_ids[0]

    def __getitem__(self, item):
        return self.nodes[item]


class SerialGateway(Gateway):
    """ MySensors Serial Gateway. """

    def __init__(self, port, baudrate=115200, message_callback=None, protocol_version=None, **kwargs):
        self.serial = None
        self.port = port
        self.baudrate = baudrate
        self.timeout = kwargs.get('timeout', 10.0)
        super(SerialGateway, self).__init__(message_callback, protocol_version, **kwargs)

    def connect(self):
        """ Connects to the serial port. """

        if not self.serial:
            connected = False
            try:
                self.serial = serial.Serial(port=self.port, baudrate=self.baudrate,
                                            parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                                            bytesize=serial.EIGHTBITS, timeout=self.timeout)
                msg = Message()
                for _ in range(2):
                    data = self.serial.readline().decode("utf-8")
                    if not data:
                        raise GatewayError("Gateway not initialized correctly.")
                    msg.decode(data)
                    if msg.node_id == 0 and msg.type == 3:
                        if msg.sub_type == 9:
                            self.log_queue.append(msg.payload)
                        elif msg.sub_type == 14:
                            connected = True

                if not connected:
                    raise GatewayError("Gateway not initialized correctly.")

                if self.protocol_version is None:
                    msg = Message("0;0;3;0;2;")
                    self.serial.write(msg.encode().encode("utf-8"))
                    data = self.serial.readline().decode("utf-8")
                    msg.decode(data)
                    if msg.node_id == 0 and msg.type == 3 and msg.sub_type == 2:
                        self.protocol_version = msg.payload
                        self.const = self.protocol_version

            except serial.SerialException as err:
                raise GatewayError("Gateway not connected or problem in Serial connection.")
        return True

    def disconnect(self):
        """ Disconnects from the serial port. """
        if self.serial is not None:
            self.serial.close()
            self.serial = None

    def receive(self):
        return self.serial.readline().decode("utf-8")

    def send(self, message):
        """ Sends a Message to the gateway. """
        self.serial.write(message.encode().encode("utf-8"))


class EthernetGateway(Gateway):
    """ MySensors Ethernet Gateway (Not impemented yet) """
    pass


class Node(object):
    """ Represents a node. """

    def __init__(self, sensor_id):
        self.id = sensor_id
        self.sensors = {}
        self.sketch_name = ""
        self.sketch_version = 0.0
        self.battery_level = 0

    def add_sensor(self, id, type):
        """ Creates and adds a child sensor. """
        if id not in self.sensors:
            self.sensors[id] = Sensor(id, type)

    def set_sensor_value(self, id, value_type, value):
        """ Sets a child sensor's value. """
        if id in self.sensors:
            self.sensors[id].values[value_type] = value
        # TODO: Handle error

    def __getitem__(self, item):
        return self.sensors[item]

    def __str__(self):
        return "N_ID: {n.id} | SKETCH NAME: {n.sketch_name} | SKETCH_VERSION: {n.sketch_version} | "\
                "BATTERY LEVEL: {n.battery_level}".format(n=self)


class Sensor(object):
    """ Represents a sensor. """

    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.values = {}

    def __str__(self):

        return "S_ID: {s.id} | TYPE: {s.type.name} | VALUES: {s.values}".format(s=self)


class Message(object):
    """ Represents a message from the gateway. """

    def __init__(self, raw=None):
        self.node_id = 0
        self.sensor_id = 0
        self.type = ""
        self.ack = 0
        self.sub_type = ""
        self.payload = ""
        if raw is not None:
            self.decode(raw)

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
        try:
            data = data.rstrip().split(';')
            self.payload = data.pop()
            (self.node_id,
             self.sensor_id,
             self.type,
             self.ack,
             self.sub_type) = [int(f) for f in data]
        except ValueError:
            raise BadMessageError("Malformed message: {}".format(data))

    def encode(self):
        """ Encode a command string from message. """
        return ";".join([str(f) for f in [
            self.node_id,
            self.sensor_id,
            int(self.type),
            self.ack,
            int(self.sub_type),
            self.payload,
        ]]) + "\n"

    def __str__(self):
        return "{};{};{};{};{};{}".format(self.node_id, self.sensor_id, self.type, self.ack, self.sub_type, self.payload)


# Custom Exceptions


class GatewayError(Exception):
    def __init__(self, *args, **kwargs):
        super(GatewayError, self).__init__(*args, **kwargs)


class BadMessageError(Exception):
    def __init__(self, *args, **kwargs):
        super(BadMessageError, self).__init__(*args, **kwargs)