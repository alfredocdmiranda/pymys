# pyMYS
It is a module to make easier communication with MySensor's network.

This module was originally based on pymysensors module. However, in its way it took some changes which led it to what 
you can see now.

You can find more information about the MySensors Project on its official webpage (http://www.mysensors.org/).

## Documentation

Currently, all documentation can be accessed in project's GitHub page.

## Dependencies

You can find all dependencies in requirements.txt and
install them using pip.

- pyserial

## Installation

    python setup.py install

or

    pip pymys

## Support

This project should support all Python 3 versions. However, it was only tested with Python 3.4.

## Protocol Version Supported

This module should support MySensors 1.4, 1.5 and 1.6 protocol.

## Data Structures

    Gateway                     Implements Gateway's base
        - nodes                 Dictionary of nodes
        - protocol_version      Gateway's protocol version
        - log_queue             A queue of log messages
        - const                 Variable that points to the module of contants (mys_14, mys_15, mys_16, ...)
        - callbacks             A dictionary that points to the functions which will handle each message type
    
    SerialGateway               It is an specialization to communicate over Serial port
    
    EthernetGateway             It is an specialization to communicate over Ethernet port
    
    Node                        Implements Node structure
        - id                    Node's id
        - sensors               Dictionary of sensors
        - sketch_name           Sketch name
        - sketch_version        Sketch version
        - battery_level         Battery level
    
    Sensor                      Implements Sensor structure
        - id                    Sensor's id
        - type                  Sensor's type
        - values                Dictionary of values
    
    Message                     Implements Message structure
        - node_id               Node's id
        - sensor_id             Sensor's id
        - type                  Message type
        - ack                   If a message is an ACK message
        - sub_type              Subtype Message
        - payload               Message's payload

## Methods

    Gateway
        - connect               Connects on the interface. It should be implemented on child classes
        - disconnect            Disconnects from the interface. It should be implemented on child classes
        - send                  Sends a message to the network. It should be implemented on child classes
        - receive               Receives a message from the network. It should be implemented on child classes
        - presentation          Handles presentation messages
        - set                   Handles set messages
        - req                   Handles request messages
        - stream                Handles stream messages
        - internal              Handles internal messages
        - process               Try to receive a message and handle it
        - get_free_id           Return a free id to be assign to a node
    
    Node
        - add_sensor            Includes a node in list of sensors
        - set_sensor_value      Set a new value to a sensor
    Message
        - copy                  Return a new Message object
        - decode                Fill the object using a raw message
        - encode                Return a raw message using object's information

## Customization

You can customize your own Gateway by creating a new class which inherit from the SerialGateway or EthernetGateway or 
even from base Gateway (you will have to implement some required methods such as connect, send and receive). After that, 
you just need to implement the methods you want to change.

    from pymys import mysensors as mys
    
    class NewSerialProtocol(mys.SerialGateway):
        def presentation(self, msg):
            # Overwriting presentation handle
            pass

If you don't want to create a whole new class, you can just create a function and change on obeject's callbacks attribute/

    from pymys import mysensors as mys
    
    def presentation(gw, msg):
        # Now you can access Gateway object and Message object
        pass
    
    gw = mys.SerialGateway("/dev/ttyACM0")
    gw.callbacks[0] = presentation

## Usage

    